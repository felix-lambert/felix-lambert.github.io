#!/usr/bin/env bash
# Génère une vignette WebP (poster) pour chaque vidéo distante référencée dans les posts.
# Idempotent : ne régénère pas un poster déjà présent.
set -uo pipefail
OUT=assets/img/posters
mkdir -p "$OUT"

grep -rhoE 'https://[^"]+\.mp4' all_collections/_posts/*.md | sort -u > /tmp/vid-urls.txt
echo "$(wc -l < /tmp/vid-urls.txt) vidéos distinctes"

ok=0; fail=0
while read -r url; do
  name=$(basename "$url" .mp4)
  dst="$OUT/$name.webp"
  [ -f "$dst" ] && continue
  if ffmpeg -y -loglevel error -ss 1 -i "$url" -frames:v 1 -vf "scale=480:-2" -q:v 58 "$dst" >/dev/null 2>&1 \
     && [ -s "$dst" ]; then
    ok=$((ok+1))
  else
    # certaines vidéos font moins d'1s : on retente à t=0
    if ffmpeg -y -loglevel error -i "$url" -frames:v 1 -vf "scale=480:-2" -q:v 58 "$dst" >/dev/null 2>&1 && [ -s "$dst" ]; then
      ok=$((ok+1))
    else
      rm -f "$dst"; fail=$((fail+1)); echo "  ! échec: $name"
    fi
  fi
done < /tmp/vid-urls.txt
echo "posters générés: $ok, échecs: $fail, total présents: $(ls "$OUT" | wc -l)"
