#!/usr/bin/env python3
"""Vérifie que les vidéos YouTube embarquées dans les posts sont toujours en ligne.

Usage:  python3 tools/check-videos.py [fichier.md ...]
Sans argument, vérifie tous les posts.
Sortie: code 1 si au moins une vidéo est morte (utilisable en cron / CI).
"""
import glob
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

EMBED_RE = re.compile(r'youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=)([A-Za-z0-9_-]+)')
OEMBED = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={}&format=json"


def extract(paths):
    """-> [(fichier, ligne, id)] pour chaque embed trouvé."""
    found = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                for vid in EMBED_RE.findall(line):
                    found.append((path, n, vid))
    return found


def check(item):
    path, line, vid = item
    if len(vid) != 11:
        return dict(file=path, line=line, id=vid, ok=False,
                    reason=f"id invalide ({len(vid)} car., attendu 11)", title="", channel="")
    req = urllib.request.Request(OEMBED.format(vid), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            d = json.load(resp)
        return dict(file=path, line=line, id=vid, ok=True, reason="",
                    title=d.get("title", ""), channel=d.get("author_name", ""))
    except urllib.error.HTTPError as e:
        reason = {401: "embed désactivé", 403: "privée ou restreinte",
                  404: "supprimée"}.get(e.code, f"HTTP {e.code}")
        return dict(file=path, line=line, id=vid, ok=False, reason=reason, title="", channel="")
    except Exception as e:
        return dict(file=path, line=line, id=vid, ok=False,
                    reason=f"réseau: {type(e).__name__}", title="", channel="")


def main():
    paths = sys.argv[1:] or sorted(glob.glob("all_collections/_posts/*.md"))
    items = extract(paths)
    if not items:
        print("Aucun embed YouTube trouvé.")
        return 0

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(check, items))
    results.sort(key=lambda r: (r["file"], r["line"]))

    with open("tools/videos-status.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)

    dead = [r for r in results if not r["ok"]]
    print(f"{len(results)} embeds — {len(results) - len(dead)} OK, {len(dead)} en échec\n")
    for r in dead:
        print(f"  {r['file']}:{r['line']}  {r['id']}  → {r['reason']}")
    if dead:
        print("\nMétadonnées complètes : tools/videos-status.json")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
