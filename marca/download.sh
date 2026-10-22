#!/bin/bash
# Descarrega as fontes, o guia de marca e os efeitos sonoros para marca/fontes/ e marca/sons/.
# Não vão para o GitHub (o repositório é público e as licenças não o permitem).
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")" && pwd)"
DIR="$RAIZ/fontes"; SONS="$RAIZ/sons"
mkdir -p "$DIR" "$SONS"

baixar() {  # baixar <id do Drive> <nome do ficheiro>
  [ -s "$DIR/$2" ] && return 0
  curl -fsSL "https://drive.google.com/uc?export=download&id=$1" -o "$DIR/$2"
}
baixar_gf() {  # baixar_gf <caminho em fonts.gstatic.com> <nome> — fontes gratuitas (Google Fonts, OFL)
  [ -s "$DIR/$2" ] || curl -fsSL "https://fonts.gstatic.com/s/$1" -o "$DIR/$2"
}

# Guia de marca (Drive da Rute)
baixar 1FRKX9vR695PuDo9nqCaw0m8ZooVhMOsq guia-de-marca.png

# Montserrat: a letra sans serif dos vídeos (vlog e yapping), escolhida pela Rute. Gratuita (Google Fonts, OFL).
baixar_gf montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtr6Ew-.ttf Montserrat-Regular.ttf
baixar_gf montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCtZ6Ew-.ttf Montserrat-Medium.ttf
baixar_gf montserrat/v31/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCu170w-.ttf Montserrat-SemiBold.ttf

# Sloop (yapping: títulos e destaques; vlog: algumas palavras das legendas). A Rute já enviou o ficheiro
# (Sloop Script Regular, .ttf), mas ainda não está no Drive. Quando estiver, acrescentar aqui: baixar <id> Sloop.ttf
# Substituta só para pré-visualizações: Mrs Saint Delafield.
baixar_gf mrssaintdelafield/v14/v6-IGZDIOVXH9xtmTZfRagunqBw5WC62cK4.ttf MrsSaintDelafield.ttf

# Efeitos sonoros. Ficam já aparados, prontos a usar.
baixar_som() {  # baixar_som <id do Drive> <nome> <início s> <duração s>
  [ -s "$SONS/$2.wav" ] && return 0
  curl -fsSL "https://drive.google.com/uc?export=download&id=$1" -o "$SONS/$2-original.mp3"
  ffmpeg -loglevel error -y -ss "$3" -t "$4" -i "$SONS/$2-original.mp3" \
    -af "afade=t=out:st=$(awk "BEGIN{print $4-0.05}"):d=0.05" "$SONS/$2.wav"
}
baixar_som 1DS2agJOrVxUrOT6hdK41ga7RuypEO7zM clique  1.53 0.20   # um clique de rato
baixar_som 1K-dY1BRNXJVKc-1xY2vvOwtfI1fW-q65 teclado 0.36 6.40   # teclas a bater; cortar à medida do texto

# Instala no sistema para o ffmpeg (legendas) também as encontrar
mkdir -p ~/.local/share/fonts && cp "$DIR"/*.ttf ~/.local/share/fonts/ 2>/dev/null || true
cp "$DIR"/*.otf ~/.local/share/fonts/ 2>/dev/null || true
command -v fc-cache >/dev/null && fc-cache -f >/dev/null || true
