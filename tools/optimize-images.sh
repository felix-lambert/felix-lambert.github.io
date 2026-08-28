#!/usr/bin/env bash
# Convertit les images de assets/img en WebP (max 1600px de large).
# Idempotent : ne reconvertit que si le source est plus récent que le .webp.
# Ne remplace la référence que si le WebP est réellement plus léger.
set -euo pipefail

DIR="${1:-assets/img}"
MAX_W=1600
Q=82

command -v cwebp    >/dev/null || { echo "cwebp manquant (brew install webp)"; exit 1; }
command -v gif2webp >/dev/null || { echo "gif2webp manquant (brew install webp)"; exit 1; }
command -v magick   >/dev/null || { echo "magick manquant (brew install imagemagick)"; exit 1; }

before=0; after=0; converted=0; skipped=0

shopt -s nullglob nocaseglob
for src in "$DIR"/*.{png,jpg,jpeg,gif}; do
  [ -f "$src" ] || continue
  out="${src%.*}.webp"

  if [ -f "$out" ] && [ "$out" -nt "$src" ]; then
    skipped=$((skipped+1)); continue
  fi

  if [[ "$(printf %s "$src" | tr A-Z a-z)" == *.gif ]] && [ "$(magick identify "$src" 2>/dev/null | wc -l)" -gt 1 ]; then
    # GIF animé : gif2webp préserve l'animation (pas de redimensionnement)
    gif2webp -q "$Q" -m 6 "$src" -o "$out" >/dev/null 2>&1 || { echo "  ! échec $src"; continue; }
  else
    w=$(magick identify -format '%w' "$src[0]" 2>/dev/null || echo 0)
    if [ "$w" -gt "$MAX_W" ]; then
      magick "$src[0]" -resize "${MAX_W}x>" -strip png:- 2>/dev/null | cwebp -q "$Q" -m 6 -quiet -o "$out" -- - 
    else
      cwebp -q "$Q" -m 6 -quiet -o "$out" -- "$src"
    fi
  fi

  [ -f "$out" ] || continue
  bs=$(stat -f%z "$src"); as=$(stat -f%z "$out")

  if [ "$as" -ge "$bs" ]; then
    rm -f "$out"           # WebP plus lourd : on garde l'original
    echo "  = $(basename "$src") : webp plus lourd, conservé tel quel"
    continue
  fi

  before=$((before+bs)); after=$((after+as)); converted=$((converted+1))
  printf "  ✓ %-34s %6.1f Mo -> %5.2f Mo\n" "$(basename "$src")" \
    "$(echo "$bs/1048576" | bc -l)" "$(echo "$as/1048576" | bc -l)"
done

echo
printf "%d converties, %d déjà à jour\n" "$converted" "$skipped"
printf "Total : %.1f Mo -> %.1f Mo\n" \
  "$(echo "$before/1048576" | bc -l)" "$(echo "$after/1048576" | bc -l)"
