#!/bin/bash
# Exportação final 4K (2160×3840), sem textos: corte 4K + loudness -14 LUFS → final_4k.mp4
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
IN=cuts_3840.mkv
M=$(ffmpeg -i $IN -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i $IN -c:v copy -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ar 48000 -c:a aac -b:a 256k -movflags +faststart -tag:v avc1 final_4k.mp4
ffmpeg -i final_4k.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,duration,r_frame_rate -of compact final_4k.mp4
ls -la final_4k.mp4
