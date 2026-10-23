"""Lettering "vlog" da marca (marca/FORMATOS.md) para a montagem com voz off (edl_vozoff.json).
Gera animations/slot_3/index.html (HyperFrames, fundo transparente) a partir de marca/marca.css.
ESCALA=1 → 1080×1920 (pré-visualização); ESCALA=2 → 2160×3840 (4K final). Tempos em vozoff_tempos.json.
- Título "tenho / de ser / sincera": Montserrat SemiBold 260 px, condensado (letras -0,09 em, linhas 0,68),
  à esquerda, Cherry Burgundy (escolha da Rute), máquina de escrever (14 letras/s) com cursor; só 0–2,9 s.
- Subtítulo "quando o caos ataca uma família de 4": Montserrat Medium 44 px, Winter White, por baixo do título;
  aparece quando o título acaba de se escrever e sai com ele.
- Hora + atividade: ao centro, Winter White; cada uma fica até aparecer a seguinte (pedido da Rute).
- Legendas da voz (voz off 81 e 82 + bloco da sopa): uma palavra de cada vez, coladas por baixo da hora; só neste vídeo
  mais pequenas, a negrito e mais apertadas (Montserrat Bold 34 px, -0,06 em; pedido da Rute); não aparecem
  enquanto o título está no ecrã. Destaques em Burgundy sempre que passam o teste de contraste no sítio da palavra
  (senão Champagne), alternando "cor" e "sloop"; "chef" sempre em Burgundy (escolha da Rute). A Sloop pode tocar na atividade.
Uso: ESCALA=1 python3 scripts/build_lettering_vlog.py
"""
import html, json, os, re, shutil
from pathlib import Path

E = Path(__file__).resolve().parents[1]
R = E.parents[1]
OUT = E/'animations/slot_3'
(OUT/'fontes').mkdir(parents=True, exist_ok=True)
for f in (R/'marca/fontes').glob('*.ttf'):
    shutil.copy(f, OUT/'fontes'/f.name)
shutil.copy(R/'marca/marca.css', OUT/'marca.css')

ESC = int(os.environ.get('ESCALA', '1'))
W, H = 1080*ESC, 1920*ESC
T = json.load(open(E/'vozoff_tempos.json')); S = T['secoes']
DUR = S['fim']
TITULO, T0, LPS, FIM_TITULO = ['tenho', 'de ser', 'sincera'], 0.3, 14, 2.9   # título novo (pedido da Rute): é o que ela diz nesse momento
T_TITULO = 260   # o maior tamanho em que "sincera" (+ cursor) cabe entre a margem esquerda e a coluna de ícones
SUBTITULO = 'quando o caos ataca uma família de 4'
HORAS = [  # (início, hora, atividade) — cada uma fica até aparecer a seguinte (a última até ao fim)
    (FIM_TITULO, '17:50', 'chegar a casa'),
    (S['cozinha'], '17:50', 'tentar preparar o jantar'),
    (S['sopa'], '18:10', 'plano b'),
    (S['jantar_henrique'], '18:30', 'jantar do Henrique (omelete + banana esmagada)'),
    (S['banho'], '18:50', 'banho do Henrique'),
    (S['deitar'], '19:30', 'deitar o bebé'),
    (S['clara'], '19:45', 'Clarita chega de rastos'),
    (S['sopa_taca'], '19:50', 'ainda bem que tinha esta sopa'),
    (S['mesa'], '20:00', 'jantar em família'),
]
HORAS = [(round(a, 3), round(HORAS[k+1][0] if k+1 < len(HORAS) else DUR, 3), h, r) for k, (a, h, r) in enumerate(HORAS)]
# atividades que ocupam 2 linhas (Montserrat SemiBold 28 px, maiúsculas, +0,04 em, largura útil 840 px): a legenda desce uma linha
from PIL import ImageFont
_f = ImageFont.truetype(str(R/'marca/fontes/Montserrat-SemiBold.ttf'), 28)
LINHAS = {r: 2 if _f.getlength(r.upper()) + 0.04*28*len(r) > 840 else 1 for _, _, _, r in HORAS}
def topo_legenda(t):   # colada por baixo da hora/atividade que está no ecrã
    for a, b, h, r in HORAS:
        if a <= t < b and LINHAS[r] == 2: return 968 + 34
    return 968

# ---- legendas: palavras com tempos (início, fim da fala) ----
PROPRIOS = {'henrique': 'Henrique', 'paulo': 'Paulo', 'clara': 'Clara', 'continente': 'Continente'}
CORRIGE = {'controle': 'controlo', 'raste': 'rastos'}
def limpa(t):
    w = re.sub(r'[.,?!…]', '', t).lower()
    return PROPRIOS.get(w, CORRIGE.get(w, w))
