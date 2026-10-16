# Recuperar o projeto "continente_sopas" numa sessão nova

1. `bash setup.sh`
2. Descarregar o original do Drive para `videos/continente_sopas.mov`
   (pasta https://drive.google.com/drive/folders/14CyzzZlJ5oNdxDZO9Rt39-5g0xQPhKSY).
3. Copiar esta pasta para `videos/edit/` e voltar a transcrever (`transcribe.py ... --language pt`).
4. Criar `videos/edit/animations/slot_1` (`npx hyperframes init . --example blank`), copiar `animations/fonts` para lá.
5. `render.py edl.json -o cuts.mp4 --no-subtitles --no-loudnorm` e depois `scripts/finish.sh`.

Os vídeos e a transcrição não ficam no git (são privados); aqui só ficam as decisões de edição.
