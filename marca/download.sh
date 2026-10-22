#!/bin/bash
# Descarrega as fontes e o guia de marca do Google Drive para marca/fontes/.
# Não vão para o GitHub (o repositório é público e as licenças das fontes não o permitem).
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)/fontes"
mkdir -p "$DIR"

baixar() {  # baixar <id do Drive> <nome do ficheiro>
  [ -s "$DIR/$2" ] && return 0
  curl -fsSL "https://drive.google.com/uc?export=download&id=$1" -o "$DIR/$2"
}

baixar 1COyifFCltS3P1d0ZsZ9sB59SKDDfJXAY guia-de-marca.png
baixar 18wyDQH5_7d-hSt3mufFEmHfI1SI1Mg1N LaLuxes.otf
baixar 19MQf7rf055naXSAOq0rj-C4Bg4uBIEg3 NewIconScript.otf
baixar 12q7uqaoTBakZanK3CSsH3tWC4Sai2yMe NewIconScript-Licenca.txt
baixar 1XHX_bzvOlmjjThkTVbkCvmTLvjZ1B9lj HindSiliguri-Light.ttf
baixar 1LBUTdHgx306PsFVkgXss1a-SSo9OMcuH HindSiliguri-Regular.ttf
baixar 1mZELJL3HV-pgjuAKRRtGprTCRJ5W-ciq HindSiliguri-Medium.ttf
baixar 1yZxvg7EBntzLShJvM9jIzEYapbehav64 HindSiliguri-SemiBold.ttf
baixar 1ObpUbNA0PCRg0g-v_uamU9c4JnGIZViO HindSiliguri-Bold.ttf

# Proxima Nova (letra dos vídeos). Fonte paga: só funciona quando a Rute puser os ficheiros no Drive.
# Quando houver IDs, acrescentar aqui: baixar <id> ProximaNova-Regular.otf / -Medium.otf / -Semibold.otf
# Substituta enquanto não houver: Montserrat (gratuita, Google Fonts, licença OFL).
baixar_gf() { [ -s "$DIR/$2" ] || curl -fsSL "https://fonts.gstatic.com/s/montserrat/v31/$1" -o "$DIR/$2"; }
baixar_gf JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtr6Ew-.ttf Montserrat-Regular.ttf
baixar_gf JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtZ6Ew-.ttf Montserrat-Medium.ttf
baixar_gf JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCu170w-.ttf Montserrat-SemiBold.ttf

# Efeitos sonoros (yapping). Ficam já aparados, prontos a usar.
SONS="$(cd "$(dirname "$0")" && pwd)/sons"
mkdir -p "$SONS"
baixar_som() {  # baixar_som <id do Drive> <nome> <início s> <duração s>
  [ -s "$SONS/$2.wav" ] && return 0
  curl -fsSL "https://drive.google.com/uc?export=download&id=$1" -o "$SONS/$2-original.mp3"
  ffmpeg -loglevel error -y -ss "$3" -t "$4" -i "$SONS/$2-original.mp3" \
    -af "afade=t=out:st=$(awk "BEGIN{print $4-0.05}"):d=0.05" "$SONS/$2.wav"
}
baixar_som 1DS2agJOrVxUrOT6hdK41ga7RuypEO7zM clique  1.53 0.20   # um clique de rato
baixar_som 1K-dY1BRNXJVKc-1xY2vvOwtfI1fW-q65 teclado 0.36 6.40   # teclas a bater; cortar à medida do texto

# Instala no sistema para o ffmpeg (legendas) também as encontrar
mkdir -p ~/.local/share/fonts && cp "$DIR"/*.otf "$DIR"/*.ttf ~/.local/share/fonts/
command -v fc-cache >/dev/null && fc-cache -f >/dev/null || true
