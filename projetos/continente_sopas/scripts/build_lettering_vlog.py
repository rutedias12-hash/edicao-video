"""Lettering "vlog" da marca (marca/FORMATOS.md) para a montagem 4K60 com o bloco da sopa.
Gera animations/slot_3/index.html (HyperFrames, 2160×3840, fundo transparente) a partir de marca/marca.css.
- Título "fim / de / dia": Montserrat SemiBold 470 px, uma palavra por linha, à esquerda, máquina de escrever (14 letras/s)
  com cursor; só 0–2,9 s. Cor: Cherry Burgundy por escolha da Rute neste vídeo (mesmo sem passar o teste de contraste).
- Destaque "chef" (Sloop) também em Burgundy, por escolha da Rute; os outros destaques em Champagne.
- Hora + atividade: ao centro, Winter White, só aparecem/desaparecem.
- Legendas da voz (só bloco da sopa): uma palavra de cada vez, coladas por baixo da hora; destaques em Champagne
  (o burgundy/espresso não passam o teste), alternando "cor" (SemiBold) e "sloop".
Uso: python3 scripts/build_lettering_vlog.py
"""
import html, json, shutil
from pathlib import Path

E = Path(__file__).resolve().parents[1]
R = E.parents[1]
OUT = E/'animations/slot_3'
(OUT/'fontes').mkdir(parents=True, exist_ok=True)
for f in (R/'marca/fontes').glob('*.ttf'):
    shutil.copy(f, OUT/'fontes'/f.name)
shutil.copy(R/'marca/marca.css', OUT/'marca.css')

DUR = 38.5
TITULO, T0, LPS, FIM_TITULO = ['fim', 'de', 'dia'], 0.3, 14, 2.9   # uma palavra por linha (pedido da Rute)
HORAS = [  # (início, fim, hora, atividade) — o fim é recalculado: cada uma fica até aparecer a seguinte (a última até ao fim)
    (2.9, 4.9, '17:50', 'tentar preparar o jantar'),
    (8.9, 11.46, '18:10', 'plano b'),
    (16.2, 18.0, '18:30', 'jantar do Henrique (omelete + banana esmagada)'),
    (20.2, 22.3, '18:50', 'banho do Henrique'),
    (26.7, 28.5, '19:30', 'deitar o bebé'),
    (30.4, 32.1, '19:45', 'Clarita chega de rastos'),
    (32.1, 34.2, '19:50', 'ainda bem que tinha esta sopa'),
    (34.2, 36.2, '20:00', 'jantar em família'),
]
# (palavra, início em s na montagem, destaque) — tempos da transcrição do bloco (ElevenLabs)
LEG = [('eu', 9.00), ('descobri', 9.14), ('a', 9.44), ('melhor', 9.52, 'cor'), ('sopa', 10.04), ('de', 10.36),
       ('sempre', 10.48), ('no', 10.84), ('Continente', 10.98),
       ('é', 11.60), ('a', 11.64), ('receita', 11.72), ('do', 12.00), ('chef', 12.16, 'sloop-vermelho'),
       ('sopa', 12.62), ('de', 12.96), ('abóbora', 13.04), ('camarão', 13.66), ('e', 13.98), ('coentros', 14.08),
       ('é', 14.42), ('maravilhosa', 14.74, 'cor'),
       ('amamos', 15.60, 'sloop')]
LEG_FIM = 16.06
# pedido da Rute: a hora/atividade fica sempre no ecrã e só sai quando aparece a seguinte
HORAS = [(a, HORAS[k+1][0] if k+1 < len(HORAS) else DUR, h, r) for k, (a, b, h, r) in enumerate(HORAS)]

# ---- título: um elemento por letra (a quebra de linha conta como uma letra, como no marca/exemplo.html) ----
chars = []
for i, linha in enumerate(TITULO):
    if i: chars.append('<br>')
    chars += [html.escape(c) if c != ' ' else '&nbsp;' for c in linha]
