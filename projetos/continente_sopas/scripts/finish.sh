#!/bin/bash
# Textos (HyperFrames) + legendas + som do fecho em silêncio + loudness -14 LUFS → preview.mp4
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
python3 scripts/build_texts.py > /dev/null
(cd animations/slot_1 && npx --yes hyperframes@0.8.164 render --format webm -o render.webm 2>&1 | grep -E "rendered in|rror")
F=$(python3 -c "import json;print(json.load(open('animations/slot_1/timings.json'))['fecho'])")
ffmpeg -v error -y -i cuts.mkv -c:v libvpx-vp9 -i animations/slot_1/render.webm -filter_complex \
 "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:format=auto:eof_action=pass[v1];[v1]subtitles=legendas.ass:fontsdir=$E/animations/fonts[outv]" \
 -map "[outv]" -map 0:a -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a pcm_s16le prenorm.mkv
M=$(ffmpeg -i prenorm.mkv -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i prenorm.mkv -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a aac -b:a 192k -movflags +faststart preview.mp4
ffmpeg -i preview.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -show_entries format=duration -of csv=p=0 preview.mp4
