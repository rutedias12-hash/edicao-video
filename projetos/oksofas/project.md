# OK Sofás — Pub "6 meses depois"

## Sessão 1 — 2026-10-16

**Estratégia:** anúncio vertical 9:16 (1080x1920, 30 fps), ~26 s. Gancho falado → montagem rápida de usos →
personalização + encosto ajustável → arcas → stop-motion sofá→cama → cartão final com logótipo. Sem legendas, sem música
(a cliente trata da música). Áudio só com as vozes escolhidas, -14 LUFS.

**Decisões:**
- Gancho: IMG_6297 (mais rápida, sem pausa entre "meses" e "ainda"); 6296 fica de reserva.
- Planos horizontais filmados de cima rodados 90° para encher o 9:16 (2.ª sala rodada ao contrário para ela ficar de cabeça para cima).
- Personalização: 6302 "nós personalizamos…sofá," + "desde o comprimento, cor, arrumação" (falso começo dos 7,3 s cortado); 2.ª parte por cima do encosto (6309 4,6 s).
- Arcas: 1.ª versão da 6303 (mais curta), voz 0,06–3,44 sobre a imagem da arca aberta (1,95 s).
- Stop-motion: 6310–6313 são o mesmo estado → só 4 passos (6310, 6314, 6315, 6316).
- Paleta: creme #F4EFE8, areia #CDBBA3, castanho #2B2420, vermelho da marca #D6342A (tirado do logótipo). DM Serif Display + Inter.
- Animações HyperFrames: slot_1 "6 MESES DEPOIS", slot_2 palavras da montagem, slots 3–5 etiquetas (chaise, encosto, arcas), slot_6 "De sofá… a cama.", slot_7 cartão final.

**Ficheiros:** build.py (base/final), overlays.json, final.mp4.
**Pendente:** música (cliente), feedback da pré-visualização.

## Sessão 1 (cont.) — iterações
- Volume baixado: -14 → -17 LUFS (pedido da cliente).
- Mais rápido: arcas a 2x (6303 0,8 s em diante: vê-se a mão a abrir a arca); stop-motion 0,4 s por passo; total 23,8 s.
  slot_6 re-temporizado (cortes 0/0,4/0,8/1,2; "…a cama." aos 1,2 s; 2,7 s). Cartão final passa a começar aos 21,28 s.
- Erro corrigido: com aceleração, a duração tem de ser cortada à entrada (-t antes de -i).
- Música: "Voja - Great Escape - No Lead Vocals.wav" (136 BPM). Começa aos 25,82 s da faixa para a subida (29,24 s)
  cair no 1.º corte da montagem (3,42 s). -8 dB sem voz, -13 dB extra sob as vozes (rampas 0,25 s), fade-out 1,5 s.
  Vozes igualadas (+2 dB gancho, +4 dB arcas). Voz ~12-16 dB acima da música. Mistura -17,5 LUFS, pico -2,2 dBFS.
