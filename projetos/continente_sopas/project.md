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
- 7.1: teaser a 3× (cada plano mostra 0,9 s de ação em 0,3 s).
- 7.2 (corrigido): dessincronização causada pelo teaser — nos planos acelerados a imagem ficava com 0,17 s e o som 0,3 s
  (o fps era fixado antes de acelerar). `cut.py` agora acelera antes de fixar os 30 fps e **falha se imagem ≠ som** em qualquer plano.
- 8: textos (`scripts/build_titles.py` → `animations/slot_2`, `scripts/finish_titles.sh`):
  título "caos de fim de dia" (Inter Bold, Winter White #F5ECD2, à esquerda, typewriter + teclas reais recortadas do som de teclado da biblioteca),
  subtítulo "família de 4 em dia de atividades extracurriculares" (branco, escrita à mão + som de caneta sintetizado),
  corpo "17:50 às 20:30" centrado; textos iniciais até 4,1 s (o teaser só tem 2,4 s).
  Etiquetas hora + descrição por cena, centradas, Winter White, 40 px, sem animação. **Horas propostas, a confirmar** (só 17:50 é certa).
- 8.1: textos sem sombreado.

## Sessão 2 (cont.) — exportação final
- Textos e efeitos sonoros retirados a pedido da Rute (não gostou). Fica: teaser 3× + vídeo da versão 6.2, sem texto.
- **Exportação 4K**: `H=3840 python3 scripts/cut.py` + `scripts/export_4k.sh` → `videos/edit/final_4k.mp4` (2160×3840, 30 fps, H.264, 46,5 s, -14 LUFS, 136 MB).

## Sessão 3 — 2026-10-18 · versão editada pela Rute (lettering + SFX feitos por ela no CapCut)
- Ficheiro dela: `videos/rute_v2/sopaContinente.mov` (42,6 s, 4K, textos "colados" na imagem; som próprio no teaser).
- Pedido: tirar os planos de sopa do teaser. Trocados (imagem só): embalagem na mão → Henrique na cadeira (2:12);
  a deitar a sopa → Clara ao colo (40:46); embalagem em grande plano → abraço de pijama (20:59).
- Método (`edit/scripts/replace_teaser.py`): o vídeo dela coincide frame a frame com `final_4k.mp4`; textos dela recuperados
  por máscara de cor (magenta ≈ RGB 161,0,50) × molde das letras (frame 80) × "já escrito" (difere da imagem limpa) + brancos e cursor.
  Verificado: 27 frames revistos, resto do vídeo igual (só recompressão), som bit a bit idêntico.
  → `videos/rute_v2/sopaContinente_teaser.mp4`.
- Música "Genesis": ficheiro não fornecido — pendente.

## Sessão 4 — 2026-10-20 · correções sobre `rute_v3/continenteReels.mov` (versão da Rute, 42,6 s)
- Diagnóstico: imagem igual à versão anterior dela (teaser ainda com sopa); só o som da cena do jantar do Henrique mudou.
- `edit/scripts/fix_v3.py` → `rute_v3/continenteReels_corrigido.mp4`:
  1. Teaser: 3 planos de sopa trocados de novo (Henrique na cadeira, Clara ao colo, abraço de pijama), textos dela preservados.
  2. Jantar do Henrique (26,07–28,57 s): restos de sopa apagados dentro da taça (fica taça vazia; borda intacta), cliente não quer que se note a sopa.
  3. Choro (11,47 s): antes da voz, choro substituído por resmungo curto (8:02 do original); fim do choro por baixo do 1.º "Espera" subtraído;
     resmungo baixinho (9:24) na pausa. Bebé −14,6 → −23,7 dB; voz da Rute inalterada; resto do som igual (dif. −38 dB, só compressão).

## Sessão 4 (cont.) — plano do jantar do Henrique sem fala
- Marca não quer "não é doce". `edit/scripts/fix_v4.py` → `rute_v4/continenteReels_v4.mp4` (a partir de continenteReels_corrigido.mp4):
  frames 782–856 (26,07–28,57 s) trocados por 36:11,6–36:14,1 do original (Rute leva a colher ao Henrique e faz "ahh" sem som),
  imagem sem letras (a Rute acrescenta), taça limpa, som = ambiente do próprio plano (−54 dB, sem fala). Resto igual (verificado).
- Nota: `-shortest` no mux cortava 4 frames finais → removido de fix_v3/fix_v4.

## Sessão 5 — 2026-10-21 · "clipes travados"
- Causa: as exportações do CapCut da Rute mostram só ~20 imagens únicas/s (padrão 0,1,3,4,6,7…: salta 1 em cada 3 do nosso final_4k).
  Detalhe 4K completo → não é ficheiro reduzido; o salto acontece no projeto/exportação do CapCut. Reexportar a 60 fps (rute_v6/1018(1).mov) não resolve.
- As nossas correções (v3/v4) partiram dessa exportação → herdaram o salto (exceto planos substituídos por nós: teaser e Henrique, fluidos).
- Reconstrução a 30 fps possível (mapa de frames em rute_v7/: maioria dos planos ligada ao final_4k por desvio constante),
  mas há o plano P&B com aproximação (17,0–17,8 s) e planos estáticos que precisam de tratamento à parte. Pendente de decisão da Rute.
- Enviada a v4 a pedido dela.

## Sessão 5 (cont.) — versão limpa 4K a 30 fps reais (sem textos) com todas as correções → `edit/final_4k_v8.mp4` (46,3 s)
Feita a partir da fonte (cut.py H=3840 + export_4k.sh), não da exportação do CapCut — sem saltos de imagens (29 repetidos = planos parados).
- Teaser: planos de sopa → Henrique na cadeira (2:12), Clara ao colo (40:46), abraço de pijama (20:59).
- Choro → resmungos (`audio_layers` 8:02 a 0 dB e 9:24 a −6 dB); bebé −21…−27 dB vs voz −13…−16 dB.
- Jantar do Henrique → 36:11,6 sem fala; `bowl_clean` (novo em cut.py) apaga a sopa da taça.
- Correção geral: com o desfasamento de 0,10 s do som, os planos com fala cortavam o início das palavras e apanhavam a seguinte
  ("malta", "fi-", "tio") → planos de fala recuados 0,10 s (imagem e som juntos) e limites à volta de "malta" acertados. Verificado: 0 palavras cortadas.
- Plano "a deitar a sopa": som trocado por ambiente da cozinha sem fala (havia "Quem é o…" de fundo).
- Transcrição final verificada: sem "doce".

## Sessão 6 — 2026-10-22 · MONTAGEM SEM VOZ (a marca não gostou da versão falada)
- `edl_montagem.json` (cut.py com `EDL=edl_montagem.json`), 30 planos de ~1 s, 31,2 s, todos `mute` → `edit/montagem_4k_sem_som.mp4` (4K, 30 fps, sem faixa de som).
- Ordem pedida pela Rute: chegada · cozinha caótica · jantar do Henrique (ovos, Henrique à mesa, colher "ahh"; taças limpas) · banho · pijama ·
  deitar (com "shhh") · a Clara chega · jantar com a sopa (sopa a sair da embalagem, taças, mesa) · fecho (embalagem com zoom 1,0→1,22).
- Fora: tudo com fala, Henrique a comer sopa, embalagem na mão (ela falava).

## Sessão 6 (cont.) — montagem com os CLIPES ORIGINAIS do iPhone (4K, 60 fps) → `edit/montagem_4k60_hq_sem_som.mp4` (31,2 s, 1872 frames)
- Pasta Drive da Rute: 58 clipes IMG_6555…IMG_6638 (4K HEVC ~60 fps). O vídeo longo = estes clipes por ordem (desvio crescente até ~0,9 s).
- Disco não chegava (~30 GB): clipes descarregados um a um; `scripts/hq_extract.py` extrai só os pedaços usados (+1 s margem) e acerta cada plano
  ao frame contra o vídeo longo (erro 0,1–0,6); clipe grande apagado. Pedaços em `videos/hq_pedacos/` (+ hq_map.json, duracoes.json).
- `scripts/build_hq_edl.py` → `edl_montagem_hq.json`; render `EDL=edl_montagem_hq.json H=3840 FPS=60 cut.py` (cut.py: FPS configurável; silêncio para planos sem som).
- Verificado: 0 repetidos nos planos com movimento; os repetidos estão só nos planos escuros (quarto vermelho) — o iPhone grava menos imagens com pouca luz. Taças limpas.
