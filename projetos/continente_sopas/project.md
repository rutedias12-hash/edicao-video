# Projeto: continente_sopas

## Fonte
- `videos/continente_sopas.mov` — 49m24s, 2160x3840 (vertical 9:16), HEVC 30fps, áudio AAC estéreo, 7.7 GB.
- Origem: Google Drive (pasta partilhada pela Rute), ficheiro "continente sopas (em falta).mov".
- Transcrição: `transcripts/continente_sopas.json` (Scribe, pt) → `takes_packed.md` (311 frases).

## Briefing
- Formato: vlog para Instagram (Reel), vertical.
- **Parceria paga com o Continente.** Produto a comunicar: **Sopas Receita do Chef Continente**
  (no vídeo: sopa de abóbora, camarão e coentros). Destacar sempre que possível.
- Por confirmar: duração, legendas, exemplos de estilo, significado de "(em falta)".

## Momentos-chave do produto
- 219–232s: "descobri a melhor sopa de sempre no Continente… a receita do chef, sopa de abóbora, camarão e coentros" (embalagem na mão, bem visível 226–232).
- 252.8–256s: "É simplesmente maravilhosa, sopa de abóbora, camarão e coentros" (embalagem visível).
- 691–694s: "Felizmente temos sopa".
- 2133–2191s: bebé come a sopa ("é sopa, não pode ser sempre doce", "a sopa é boa").
- 2820–2826s: Clara "Posso ficar com mais sopa?".

## Referências (edit/downloads/refs/)
- DW7GdH7ESnD — **a própria Rute**, série "Vlog Noite — A realidade de uma família de 4" (90s, ~56 cortes):
  título em letra manuscrita dourada + subtítulo serifado em maiúsculas; etiquetas pequenas centradas "18:30 / banho da Maria Clara".
- DXw1lxKCudx — Ellie Frazier, day in my life (50s): hora grande + legenda curta minúscula, cortes rápidos.
- DdNDSjXRfHw — Chantelle Suarez, uni vlog (23s): título serifado, hora + atividade pequenas.
- Pedido: estilo **clean**, sem abusar de efeitos. Narrativa: vai fazer o jantar → caos → opta pela sopa.

## Sessão 1 — 2026-10-16
**Estratégia:** novo episódio da série "Vlog Noite": 17:50 ir fazer o jantar → caos (bebé com dentes) → "plano B" → Sopa Receita do Chef Continente → jantar do Henrique → Clara "posso ficar com mais sopa?" → fecho "jantar salvo".
**Duração:** pedido ≤45 s → 21 cortes, 43.9 s (versão de 80 s guardada em `edl_80s.json`).
**Decisões:** frase do produto = 1.ª versão (3:41–3:50, sem o falso começo "tip–"); estilo clean igual ao Reel DW7GdH7ESnD
(Pinyon Script dourado #f3e3a3 + Cormorant + Space Mono/Poppins); cartão do produto com fundo escuro translúcido no topo
(armários brancos tiram contraste); legendas Poppins 54 px, discretas, a ~71 % da altura.
**Ficheiros:** `edl.json` → `cuts.mp4`; textos `animations/slot_1/render.webm` (HyperFrames, alfa); `legendas.ass`; `preview.mp4` (-14.2 LUFS, pico -0.6 dBFS).
**Por confirmar:** horas exatas dos jantares (etiquetas sem hora); falas sobrepostas da Clara (47:00) legendadas de forma simplificada.

### Iteração 2 (feedback da Rute)
- Abertura: plano trocado para ela a **entrar** em casa (17.0–18.2 s).
- Cortes mais rápidos: 32 cortes, ~1,4 s por plano; saíram "Corta pra trás este plano", "A sopa é boa", 1 plano de batatas e 1 de ovos.
- Acrescentado: banho (banhoca + banheira + toalha), pijama, deitar o Henrique (quarto vermelho + "shhh"), Clara ao colo,
  sopa servida nas taças (42:30) e fecho sobre o **grande plano da embalagem Cozinha Continente Receita do Chef** (43:00), com o som em silêncio (o Paulo fala de outra coisa).
- A chegada da Clara **não existe neste ficheiro** (provável parte "em falta").
- Volume aprovado. Scripts: `scripts/build_texts.py` (legendas + textos a partir do EDL) e `scripts/finish.sh` (montagem final).

### Iteração 3
- Abertura com 3 planos a entrar em casa (12.0, 18.6, 67.4 s).
- B-roll por cima da fala (novo `scripts/cut.py`, campo "cutaways" no EDL): batatas na frase "loucura";
  descascar/cortar/tabuleiros por cima de "como hoje a Clara tem treino na ginástica e chega um bocadinho tarde" (15:53);
  ovos na frigideira por cima de "vou fazer uns ovos".
- Banho com 3 planos (banheira, toalha de pé, bebé na toalha na cama); deitar: plano a ENTRAR no quarto (37:36) em vez do "shhh".
- Saíram "Este dia nunca mais acaba" e "Espera, filho". 29 cortes, 44,6 s.
