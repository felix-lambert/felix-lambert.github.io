#!/usr/bin/env python3
"""
Optimise le HTML embarqué dans les posts Markdown :
  1. réécrit les images locales vers .webp quand la variante existe
  2. ajoute loading="lazy" decoding="async" + width/height sur les <img>
  3. passe les <video> en preload="none" et leur ajoute un poster
  4. remplace les <iframe> YouTube par une façade cliquable (aucun JS tiers au chargement)

Idempotent : relancer le script ne produit aucun changement supplémentaire.
Usage : python3 tools/optimize-post.py [fichier.md ...]
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "img")
POSTER_DIR = os.path.join(IMG_DIR, "posters")
DIM_CACHE = os.path.join(ROOT, "tools", "image-dims.json")

# ---------------------------------------------------------------- dimensions

try:
    _dims = json.load(open(DIM_CACHE))
except Exception:
    _dims = {}


def identify(path_or_url):
    """(largeur, hauteur) d'une image locale ou distante, avec cache disque."""
    if path_or_url in _dims:
        return tuple(_dims[path_or_url])
    target = path_or_url
    tmp = None
    if path_or_url.startswith("http"):
        try:
            tmp = "/tmp/_dim_probe"
            req = urllib.request.Request(path_or_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r, open(tmp, "wb") as f:
                f.write(r.read())
            target = tmp
        except Exception:
            _dims[path_or_url] = [0, 0]
            return (0, 0)
    try:
        out = subprocess.check_output(
            ["magick", "identify", "-format", "%w %h", target + "[0]"],
            stderr=subprocess.DEVNULL,
        ).decode()
        w, h = (int(x) for x in out.split()[:2])
    except Exception:
        w = h = 0
    if tmp and os.path.exists(tmp):
        os.remove(tmp)
    _dims[path_or_url] = [w, h]
    return (w, h)


# ------------------------------------------------------------- attributs HTML

ATTR_RE = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+))?')


def parse_attrs(tag_inner):
    attrs, order = {}, []
    for m in ATTR_RE.finditer(tag_inner):
        name = m.group(1).lower()
        val = m.group(2)
        if val and val[0] in "\"'":
            val = val[1:-1]
        if name not in attrs:
            order.append(name)
        attrs[name] = val
    return attrs, order


def build_tag(name, attrs, order, self_closing=True):
    parts = [name]
    for k in order:
        v = attrs.get(k)
        parts.append(k if v is None else f'{k}="{v}"')
    return "<" + " ".join(parts) + (" />" if self_closing else ">")


# ------------------------------------------------------------------- 1. webp

def webp_variant(path):
    """/assets/img/x.png -> /assets/img/x.webp si le fichier existe sur disque."""
    m = re.match(r"^(/?assets/img/)(.+)\.(png|jpg|jpeg|gif|PNG|JPG|JPEG|GIF)$", path)
    if not m:
        return None
    cand = f"{m.group(1)}{m.group(2)}.webp"
    if os.path.exists(os.path.join(ROOT, cand.lstrip("/"))):
        return cand
    return None


def rewrite_webp(text):
    def sub(m):
        return webp_variant(m.group(0)) or m.group(0)

    return re.sub(r"/?assets/img/[^\s\"'|}]+\.(?:png|jpg|jpeg|gif|PNG|JPG|JPEG|GIF)", sub, text)


# -------------------------------------------------------------------- 2. img

def local_path_of(src):
    """Chemin disque d'un src, en tenant compte de la syntaxe Liquid relative_url."""
    m = re.search(r"assets/img/[^\s\"'|}]+", src)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(0))
    return p if os.path.exists(p) else None


def fix_img(m):
    attrs, order = parse_attrs(m.group(1))
    src = attrs.get("src", "")

    for k, v in (("loading", "lazy"), ("decoding", "async")):
        if k not in attrs:
            attrs[k] = v
            order.append(k)

    if "width" not in attrs or "height" not in attrs:
        local = local_path_of(src)
        iw, ih = identify(local) if local else (
            identify(src) if src.startswith("http") else (0, 0)
        )
        if iw and ih:
            if "width" in attrs and str(attrs["width"]).isdigit():
                w = int(attrs["width"])
                h = max(1, round(w * ih / iw))
            else:
                w, h = iw, ih
                if "width" not in attrs:
                    attrs["width"] = str(w)
                    order.append("width")
            attrs["height"] = str(h)
            if "height" not in order:
                order.append("height")
    return build_tag("img", attrs, order)


# ------------------------------------------------------------------ 3. video

def poster_for(url):
    name = os.path.basename(url).rsplit(".", 1)[0]
    rel = f"/assets/img/posters/{name}.webp"
    return rel if os.path.exists(os.path.join(ROOT, rel.lstrip("/"))) else None


def fix_video(m):
    tag = m.group(0)
    tag = tag.replace('preload="metadata"', 'preload="none"')
    if "poster=" not in tag:
        u = re.search(r'src="(https://[^"]+\.mp4)"', tag)
        if u:
            p = poster_for(u.group(1))
            if p:
                tag = re.sub(r"<video\b", f'<video poster="{p}"', tag, count=1)
    return tag


# ---------------------------------------------------------------- 4. youtube

YT_RE = re.compile(
    r'<iframe[^>]*?(?:youtube\.com|youtube-nocookie\.com)/embed/([A-Za-z0-9_-]{6,})[^>]*>\s*</iframe>',
    re.S,
)


def fix_youtube(m):
    vid = m.group(1)
    return (
        f'<a class="yt-lite" href="https://www.youtube.com/watch?v={vid}" '
        f'data-id="{vid}" rel="noopener" aria-label="Lire la vidéo YouTube">'
        f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" '
        f'loading="lazy" decoding="async" width="480" height="360" />'
        f'<span class="yt-play" aria-hidden="true"></span></a>'
    )


# --------------------------------------------------------------------- main

def process(path):
    src = open(path, encoding="utf-8").read()
    out = rewrite_webp(src)
    n_yt = len(YT_RE.findall(out))
    out = YT_RE.sub(fix_youtube, out)
    n_img = len(re.findall(r"<img\b([^>]*?)/?>", out))
    out = re.sub(r"<img\b([^>]*?)/?>", fix_img, out)
    n_vid = len(re.findall(r"<video\b.*?(?:</video>|/>)", out, re.S))
    out = re.sub(r"<video\b.*?(?:</video>|/>)", fix_video, out, flags=re.S)

    if out != src:
        open(path, "w", encoding="utf-8").write(out)
        print(f"{os.path.relpath(path, ROOT)} : {n_img} img, {n_vid} video, {n_yt} youtube")
    else:
        print(f"{os.path.relpath(path, ROOT)} : déjà à jour")


if __name__ == "__main__":
    files = sys.argv[1:] or [
        os.path.join(ROOT, "all_collections/_posts", f)
        for f in os.listdir(os.path.join(ROOT, "all_collections/_posts"))
        if f.endswith(".md")
    ]
    for f in files:
        process(f)
    json.dump(_dims, open(DIM_CACHE, "w"), indent=1)
