#!/bin/bash
# Versão sem textos nem legendas: só o corte + loudness -14 LUFS → preview.mp4
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
M=$(ffmpeg -i cuts.mkv -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i cuts.mkv -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a aac -b:a 192k -movflags +faststart preview.mp4
ffmpeg -i preview.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -show_entries format=duration -of csv=p=0 preview.mp4
