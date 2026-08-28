#!/usr/bin/env bash
# YouTube -> extrait decoupe -> R2 -> balise <video> dans le markdown.
#
# Automatise ce qui a ete fait a la main pour les 63 premieres videos.
#
# Usage:
#   ./tools/yt-to-r2.sh <url|id> <slug> [options]
#
#   --start MM:SS     debut de l'extrait (defaut: debut de la video)
#   --end   MM:SS     fin de l'extrait   (defaut: fin de la video)
#   --replace FICHIER remplace la facade yt-lite de cette video par la balise <video>
#   --dry-run         prepare tout localement, n'uploade pas
#
# Exemple:
#   ./tools/yt-to-r2.sh QKpcGQMin5M lascaux --start 1:12 --end 3:40 \
#       --replace all_collections/_posts/2025-11-01-histoire-chronologie.md
#
# Configuration (a mettre dans ton shell, ou dans tools/r2.env) :
#   export R2_ACCOUNT_ID=...        # Cloudflare > R2 > Manage API tokens
#   export R2_BUCKET=...            # nom du bucket
#   export AWS_ACCESS_KEY_ID=...    # cle R2 (S3-compatible)
#   export AWS_SECRET_ACCESS_KEY=...

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$REPO/tools/r2.env" ] && . "$REPO/tools/r2.env"

R2_PUBLIC_BASE="${R2_PUBLIC_BASE:-https://pub-c9b3a62a67a943bc875fe6a0cf9e9e98.r2.dev}"
POSTER_DIR="$REPO/assets/img/posters"
WORK="${TMPDIR:-/tmp}/yt-to-r2"

# ---------- arguments ----------
[ $# -ge 2 ] || { sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
INPUT="$1"; SLUG="$2"; shift 2
START=""; END=""; REPLACE=""; DRYRUN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --start)   START="$2"; shift 2 ;;
    --end)     END="$2";   shift 2 ;;
    --replace) REPLACE="$2"; shift 2 ;;
    --dry-run) DRYRUN=1; shift ;;
    *) echo "option inconnue : $1"; exit 1 ;;
  esac
done

# Accepte une URL complete ou un simple ID.
VID="$(printf '%s' "$INPUT" | sed -E 's|.*[?&]v=([A-Za-z0-9_-]{11}).*|\1|; s|.*/([A-Za-z0-9_-]{11})$|\1|')"
[ ${#VID} -eq 11 ] || { echo "ID YouTube introuvable dans : $INPUT"; exit 1; }

# yt-dlp le plus recent (une version perimee fait chuter YouTube en 360p).
YTDLP=""; YTDLP_V=""
for c in "$(brew --prefix yt-dlp 2>/dev/null)/bin/yt-dlp" "$(command -v yt-dlp || true)"; do
  [ -x "$c" ] || continue
  v="$($c --version 2>/dev/null)" || continue
  if [ -z "$YTDLP" ] || [ "$v" \> "$YTDLP_V" ]; then YTDLP="$c"; YTDLP_V="$v"; fi
done
[ -n "$YTDLP" ] || { echo "yt-dlp manquant : brew install yt-dlp"; exit 1; }

mkdir -p "$WORK" "$POSTER_DIR"
SRC="$WORK/$VID.mp4"

# ---------- 1. source ----------
# Reutilise la copie d'archive si elle existe, sinon telecharge.
ARCHIVED="$(find "$HOME/Documents/archive-chronologie/$VID" -name '*.mp4' 2>/dev/null | head -1 || true)"
if [ -n "$ARCHIVED" ]; then
  echo "1/5  source : archive locale"
  SRC="$ARCHIVED"
elif [ -f "$SRC" ]; then
  echo "1/5  source : deja telechargee ($SRC)"
else
  echo "1/5  telechargement ($YTDLP_V)"
  "$YTDLP" -f 'bv*[height<=1080]+ba/b[height<=1080]/b' --merge-output-format mp4 \
           -o "$SRC" --no-playlist --quiet --progress "https://www.youtube.com/watch?v=$VID"
fi

# ---------- 2. decoupe + optimisation web ----------
OUT="$WORK/$SLUG.mp4"
CUT=(); [ -n "$START" ] && CUT+=(-ss "$START"); [ -n "$END" ] && CUT+=(-to "$END")
echo "2/5  decoupe${START:+ de $START}${END:+ a $END} + reencodage web"
# -movflags +faststart : la lecture demarre avant la fin du telechargement.
# scale : plafonne a 1280 de large, hauteur paire imposee par libx264.
ffmpeg -hide_banner -loglevel error -y "${CUT[@]}" -i "$SRC" \
  -vf "scale='min(1280,iw)':-2" \
  -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart "$OUT"

# ---------- 3. poster ----------
POSTER="$POSTER_DIR/$SLUG.webp"
echo "3/5  poster -> assets/img/posters/$SLUG.webp"
DUR="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT" | cut -d. -f1)"
ffmpeg -hide_banner -loglevel error -y -ss "$(( DUR / 3 ))" -i "$OUT" \
  -frames:v 1 -vf "scale='min(1280,iw)':-2" -quality 82 "$POSTER"

SIZE="$(du -h "$OUT" | cut -f1)"

# ---------- 4. upload R2 ----------
if [ "$DRYRUN" = "1" ]; then
  echo "4/5  --dry-run : pas d'upload (fichier pret : $OUT, $SIZE)"
else
  : "${R2_ACCOUNT_ID:?manque R2_ACCOUNT_ID - voir entete du script}"
  : "${R2_BUCKET:?manque R2_BUCKET}"
  echo "4/5  upload vers R2 ($SIZE)"
  aws s3 cp "$OUT" "s3://$R2_BUCKET/$SLUG.mp4" \
    --endpoint-url "https://$R2_ACCOUNT_ID.r2.cloudflarestorage.com" \
    --content-type video/mp4 --only-show-errors
fi

# ---------- 5. balise ----------
TAG="<p style=\"text-align:center\">
  <video poster=\"/assets/img/posters/$SLUG.webp\" controls preload=\"none\" width=\"640\" height=\"360\" src=\"$R2_PUBLIC_BASE/$SLUG.mp4\"></video>
</p>"

if [ -n "$REPLACE" ]; then
  echo "5/5  remplacement de la facade yt-lite dans $(basename "$REPLACE")"
  VID="$VID" TAG="$TAG" python3 - "$REPLACE" <<'PY'
import os, re, sys
path = sys.argv[1]
vid, tag = os.environ["VID"], os.environ["TAG"]
src = open(path, encoding="utf-8").read()
# Le <p> entier qui porte la facade yt-lite de cette video.
pat = re.compile(r'<p[^>]*>\s*<a class="yt-lite"[^>]*data-id="' + re.escape(vid) + r'".*?</a>\s*</p>', re.S)
new, n = pat.subn(tag, src)
if n == 0:
    sys.exit(f"  aucune facade trouvee pour {vid} — balise a coller a la main")
open(path, "w", encoding="utf-8").write(new)
print(f"  {n} occurrence(s) remplacee(s)")
PY
else
  echo "5/5  balise a coller :"
  echo
  echo "$TAG"
fi