fim_escrita = T0 + len(chars) / LPS
tit = ''.join(f'<span id="c{i}" class="ch">{c}</span>' if c != '<br>' else f'<br id="c{i}" class="ch">' for i, c in enumerate(chars))
tl = [f'tl.set("#c{i}", {{ display: "inline" }}, {T0 + (i+1)/LPS:.3f});' for i in range(len(chars))]
# cursor: fixo durante a escrita; depois pisca (0,5 s desligado / 0,5 s ligado) e some com o título
t = fim_escrita; on = False
while t < FIM_TITULO:
    tl.append(f'tl.set("#cursor", {{ opacity: {1 if on else 0} }}, {t:.3f});'); on = not on; t += 0.5

clips = [f'<div id="titulo" class="clip" data-start="0" data-duration="{FIM_TITULO}">{tit}<span id="cursor" class="cursor"></span></div>']
for k, (a, b, h, r) in enumerate(HORAS):
    clips.append(f'<div id="hora{k}" class="clip hora" data-start="{a:.3f}" data-duration="{b-a:.3f}">'
                 f'<div class="h">{h}</div><div class="r">{html.escape(r)}</div></div>')
for k, w in enumerate(LEG):
    nxt = LEG[k+1][1] if k+1 < len(LEG) else LEG_FIM
    fim = min(nxt, w[1] + 0.6) if k+1 < len(LEG) else LEG_FIM   # sai antes da seguinte; nas pausas fica no máx. 0,6 s
    d = w[2] if len(w) > 2 else ''
    inner = (f'<span class="dest-sloop" style="color:var(--burgundy)">{w[0]}</span>' if d == 'sloop-vermelho' else
             f'<span class="dest-sloop" style="color:var(--champagne)">{w[0]}</span>' if d == 'sloop' else
             f'<span class="dest-cor" style="color:var(--champagne)">{w[0]}</span>' if d == 'cor' else w[0])
    clips.append(f'<div id="w{k}" class="clip leg" data-start="{w[1]:.3f}" data-duration="{fim-w[1]:.3f}">{inner}</div>')

page = f'''<!doctype html>
<html lang="pt">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=2160, height=3840" />
    <title>Fim de dia — lettering vlog</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="marca.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 2160px; height: 3840px; overflow: hidden; background: transparent; }}
      #root {{ position: relative; width: 2160px; height: 3840px; overflow: hidden; }}
      /* palco em coordenadas 1080×1920 (as da marca), ampliado 2× para 4K */
      #palco {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform: scale(2); transform-origin: 0 0;
               font-family: var(--fonte-texto); color: var(--winter-white); }}
      .clip {{ position: absolute; }}
      #titulo {{ top: calc(var(--seg-topo) + 24px); left: 70px; right: var(--seg-dir); font-weight: 600; font-size: 470px;
                line-height: var(--lh-titulo-vlog); letter-spacing: var(--esp-titulo); color: var(--burgundy); white-space: nowrap; }}
      .ch {{ display: none; }}
      #titulo .cursor {{ width: .06em; height: .72em; vertical-align: -.02em; }}
      .hora {{ top: 880px; left: var(--seg-dir); right: var(--seg-dir); text-align: center; }}
      .hora .h {{ font-weight: 600; line-height: 1; font-size: var(--t-hora); letter-spacing: var(--esp-texto); }}
      .hora .r {{ font-weight: 600; line-height: 1.2; font-size: var(--t-rotulo); letter-spacing: var(--esp-rotulo); text-transform: uppercase; }}
      .leg {{ top: 968px; left: var(--seg-dir); right: var(--seg-dir); text-align: center; font-weight: 400;
              font-size: var(--t-legenda); line-height: var(--lh-texto); letter-spacing: var(--esp-texto); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="2160" data-height="3840">
      <div id="palco">
        {chr(10).join('        ' + c for c in clips).lstrip()}
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join('      ' + x for x in tl).lstrip()}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
(OUT/'index.html').write_text(page)
json.dump({'fim_escrita': round(fim_escrita, 3), 'inicio_escrita': T0}, open(OUT/'timings.json', 'w'))
print('slot_3 pronto · escrita do título', T0, '→', round(fim_escrita, 3), 's')
