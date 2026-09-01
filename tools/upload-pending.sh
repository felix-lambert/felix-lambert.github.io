#!/usr/bin/env bash
# Envoie sur R2 les .mp4 en attente dans _a-uploader-sur-r2, puis verifie.
#
# Usage:  ./tools/upload-pending.sh [--purge-mkv]
#         --purge-mkv  supprime aussi les anciens .mkv du bucket (destructif)
#
# Necessite tools/r2.env (voir tools/r2.env.example).

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$HOME/Documents/archive-chronologie/_a-uploader-sur-r2"
PUBLIC="${R2_PUBLIC_BASE:-https://pub-c9b3a62a67a943bc875fe6a0cf9e9e98.r2.dev}"

[ -f "$REPO/tools/r2.env" ] || { echo "manque tools/r2.env - copie tools/r2.env.example"; exit 1; }
. "$REPO/tools/r2.env"
: "${R2_ACCOUNT_ID:?R2_ACCOUNT_ID vide dans tools/r2.env}"
: "${R2_BUCKET:?R2_BUCKET vide dans tools/r2.env}"

EP="https://$R2_ACCOUNT_ID.r2.cloudflarestorage.com"
PURGE=0; [ "${1:-}" = "--purge-mkv" ] && PURGE=1

# ---------- upload ----------
for f in "$SRC"/*.mp4; do
  [ -e "$f" ] || { echo "rien a envoyer dans $SRC"; exit 0; }
  n="$(basename "$f")"
  echo "envoi  $n  ($(du -h "$f" | cut -f1))"
  aws s3 cp "$f" "s3://$R2_BUCKET/$n" --endpoint-url "$EP" \
      --content-type video/mp4 --only-show-errors
done

# ---------- verification ----------
echo
echo "verification des URL publiques :"
fail=0
for f in "$SRC"/*.mp4; do
  n="$(basename "$f")"
  code="$(curl -s -o /dev/null -w '%{http_code}' -I -m 25 "$PUBLIC/$n")"
  printf "  %-36s %s\n" "$n" "$code"
  [ "$code" = "200" ] || fail=1
done
[ "$fail" = "0" ] || { echo; echo "au moins une URL ne repond pas 200 - ne supprime rien pour l'instant"; exit 1; }

# ---------- anciens .mkv ----------
echo
MKV="$(aws s3 ls "s3://$R2_BUCKET/" --endpoint-url "$EP" | awk '{ $1=$2=$3=""; sub(/^ +/,""); print }' | grep '\.mkv$' || true)"
if [ -z "$MKV" ]; then
  echo "aucun .mkv restant dans le bucket"
elif [ "$PURGE" = "1" ]; then
  echo "suppression des .mkv :"
  printf '%s\n' "$MKV" | while IFS= read -r k; do
    [ -n "$k" ] || continue
    echo "  - $k"
    aws s3 rm "s3://$R2_BUCKET/$k" --endpoint-url "$EP" --only-show-errors
  done
else
  echo ".mkv encore presents (aucun n'est reference par le site) :"
  printf '%s\n' "$MKV" | sed 's/^/  /'
  echo "relance avec --purge-mkv pour les supprimer."
fi
