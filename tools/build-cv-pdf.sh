#!/usr/bin/env bash
# Rebuilds download/Felix-Lambert-CV-{EN,FR}.pdf from the /cv/ pages.
# The extra _config_pdf.yml is the only build that prints the phone number.
set -euo pipefail
cd "$(dirname "$0")/.."
export LC_ALL=${LC_ALL:-C.UTF-8}
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT
bundle exec jekyll build --quiet --config _config.yml,_config_pdf.yml -d "$build_dir"
node tools/print-cv.js "$build_dir" download
