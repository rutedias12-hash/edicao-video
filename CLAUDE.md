# Projeto de edição de vídeo (video-use + HyperFrames)

Idioma de trabalho: **português (Portugal)** — conversa, transcrição (`--language pt`), textos no ecrã.
Explicar sempre tudo de forma simples, sem jargão.

## Ferramentas
- Se `tools/video-use` não existir, correr primeiro `bash setup.sh` (instala tudo).
- video-use: `tools/video-use` (skill `video-use`; ler `tools/video-use/SKILL.md`). Chave em `tools/video-use/.env`.
- HyperFrames: skills `hyperframes`, `talking-head-recut`, etc. em `~/.claude/skills/`; usar `npx --yes hyperframes ...`.

## Onde ficam os vídeos
- Originais em `videos/`; resultados em `videos/edit/` (nada disto vai para o git).

## Fluxo para cada vídeo enviado
1. **Inventário** (video-use): `ffprobe`, `transcribe.py <vídeo> --language pt`, `pack_transcripts.py`.
2. **Plano de cortes**: listar silêncios, hesitações ("hum", "é...", "pronto"), falsos começos e repetições;
   em cada frase repetida escolher a melhor versão e dizer porquê.
3. **Plano de animações** (HyperFrames): para cada momento-chave, o que aparece no ecrã, quando
   (ligado à palavra dita) e com que estilo (paleta/tipo de letra propostos).
4. **MOSTRAR O PLANO E ESPERAR APROVAÇÃO.** Não cortar nem renderizar nada antes do "sim".
5. Executar: `edl.json` → `render.py` (cortes) → slots HyperFrames em `edit/animations/slot_<id>/`
   (em paralelo) → composição final → auto-verificação (`timeline_view` nos cortes, loudness).
6. Mostrar a pré-visualização, iterar com o feedback, render final. Registar em `edit/project.md`.
