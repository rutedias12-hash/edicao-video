#!/bin/bash
# Instala video-use + HyperFrames. Seguro de correr várias vezes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TOOLS="$ROOT/tools"
VU="$TOOLS/video-use"
mkdir -p "$TOOLS" ~/.claude/skills

# 1. video-use (a "tesoura": transcrição + cortes)
if [ -d "$VU/.git" ]; then
  git -C "$VU" pull --ff-only -q || true
else
  git clone -q --depth 1 https://github.com/browser-use/video-use "$VU"
fi
pip install -q -e "$VU"
ln -sfn "$VU" ~/.claude/skills/video-use

# Chave ElevenLabs: vem da variável de ambiente, nunca do repositório
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  printf 'ELEVENLABS_API_KEY=%s\n' "$ELEVENLABS_API_KEY" > "$VU/.env"
  chmod 600 "$VU/.env"
else
  echo "aviso: ELEVENLABS_API_KEY não definida — a transcrição não vai funcionar" >&2
fi

# 2. HyperFrames (o "designer": animações).
# Corre dentro de tools/ para instalar as skills em ~/.claude/skills.
(cd "$TOOLS" && npx --yes hyperframes skills update talking-head-recut)
npx --yes hyperframes browser ensure

# 3. Marca: fontes e guia (do Google Drive, fora do git)
bash "$ROOT/marca/download.sh" || echo "aviso: não foi possível descarregar as fontes da marca" >&2

command -v ffmpeg >/dev/null || echo "aviso: ffmpeg não encontrado" >&2
echo "Pronto."
