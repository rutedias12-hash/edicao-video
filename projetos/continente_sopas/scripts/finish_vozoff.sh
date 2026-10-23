#!/bin/bash
# Montagem com voz off: cortes (edl_vozoff.json) + vozes 81/82 (condensadas) + lettering (animations/slot_3) + teclado no título
# + -14 LUFS. Uso: bash scripts/finish_vozoff.sh preview   → vozoff_preview.mp4 (1080×1920, 30 fps, rápido)
#                  bash scripts/finish_vozoff.sh 4k        → vozoff_4k60.mp4 (2160×3840, 60 fps)
# Antes: cut.py (EDL=edl_vozoff.json, H/FPS) e o render do slot_3 com a mesma ESCALA.
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
R="$(cd "$E/../.." && pwd)"
if [ "${1:-preview}" = 4k ]; then CUTS=cuts_3840_edl_vozoff.mkv; OV=animations/slot_3/render.webm; OUT=vozoff_4k60.mp4; FPS=60; CRF=16
else CUTS=cuts_edl_vozoff.mkv; OV=animations/slot_3/render_1080.webm; OUT=vozoff_preview.mp4; FPS=30; CRF=20; fi
T81=$(python3 -c "import json;print(json.load(open('vozoff_tempos.json'))['voz81'])")
T82=$(python3 -c "import json;print(json.load(open('vozoff_tempos.json'))['voz82'])")
KD=$(python3 -c "import json;t=json.load(open('animations/slot_3/timings.json'));print(round(t['fim_escrita']-t['inicio_escrita'],3))")   # duração da escrita do título
ms(){ python3 -c "print(int(round($1*1000)))"; }
# vozes +8,2 dB (-25,3 → -17,1 LUFS, o nível da parte da sopa); teclado ~20 dB abaixo da voz, só enquanto o título se escreve
ffmpeg -v error -y -i "$CUTS" -i "$R/videos/voz/voz81.wav" -i "$R/videos/voz/voz82.wav" -i "$R/marca/sons/teclado.wav" -filter_complex \
 "[1:a]volume=8.2dB,adelay=$(ms $T81)|$(ms $T81)[v1];[2:a]volume=8.2dB,adelay=$(ms $T82)|$(ms $T82)[v2];\
  [3:a]atrim=0:$KD,afade=t=out:st=$(python3 -c "print($KD-0.05)"):d=0.05,volume=-1.5dB,aresample=48000,aformat=channel_layouts=stereo,adelay=300|300[k];\
  [0:a][v1][v2][k]amix=inputs=4:normalize=0:duration=first[a]" -map "[a]" -c:a pcm_s16le prenorm_vozoff.wav
M=$(ffmpeg -i prenorm_vozoff.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i prenorm_vozoff.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" audio_vozoff.wav
ffmpeg -v error -y -i "$CUTS" -c:v libvpx-vp9 -i "$OV" -i audio_vozoff.wav -filter_complex \
 "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset medium -crf $CRF -r $FPS -c:a aac -b:a 256k -tag:v avc1 -movflags +faststart "$OUT"
ffmpeg -i "$OUT" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -count_frames -show_entries stream=codec_type,width,height,nb_read_frames,duration -of compact "$OUT"
