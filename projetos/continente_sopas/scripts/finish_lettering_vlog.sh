#!/bin/bash
# Montagem 4K60 com a sopa + lettering "vlog" da marca (animations/slot_3) + som de teclado no título + -14 LUFS
# → montagem_4k60_lettering.mp4
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
R="$(cd "$E/../.." && pwd)"
BASE=montagem_4k60_hq_com_sopa.mp4
# teclado: só enquanto o título se escreve (0,3 → 1,014 s), ~20 dB abaixo da voz (-35,6 LUFS → -37 LUFS; voz -17)
ffmpeg -v error -y -i "$BASE" -i "$R/marca/sons/teclado.wav" -filter_complex \
 "[1:a]atrim=0:0.714,afade=t=out:st=0.664:d=0.05,volume=-1.5dB,aresample=48000,aformat=channel_layouts=stereo,adelay=300|300[k];\
  [0:a][k]amix=inputs=2:normalize=0:duration=first[a]" -map "[a]" -c:a pcm_s16le prenorm.wav
M=$(ffmpeg -i prenorm.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i prenorm.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" final_audio.wav
ffmpeg -v error -y -i "$BASE" -c:v libvpx-vp9 -i animations/slot_3/render.webm -i final_audio.wav -filter_complex \
 "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset medium -crf 16 -r 60 -c:a aac -b:a 256k -tag:v avc1 -movflags +faststart montagem_4k60_lettering.mp4
ffmpeg -ss 8.9 -t 7.3 -i montagem_4k60_lettering.mp4 -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -count_frames -show_entries stream=codec_type,width,height,nb_read_frames,duration -of compact montagem_4k60_lettering.mp4
