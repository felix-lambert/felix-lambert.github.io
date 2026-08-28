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

command -v yt-dlp >/dev/null || { echo "yt-dlp manquant : brew install yt-dlp"; exit 1; }

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
yt-dlp \
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
  --sleep-requests 1 \
  --progress

echo
DONE=$(wc -l < "$DEST/downloaded.txt" 2>/dev/null | tr -d ' ' || echo 0)
echo "Archivées : $DONE / $TOTAL"
[ "$DONE" -lt "$TOTAL" ] && echo "Les manquantes sont indisponibles (privées/supprimées) — relance pour réessayer."
du -sh "$DEST" 2>/dev/null
