#!/usr/bin/env bash
# Renders the site animations in light and dark themes at 1920x1080 (hero: 1920x820), 24 fps,
# then writes web-encoded MP4s and final-frame JPEG posters to ../media/.
#
#   ./render_all.sh                      # every scene
#   ./render_all.sh Triage Forest      # only the named scenes
#
# Scenes run one at a time: parallel runs can collide on Manim's text cache.
# Requires Manim (requirements.txt), Cairo, Pango and ffmpeg.
set -euo pipefail
cd "$(dirname "$0")"
export LANG=C.UTF-8 LC_ALL=C.UTF-8

# scene:module:site-file
ALL=(
  "Flow:scenes:hero"
  "Committee:scenes:fig1"
  "TwoReaders:scenes:fig2"
  "Evidence:scenes:fig3"
  "Triage:scenes:fig4"
  "Forest:scenes:fig5"
  "App:scenes:fig6"
)

want() { [ $# -eq 0 ] && return 0; local s; for s in "${@:2}"; do [ "$s" = "$1" ] && return 0; done; return 1; }

for entry in "${ALL[@]}"; do
  IFS=: read -r scene module out <<< "$entry"
  if [ $# -gt 0 ] && ! want "$scene" "$@"; then continue; fi
  for theme in light dark; do
    hero=""; [ "$scene" = "Flow" ] && hero=1
    THEME=$theme HERO=$hero manim render "$module.py" "$scene" \
      --media_dir "out_$theme" -o "$scene.mp4" --disable_caching -v WARNING
    src=$(find "out_$theme/videos/$module" -name "$scene.mp4" | head -n 1)
    dest="../media/$out-$theme"
    ffmpeg -y -loglevel error -i "$src" -c:v libx264 -preset veryfast -crf 23 \
      -pix_fmt yuv420p -movflags +faststart -an "$dest.mp4"
    ffmpeg -y -loglevel error -sseof -0.5 -i "$dest.mp4" -frames:v 1 -q:v 2 "$dest.jpg"
    echo "wrote $dest.mp4 and $dest.jpg"
  done
done