LEG = []   # (palavra, início, fim da fala, destaque)
def voz(n, inicio, destaques):
    P = json.load(open(E.parents[0]/f'voz/voz{n}_palavras.json')); dest = dict(destaques)
    for i, p in enumerate(P):
        w = limpa(p['texto'])
        if w == 'da' and i and limpa(P[i-1]['texto']) == 'rastos': w = 'a'   # "de rastos a casa"
        LEG.append([w, round(inicio + p['ini'], 3), round(inicio + p['fim'], 3), dest.pop(w, '')])
    LEG.append(None)   # fim do bloco de fala
voz('81', T['voz81'], [('controlo', 'sloop'), ('jantar', 'cor'), ('incomodado', 'sloop'), ('sozinha', 'cor'), ('ceder', 'sloop')])
SOPA = S['sopa'] + 0.1 - 9.00   # tempos do bloco da sopa medidos com o "Eu" aos 9,00 s
for w, t, *d in [('eu', 9.00), ('descobri', 9.14), ('a', 9.44), ('melhor', 9.52, 'cor'), ('sopa', 10.04), ('de', 10.36),
                 ('sempre', 10.48), ('no', 10.84), ('Continente', 10.98), ('é', 11.60), ('a', 11.64), ('receita', 11.72),
                 ('do', 12.00), ('chef', 12.16, 'sloop-vermelho'), ('sopa', 12.62), ('de', 12.96), ('abóbora', 13.04),
                 ('camarão', 13.66), ('e', 13.98), ('coentros', 14.08), ('é', 14.42), ('maravilhosa', 14.74, 'cor'),
                 ('amamos', 15.60, 'sloop')]:
    LEG.append([w, round(t + SOPA, 3), round(t + SOPA + 0.3, 3), d[0] if d else ''])
LEG[-1][2] = round(16.06 + SOPA, 3); LEG.append(None)
voz('82', T['voz82'], [('sacrificar', 'cor'), ('batalhas', 'sloop'), ('fogão', 'cor'), ('mão', 'sloop'), ('real', 'cor'), ('saboroso', 'sloop')])
for k in range(1, len(LEG)):   # palavras ditas "ao mesmo tempo" (ex.: "e eu"): cada uma fica pelo menos 0,07 s
    if LEG[k] and LEG[k-1] and LEG[k][1] < LEG[k-1][1] + 0.07:
        LEG[k][1] = round(LEG[k-1][1] + 0.07, 3)

# ---- título: um elemento por letra (a quebra de linha conta como uma letra, como no marca/exemplo.html) ----
chars = []
for i, linha in enumerate(TITULO):
    if i: chars.append('<br>')
    chars += [html.escape(c) if c != ' ' else '&nbsp;' for c in linha]
fim_escrita = T0 + len(chars) / LPS
TOPO_SUB = round(220 + 40 + (len(TITULO) - 1) * 0.68 * T_TITULO + 0.98 * T_TITULO + 24)
tit = ''.join(f'<span id="c{i}" class="ch">{c}</span>' if c != '<br>' else f'<br id="c{i}" class="ch">' for i, c in enumerate(chars))
tl = [f'tl.set("#c{i}", {{ display: "inline" }}, {T0 + (i+1)/LPS:.3f});' for i in range(len(chars))]
# cursor: fixo durante a escrita; depois pisca (0,5 s desligado / 0,5 s ligado) e some com o título
t = fim_escrita; on = False
while t < FIM_TITULO:
    tl.append(f'tl.set("#cursor", {{ opacity: {1 if on else 0} }}, {t:.3f});'); on = not on; t += 0.5

clips = [f'<div id="titulo" class="clip" data-start="0" data-duration="{FIM_TITULO}">{tit}<span id="cursor" class="cursor"></span></div>']
for k, (a, b, h, r) in enumerate(HORAS):
    clips.append(f'<div id="hora{k}" class="clip hora" data-start="{a:.3f}" data-duration="{round(b-a, 3):.3f}">'
                 f'<div class="h">{h}</div><div class="r">{html.escape(r)}</div></div>')
clips.append(f'<div id="subtitulo" class="clip" data-start="{fim_escrita:.3f}" data-duration="{FIM_TITULO - fim_escrita:.3f}">{html.escape(SUBTITULO)}</div>')
# ---- cor dos destaques: burgundy sempre que se lê (teste da marca: 3:1 contra as partes mais escuras do fundo,
#      20.º percentil, no sítio exato da palavra e em 3 momentos); senão Champagne. "chef" fica sempre burgundy.
import subprocess
import numpy as np
from PIL import ImageFont as _IF
_fc = _IF.truetype(str(R/'marca/fontes/Montserrat-Bold.ttf'), 34)
_fs = _IF.truetype(str(R/'marca/fontes/Sloop.ttf'), 112)   # 3,3 × 34 px
BASE = E/'cuts_edl_vozoff.mkv'
def _lum(c):
    c = np.asarray(c, float)/255; c = np.where(c <= .03928, c/12.92, ((c+.055)/1.055)**2.4)
    return .2126*c[..., 0] + .7152*c[..., 1] + .0722*c[..., 2]
