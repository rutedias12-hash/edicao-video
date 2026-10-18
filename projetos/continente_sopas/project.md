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

### Iteração 4
- **Sincronização:** o som original chega ~0,10 s depois da imagem (microfone sem fios; medido na porta a fechar: imagem 15,1 s, som 15,2 s).
  `scripts/cut.py` reescrito: lê o som 0,10 s à frente, planos com frames inteiros e som com amostras exatas (sem desvio).
- "Espera, por favor, espera." com o bebé a chorar (9:29) logo a seguir à explicação da ginástica.
- Banho: corredor com o Henrique ao colo (por cima de "Vamos lá tomar banhoca") → porta a fechar → a sair da casa de banho
  com o bebé de toalha (18:51, aproximado com "crop").
- Sopa servida: plano a deitar a sopa da embalagem na taça (42:22).
- Saíram "a partir das seis da tarde isso é loucura" e "É sopa,". 27 cortes, 44,3 s.

### Iteração 5 (base = versão 3, a pedido da Rute)
- Sem textos nem legendas (`scripts/finish_clean.sh`). Mantida a correção de sincronização de 0,10 s.
- 42 planos em 44,9 s (~1,1 s cada), alternando ângulos: entrada (frente / lado perto / frente com bebé; corredor removido),
  batatas (frente, cozinha de costas com o bebé na cadeira, cortar, tabuleiros, lava-loiça), ovos (de costas a partir, frigideira, bater),
  embalagem em grande plano por cima de "sopa de abóbora, camarão e coentros", deitar (corredor, embalar, berço), Clara (2 ângulos), sopa (a deitar + taças).
- Banho: corredor a entrar com o bebé → do quarto, a porta fecha (18:46) → abre e sai com ele de toalha (18:51), sem aproximar.
- Mantido "Espera, por favor, espera." com o bebé a chorar.

### Iteração 6
- Fala da ginástica contínua e completa: "como hoje | a Clara tem treino na ginástica e chega um bocadinho tarde, eu tenho de ir adiantando esta parte." (pausa de 0,6 s removida), com 7 planos de B-roll.
- "Espera, filho. Espera." (9:46) com o bebé a choramingar por baixo (camada de som de 9:26, +2 dB) no início do plano.
- Ovos: último plano trocado pela Rute junto ao Henrique na cadeira de refeição (33:08).
- Jantar em família: sem conversa — 3 planos tranquilos (46:02, 48:41, 48:54).
- Fecho: aproximação cinemática lenta na embalagem (zoom 1,0 → 1,22, ease in-out, sobre o 4K).
- 33 segmentos, 45,0 s. Sem textos/legendas.
- 6.1: removido 'flash' de 1 frame aos 11,5 s (último B-roll não cobria o último frame); corrigido em `cut.py` para todos os planos e verificado o vídeo inteiro.
- 6.2: removido o plano do jantar (46:02) em que a Rute caminha para a câmara. 32 segmentos, 44,1 s.

**FINAL (2026-10-16):** versão 6.2 aprovada pela Rute → `videos/edit/final.mp4` (44,1 s, 1080×1920, -14 LUFS). EDL final = `edl.json`.

## Sessão 2 — 2026-10-18
- Teaser ("sneak peek") no início: 8 planos × 0,3 s a 1,25× (som acelerado sem mudar o tom): banho (corredor), batatas,
  embalagem na mão, bebé na toalha, ovos, quarto vermelho, a deitar a sopa, embalagem em grande plano. Novo campo "speed" em `cut.py`.
- Total 46,5 s (passa o limite de 45 s pedido antes — perguntar à Rute). Final anterior guardado em `final_v6_44s.mp4`.
