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

## Sessão 2 — 2026-10-17
**Pedidos:** introdução com zoom out; explicação a começar logo aos 3-4 s sobre as atividades; remover todo o lettering e o cartão final.
**Feito:**
- Gancho (6297 1,18 s): zoompan 2,2x → 1x centrado na cara, ease-in-out cúbico em 3,3 s; início 6 centésimos mais tarde (frames desfocados de ela a sentar-se); voz acompanha (sem dessincronizar).
- Nova ordem: gancho 0–3,42 → atividades 5×1,2 s (descansar, ler, trabalhar, relaxar, brincar) com "nós personalizamos… desde o comprimento, cor, arrumação" (3,52–8,70) → arcas 2x com a voz das arcas (9,52–12,90) → chaise → encosto → stop-motion → sofá-cama 2 s. Total 20,6 s. Sai o plano dela a falar (6302).
- Sem sobreposições (overlays.json vazio); slots HyperFrames ficam guardados mas fora do vídeo.
- Música: começa aos 16,34 s da faixa para a subida (29,24 s) cair quando acaba a fala (12,90 s); baixa -13 dB durante toda a fala. Voz 15-16 dB acima da música. -17,9 LUFS.
- v5: zoom out mais rápido (1,8 s); removido o clip 6301 (a rir no encosto); atividades 4×1,35 s; arcas (imagem 8,82 s, voz 8,87 s) logo a seguir a "…arrumação"; música desloca-se para a subida cair aos 12,25 s. Total 19,8 s.
- Fecho falado: nada utilizável nos clips (ver conversa). Sugerido gravar uma frase curta.
- v6: nota de voz de fecho (fecho/fecho.m4a, 37 s, várias versões). Usada a 3.ª versão (15,86–20,78) "Chaise longue redonda, encosto de cabeça ajustável e transforma-se de sofá a cama sem esforço." (mais fluida; "de sofá a cama") partida em 2 entre "redonda," e "encosto", e "Por isso, claro que aconselhamos." (22,62–23,98). Rejeitadas: 1.ª (pausa longa antes de "sem esforço"), 2.ª (incompleta), "a nossa resposta é?" (pergunta).
  Imagem acertada às palavras: chaise 12,42 / encosto 14,02 / stop-motion 15,34 ("transforma-se") / cama 16,76 ("cama"). Fecho 18,55. Total 21,0 s.
  Nota de voz +10,5 dB (chaise -4, resto +1, "aconselhamos" +4), highpass 80 Hz, limitador. Todas as falas ~-17/-18 dB RMS. Música abaixa durante toda a fala (0–20,06); subida da faixa no sofá-cama (offset 12,48). -17,3 LUFS, pico -3,8 dBFS.
- v7 (20,0 s): sem silêncios. A fala da gravação entra logo após as arcas (12,36), "encosto…" aos 13,36 e "Por isso, claro que aconselhamos." aos 17,50. Imagens reacertadas: chaise 12,30 / encosto 13,40 / stop-motion 14,72 / cama 16,14.
  Final em ecrã dividido (17,40–20,0): 3 faixas 1080x640 com os planos horizontais originais (ler 6300 4,0 s, relaxar 6306 6,0 s, trabalhar 6305 8,0 s), a entrar de cima para baixo de 0,4 em 0,4 s (esq., dir., esq.), deslize de 0,45 s ease-out cúbico, por cima do sofá-cama.
