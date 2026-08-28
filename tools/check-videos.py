#!/usr/bin/env python3
"""Vérifie que les vidéos YouTube embarquées dans les posts sont toujours lisibles.

Usage:  python3 tools/check-videos.py [--deep] [fichier.md ...]
Sans argument, vérifie tous les posts.
Sortie: code 1 si au moins une vidéo pose problème (utilisable en cron / CI).

  --deep  interroge aussi yt-dlp. Plus lent, mais attrape ce que oEmbed rate :
          une vidéo bloquée dans ton pays pour revendication de droits répond
          200 à oEmbed (elle existe) alors qu'elle ne se lit pas.
"""
import glob
import json
import shutil
import subprocess
import os
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


def find_ytdlp():
    """Le yt-dlp le plus récent : une version périmée donne des faux négatifs."""
    best = best_v = None
    cands = [shutil.which("yt-dlp")]
    try:
        prefix = subprocess.run(["brew", "--prefix", "yt-dlp"], capture_output=True,
                                text=True, timeout=10).stdout.strip()
        if prefix:
            cands.insert(0, os.path.join(prefix, "bin", "yt-dlp"))
    except Exception:
        pass
    for c in cands:
        if not c or not os.access(c, os.X_OK):
            continue
        try:
            v = subprocess.run([c, "--version"], capture_output=True, text=True,
                               timeout=15).stdout.strip()
        except Exception:
            continue
        if v and (best_v is None or v > best_v):
            best, best_v = c, v
    return best


def deep_check(results, ytdlp):
    """Confirme la lisibilité réelle. Ne contredit oEmbed que sur un blocage avéré."""
    for r in results:
        if not r["ok"]:
            continue
        try:
            p = subprocess.run(
                [ytdlp, "--skip-download", "--no-warnings", "--print", "%(availability)s",
                 f"https://www.youtube.com/watch?v={r['id']}"],
                capture_output=True, text=True, timeout=60)
        except Exception:
            continue
        err = p.stderr or ""
        # Le rate-limiting n'est pas un défaut de la vidéo : on ne le signale pas ici.
        if "not a bot" in err or "Sign in to confirm" in err:
            continue
        if p.returncode != 0 and ("unavailable" in err or "blocked" in err or "Private" in err):
            m = re.search(r"ERROR:.*?:\s*(.{0,110})", err)
            r["ok"] = False
            r["reason"] = "lecture bloquée — " + (m.group(1).strip() if m else "indisponible")


def main():
    args = sys.argv[1:]
    deep = "--deep" in args
    args = [a for a in args if a != "--deep"]
    paths = args or sorted(glob.glob("all_collections/_posts/*.md"))
    items = extract(paths)
    if not items:
        print("Aucun embed YouTube trouvé.")
        return 0

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(check, items))
    results.sort(key=lambda r: (r["file"], r["line"]))

    if deep:
        ytdlp = find_ytdlp()
        if ytdlp:
            print("vérification approfondie via yt-dlp…\n")
            deep_check(results, ytdlp)
        else:
            print("yt-dlp introuvable : --deep ignoré\n")

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
