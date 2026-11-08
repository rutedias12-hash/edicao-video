#!/bin/bash
# Versão com a voz nova (áudio 85): cortes (edl_voz85.json) + voz 85 (A + B1..B4, voz85_tempos.json) + lettering (animations/slot_4)
# + teclado no título + -14 LUFS. Uso: bash scripts/finish_voz85.sh preview | 4k
set -euo pipefail
E="$(cd "$(dirname "$0")/.." && pwd)"; cd "$E"
R="$(cd "$E/../.." && pwd)"
if [ "${1:-preview}" = 4k ]; then CUTS=cuts_3840_edl_voz85.mkv; OV=animations/slot_4/render.webm; OUT=voz85_4k60.mp4; FPS=60; CRF=16
else CUTS=cuts_edl_voz85.mkv; OV=animations/slot_4/render_1080.webm; OUT=voz85_preview.mp4; FPS=30; CRF=23; fi
KD=$(python3 -c "import json;t=json.load(open('animations/slot_4/timings.json'));print(round(t['fim_escrita']-t['inicio_escrita'],3))")
IN=(-i "$CUTS"); F=""; L=""; k=1
while read nome t; do
  IN+=(-i "$R/videos/voz/$nome.wav"); ms=$(python3 -c "print(int(round($t*1000)))")
  F+="[$k:a]volume=8.2dB,adelay=$ms|$ms[v$k];"; L+="[v$k]"; k=$((k+1))
done < <(python3 -c "import json;[print(n,t) for n,t in json.load(open('voz85_tempos.json'))['vozes']]")
IN+=(-i "$R/marca/sons/teclado.wav")
F+="[$k:a]atrim=0:$KD,afade=t=out:st=$(python3 -c "print($KD-0.05)"):d=0.05,volume=-1.5dB,aresample=48000,aformat=channel_layouts=stereo,adelay=300|300[k];"
ffmpeg -v error -y "${IN[@]}" -filter_complex "$F[0:a]${L}[k]amix=inputs=$((k+1)):normalize=0:duration=first[a]" -map "[a]" -c:a pcm_s16le prenorm_voz85.wav
M=$(ffmpeg -i prenorm_voz85.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$M" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i prenorm_voz85.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" audio_voz85.wav
ffmpeg -v error -y -i "$CUTS" -c:v libvpx-vp9 -i "$OV" -i audio_voz85.wav -filter_complex \
 "[1:v]setpts=PTS-STARTPTS[ov];[0:v][ov]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]" \
 -map "[v]" -map 2:a -c:v libx264 -preset medium -crf $CRF -r $FPS -c:a aac -b:a 192k -tag:v avc1 -movflags +faststart "$OUT"
ffmpeg -i "$OUT" -vn -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffprobe -v error -count_frames -show_entries stream=codec_type,width,height,nb_read_frames,duration -of compact "$OUT"
