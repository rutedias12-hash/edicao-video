# Edição de vídeo — video-use + HyperFrames

Fluxo de edição automática em português:

1. **video-use** (a "tesoura") — transcreve o vídeo e corta silêncios, hesitações e repetições, ficando com a melhor versão de cada frase.
2. **HyperFrames** (o "designer") — adiciona animações e visualizações ligadas ao que está a ser dito.

Antes de editar, o Claude mostra sempre o plano e espera pela tua aprovação.

## Como usar
1. Abre uma sessão do Claude Code com este repositório.
2. Garante que a variável `ELEVENLABS_API_KEY` está definida no ambiente (nunca no repositório).
3. Se as ferramentas ainda não estiverem instaladas: `bash setup.sh`.
4. Envia o vídeo e pede: *"edita este vídeo"*.

## O que vai para o GitHub
Só as instruções (`CLAUDE.md`) e o script de instalação (`setup.sh`).
Vídeos, áudio, ferramentas descarregadas e a chave ficam de fora (ver `.gitignore`).
