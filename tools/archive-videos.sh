#!/usr/bin/env bash
# Archive locale (privée) des vidéos YouTube embarquées dans les posts.
#
# But : garder une copie de préservation. Si une vidéo disparaît de YouTube,
# le contenu n'est pas perdu et tu décides à ce moment-là quoi en faire.
# Cette archive n'est PAS destinée à être publiée telle quelle.
#
# Usage:  ./tools/archive-videos.sh [dossier_destination] [post.md ...]
# Défaut: ~/Documents/archive-chronologie, tous les posts
#
# Le script est idempotent : relancé, il ne retélécharge pas ce qu'il a déjà.

set -uo pipefail

DEST="${1:-$HOME/Documents/archive-chronologie}"
shift || true
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Posts à scanner : ceux passés en argument, sinon tous.
if [ "$#" -gt 0 ]; then SOURCES=("$@"); else SOURCES=("$REPO/all_collections/_posts/"); fi

# Résout le yt-dlp le plus récent. Un vieux script pip dans /opt/homebrew/bin peut
# masquer celui de Homebrew ; une version périmée fait chuter YouTube en 360p.
YTDLP=""; YTDLP_V=""
for cand in "$(brew --prefix yt-dlp 2>/dev/null)/bin/yt-dlp" "$(command -v yt-dlp || true)"; do
  [ -x "$cand" ] || continue
  v="$($cand --version 2>/dev/null)" || continue
  if [ -z "$YTDLP" ] || [ "$v" \> "$YTDLP_V" ]; then YTDLP="$cand"; YTDLP_V="$v"; fi
done
[ -n "$YTDLP" ] || { echo "yt-dlp manquant : brew install yt-dlp"; exit 1; }
echo "yt-dlp $YTDLP_V  ($YTDLP)"

# Une version de plus de ~3 mois perd l'accès aux formats HD de YouTube.
if [ "$YTDLP_V" \< "$(date -v-3m +%Y.%m.%d 2>/dev/null || date +%Y.%m.%d)" ]; then
  echo "ATTENTION : yt-dlp est ancien, YouTube risque de ne servir que du 360p."
  echo "            Mets à jour avec : brew upgrade yt-dlp"
fi

mkdir -p "$DEST"
echo "Destination : $DEST"

# Extrait les IDs (11 caractères) de tous les posts, dédupliqués.
grep -rhoE 'youtube(-nocookie)?\.com/(embed/|watch\?v=)[A-Za-z0-9_-]{11}' \
     "${SOURCES[@]}" \
  | grep -oE '[A-Za-z0-9_-]{11}$' \
  | sort -u > "$DEST/ids.txt"

TOTAL=$(wc -l < "$DEST/ids.txt" | tr -d ' ')
echo "$TOTAL vidéos uniques référencées."
echo

# --download-archive : mémorise ce qui est déjà pris, rend le script relançable.
# -f : plafonne à 1080p pour limiter la taille sans perdre en lisibilité.
# --write-info-json / --write-thumbnail : garde titre, chaîne, date, description,
#   ce qui permet d'afficher un fallback propre si la vidéo meurt.
"$YTDLP" \
  --download-archive "$DEST/downloaded.txt" \
  --batch-file "$DEST/ids.txt" \
  --paths "$DEST" \
  --output '%(id)s/%(title).150B [%(id)s].%(ext)s' \
  --format 'bv*[height<=1080]+ba/b[height<=1080]/b' \
  --merge-output-format mp4 \
  --write-info-json \
  --write-thumbnail \
  --write-subs --write-auto-subs --sub-langs 'fr.*,en.*' --sub-format 'srt/vtt/best' \
  --embed-metadata \
  --ignore-errors \
  --no-abort-on-error \
  --retries 5 \
  --sleep-requests 2 \
  --sleep-interval 2 --max-sleep-interval 6 \
  --extractor-retries 5 \
  --progress

echo
DONE=$(wc -l < "$DEST/downloaded.txt" 2>/dev/null | tr -d ' ' || echo 0)
echo "Archivées : $DONE / $TOTAL"
[ "$DONE" -lt "$TOTAL" ] && echo "Les manquantes sont indisponibles (privées/supprimées) — relance pour réessayer."
du -sh "$DEST" 2>/dev/null
