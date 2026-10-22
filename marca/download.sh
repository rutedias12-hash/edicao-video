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

# Instala no sistema para o ffmpeg (legendas) também as encontrar
mkdir -p ~/.local/share/fonts && cp "$DIR"/*.otf "$DIR"/*.ttf ~/.local/share/fonts/
command -v fc-cache >/dev/null && fc-cache -f >/dev/null || true
