# Projeto de edição de vídeo (video-use + HyperFrames)

Idioma de trabalho: **português (Portugal)** — conversa, transcrição (`--language pt`), textos no ecrã.
Explicar sempre tudo de forma simples, sem jargão.

## Ferramentas
- Se `tools/video-use` não existir, correr primeiro `bash setup.sh` (instala tudo).
- video-use: `tools/video-use` (skill `video-use`; ler `tools/video-use/SKILL.md`). Chave em `tools/video-use/.env`.
- HyperFrames: skills `hyperframes`, `talking-head-recut`, etc. em `~/.claude/skills/`; usar `npx --yes hyperframes ...`.

## Marca e estilo (aplicar SEMPRE, sem a Rute ter de pedir)
- Antes de qualquer plano, ler `marca/MARCA.md` (cores, fontes, animações), `marca/EDICAO.md` (preferências de edição)
  e `marca/FORMATOS.md` (receita de cada formato: vlog ou yapping; perguntar qual, se não for óbvio).
- Todas as animações HyperFrames usam `marca/marca.css`. Nada de cores ou fontes fora da marca.
- Se `marca/fontes/` não existir, correr `bash marca/download.sh`.
- No fim de cada projeto, acrescentar a `marca/EDICAO.md` ("Aprendido nos projetos") o que a Rute corrigiu
  ou pediu, e fazer commit, para não voltar a ser preciso pedir.

## Onde ficam os vídeos
- Originais em `videos/`; resultados em `videos/edit/` (nada disto vai para o git).

## Fluxo para cada vídeo enviado
1. **Inventário** (video-use): `ffprobe`, `transcribe.py <vídeo> --language pt`, `pack_transcripts.py`.
2. **Plano de cortes**: listar silêncios, hesitações ("hum", "é...", "pronto"), falsos começos e repetições;
   em cada frase repetida escolher a melhor versão e dizer porquê.
3. **Plano de animações** (HyperFrames): para cada momento-chave, o que aparece no ecrã, quando
   (ligado à palavra dita) e com que estilo (sempre o da marca: `marca/MARCA.md`).
4. **MOSTRAR O PLANO E ESPERAR APROVAÇÃO.** Não cortar nem renderizar nada antes do "sim".
5. Executar: `edl.json` → `render.py` (cortes) → slots HyperFrames em `edit/animations/slot_<id>/`
   (em paralelo) → composição final → auto-verificação (`timeline_view` nos cortes, loudness).
6. Mostrar a pré-visualização, iterar com o feedback, render final. Registar em `edit/project.md`.
