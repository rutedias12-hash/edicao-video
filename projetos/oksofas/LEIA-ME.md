# OK Sofás — "6 meses depois" (receita do projeto)

Aqui fica tudo o que é preciso para refazer o anúncio, sem os vídeos (estão no Drive).

Para retomar numa sessão nova:
1. `bash setup.sh`
2. Descarregar o Drive para `videos/oksofas/` (os .MOV) e a música para `videos/oksofas/edit/assets/music.wav`
3. Copiar esta pasta para `videos/oksofas/edit/` (build.py, overlays.json, project.md, assets/, animations/)
4. Em cada `animations/slot_N/`: `npx --yes hyperframes render . --format webm --fps 30 -o render.webm`
5. `python videos/oksofas/edit/build.py base` e depois `python videos/oksofas/edit/build.py final`
   (4K: `npx --yes hyperframes render animations/texto --format webm --fps 30 --resolution portrait-4k -o animations/texto/render_4k.webm`, depois `OKS_4K=1` antes dos dois comandos)

Estado e decisões: ver `project.md`.
