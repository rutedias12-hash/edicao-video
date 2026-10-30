# Preferências de edição da Rute

Este ficheiro cresce com o tempo. No fim de cada projeto o Claude acrescenta aqui o que a Rute
corrigiu ou elogiou, para não ter de ser pedido outra vez. Em caso de conflito, a regra mais recente ganha.

## Regras base
- Formato habitual: vertical 1080×1920 (Instagram/Reels), salvo indicação em contrário.
- Cortes: remover "hum", "é…", falsos começos e repetições. Ritmo conforme o formato:
  vlog calmo (a voz respira ~0,2–0,3 s entre frases); yapping vivo (sem tempos mortos).
- Legendas, título de abertura e animações: dependem do formato (vlog ou yapping), ver `marca/FORMATOS.md`.
- Volume final: -14 LUFS.
- Música: **só se a Rute pedir** (confirmado); nesse caso, volume baixo por baixo da voz.

## Aprendido nos projetos
<!-- Formato: AAAA-MM-DD — projeto — o que mudou e porquê -->
2026-10-22 — configuração — yapping: legendas palavra a palavra; efeitos sonoros sim (só yapping); música só se pedida.
2026-10-22 — configuração — vlog: clipes de 0,5 a 2 s (nunca 3 s), cada corte muda de perspetiva.
2026-10-22 — configuração — a Rute detestou o lettering editorial (La Luxes + manuscrita). Agora: só sans serif (Hind Siliguri), sem sombras; títulos em máquina de escrever com cursor e som de teclado; resto só aparece.
2026-10-22 — configuração — letra dos vídeos passa a Proxima Nova (Montserrat até haver ficheiros) com espaçamento entre letras apertado.
2026-10-22 — configuração — guia novo (Sloop + Proxima Nova). Sloop só no yapping; vlog só "Sistema".
  Títulos do vlog: curtos, enormes, à esquerda, linhas juntas, em Burgundy (Champagne se não se ler).
  Legendas do vlog: palavra a palavra, com palavras-chave em Champagne ou em Sloop.
2026-10-22 — configuração — Montserrat definitiva (vlog e yapping), letras e linhas mais apertadas.
  Horas/atividade sempre Winter White (tom claro). Legendas: base sempre clara, nunca castanho; tons escuros só nos destaques.
2026-10-22 — configuração — legendas do vlog: uma só palavra de cada vez, desaparece antes da seguinte.
2026-10-22 — configuração — vlog: título só nos primeiros 3 s; hora/atividade ao centro do ecrã; legenda logo abaixo.
  O layout anterior ficou guardado como "legenda informativa" (marca/modelos/), só quando a Rute pedir.
2026-10-22 — configuração — legendas coladas por baixo da hora/atividade (sem espaço extra).
2026-10-22 — configuração — todo o texto dentro das margens de segurança dos Reels (220 cima, 420 baixo, 120 direita, 60 esquerda).
2026-10-22 — configuração — Sloop Script verdadeira ligada (Drive); destaques em Sloop a ~2,2×.
2026-10-24 — traços tóxicos — yapping: título em Montserrat maiúsculas com a palavra principal em Sloop (sem negrito) sobreposta;
  destaques sempre em Sloop sem negrito; números grandes (Montserrat Black, Burgundy) atrás da Rute durante cada ponto;
  títulos de secção em Montserrat Regular; o vídeo começa com zoom in no gancho.
2026-10-30 — look para o evento (vlog C&A) — a Rute quer POUCOS silêncios também no vlog, MAS sem a voz ficar robótica: manter as pausas naturais
  até ~0,28 s dentro das frases (cortar só as longas, deixando ~0,18 s) e ~0,18 s entre frases. Música de ambiente MUITO baixa (bem abaixo da voz).
  Sem fotografias no meio dos vídeos. Som ambiente das imagens fora (soava a ruído); voz limpa com RNNoise (ffmpeg arnndn, mix=0.8 para não soar metálico) + afftdn leve.
  Cor NATURAL com um pouco de contraste e nitidez (sem filtro quente). Quando a voz é de um clipe em que ela aparece a falar,
  a imagem tem de ser desse mesmo instante (nada de outras tentativas por cima: parece dessincronizado).
  Gosta de: subtítulo curto por baixo do título ("ajudem-me a escolher!"), aviso no ecrã com valores (BUDGET 150 € + 💸),
  ecrã dividido com as duas opções + pergunta em texto grande ("1 ou 2?"), speed ramp curto em transições com ecrã escuro
  (sem acelerar planos dela), b-roll rápido (~1,5×, 6–7 s) e texto de campanha do início do b-roll até ao fim.
  Horas no ecrã: confirmar com a Rute (os metadados dos clipes não deram a hora local certa).
  Música: só a que ela enviar, como ambiente MUITO baixa (~-46 dB + sidechain forte). Stories: cortes de 8–11 s do vídeo final.