def _frame(t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', str(BASE), '-frames:v', '1', '-vf', 'scale=1080:1920',
                        '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)
BURG = _lum([0x6F, 0x17, 0x2B])
def cor_destaque(word, d, topo, a, b):
    larg = (_fs if 'sloop' in d else _fc).getlength(word)
    x0, x1 = int(540 - larg/2), int(540 + larg/2)
    y0, y1 = (topo - 51, topo + 66) if 'sloop' in d else (topo, topo + 41)
    piores = [np.percentile(_lum(_frame(t)[y0:y1, x0:x1]), 20) for t in (a + 0.02, (a + b)/2, b - 0.02)]
    contraste = (max(piores) + .05) / (BURG + .05)          # fundo mais claro que o burgundy
    return ('burgundy' if contraste >= 3 else 'champagne'), round(contraste, 2)
CORES = {}
for k, w in enumerate(LEG):
    if w is None or w[1] < FIM_TITULO: continue
    nxt = LEG[k+1][1] if LEG[k+1] is not None else None
    fim = min(nxt, w[1] + 0.6) if nxt is not None else max(w[2], w[1] + 0.3)   # última palavra do bloco: até acabar de ser dita
    d = w[3]; topo = topo_legenda(w[1])
    if d == 'sloop-vermelho':
        cor = 'burgundy'
    elif d:
        cor, c = cor_destaque(w[0], d, topo, w[1], fim); CORES[w[0]] = (cor, c)
    if d:
        cls = 'dest-sloop' if 'sloop' in d else 'dest-cor'
        inner = f'<span class="{cls}" style="color:var(--{cor})">{w[0]}</span>'
    else:
        inner = html.escape(w[0])
    st = '' if topo == 968 else f' style="top:{topo}px"'
    ov = ' data-layout-allow-overlap' if 'sloop' in d else ''   # a Sloop pode tocar na atividade (pedido da Rute)
    clips.append(f'<div id="w{k}" class="clip leg"{st}{ov} data-start="{w[1]:.3f}" data-duration="{fim-w[1]:.3f}">{inner}</div>')
json.dump(CORES, open(OUT/'cores_destaques.json', 'w'), ensure_ascii=False, indent=0)
print('destaques:', ', '.join(f'{w} {c[0]} ({c[1]}:1)' for w, c in CORES.items()))

page = f'''<!doctype html>
<html lang="pt">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>Fim de dia — lettering vlog</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="marca.css" />
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: transparent; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; }}
      /* palco em coordenadas 1080×1920 (as da marca), ampliado {ESC}× */
      #palco {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform: scale({ESC}); transform-origin: 0 0;
               font-family: var(--fonte-texto); color: var(--winter-white); }}
      .clip {{ position: absolute; }}
      #titulo {{ top: calc(var(--seg-topo) + 40px); left: 70px; right: var(--seg-dir); font-weight: 600; font-size: {T_TITULO}px;
                line-height: .68; letter-spacing: -0.09em; color: var(--burgundy); white-space: nowrap; }}   /* mais condensado (pedido da Rute) */
      #subtitulo {{ top: {TOPO_SUB}px; left: 70px; right: var(--seg-dir); font-weight: 500; font-size: 44px; line-height: var(--lh-texto);
                   letter-spacing: var(--esp-texto); white-space: nowrap; }}
      .ch {{ display: none; }}
      #titulo .cursor {{ width: .06em; height: .72em; vertical-align: -.02em; }}
      .hora {{ top: 880px; left: var(--seg-dir); right: var(--seg-dir); text-align: center; }}
      .hora .h {{ font-weight: 600; line-height: 1; font-size: var(--t-hora); letter-spacing: var(--esp-texto); }}
      .hora .r {{ font-weight: 600; line-height: 1.2; font-size: var(--t-rotulo); letter-spacing: var(--esp-rotulo); text-transform: uppercase; }}
      .leg {{ top: 968px; left: var(--seg-dir); right: var(--seg-dir); text-align: center; font-weight: 700;
              font-size: 34px; line-height: var(--lh-texto); letter-spacing: -0.06em; }}   /* só neste vídeo: mais pequenas, bold, apertadas */
      .leg .dest-cor {{ font-weight: 700; }}
      .leg .dest-sloop {{ font-weight: 400; font-synthesis: none; }}   /* Sloop sem negrito (pedido da Rute) */
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
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
print(f'slot_3 pronto ({W}×{H}, {DUR:.2f} s) · escrita do título', T0, '→', round(fim_escrita, 3), 's · palavras', sum(1 for c in clips if 'class="clip leg"' in c))
