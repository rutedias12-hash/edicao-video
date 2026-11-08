"""Textos da versão com títulos (HyperFrames, animations/slot_2) + efeitos sonoros (sfx.wav).

- Título (typewriter + teclado), subtítulo (escrita à mão + papel) e corpo por cima do teaser.
- Etiquetas hora + descrição no início de cada cena (sem animação).
Cores: Pantone 11-0507 TCX "Winter White" ≈ #F5ECD2; branco puro #FFFFFF. Letra "de sistema": Inter (a mais próxima da SF do iPhone).
Uso: python3 scripts/build_titles.py
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

E = Path(__file__).resolve().parent.parent
SLOT = E/'animations/slot_2'
WINTER_WHITE = '#F5ECD2'
SR = 48000

TITLE = "caos de fim de dia"
SUB_LINES = ["família de 4 em dia de", "atividades extracurriculares"]
BODY = "17:50 às 20:30"
# Etiquetas por cena (primeiro plano de cada 'beat'). Horas a confirmar com a Rute.
SCENES = {
    'JANTAR':   ("17:50", "preparar o jantar"),
    'DECISAO':  ("18:05", "plano B"),
    'BANHO':    ("18:30", "banho do Henrique"),
    'PIJAMA':   ("18:45", "pijama"),
    'HENRIQUE': ("19:00", "jantar do Henrique"),
    'DEITAR':   ("19:30", "deitar o Henrique"),
    'CLARA':    ("19:45", "a Clara chegou"),
    'FAMILIA':  ("20:00", "jantar em família"),
}

edl = json.load(open(E/'edl.json'))
durs = json.load(open(E/'clips_graded/durs.json'))
offs = [sum(durs[:i]) for i in range(len(durs))]
total = sum(durs)
teaser_end = sum(d for r, d in zip(edl['ranges'], durs) if r['beat'] == 'TEASER')
first_speech = next(o for r, o in zip(edl['ranges'], offs) if r['beat'] == 'JANTAR')
text_end = first_speech - 0.1          # os textos do início ficam até antes da 1.ª fala

# ---------- tempos da animação de abertura ----------
T0, CPS = 0.15, 0.05                    # typewriter: 50 ms por letra
char_t = [T0 + k*CPS for k in range(len(TITLE))]
title_done = char_t[-1] + CPS
SUB0 = title_done + 0.1                 # subtítulo logo a seguir ao título
LINE_DUR = [0.75, 0.85]
sub_t = [SUB0, SUB0 + LINE_DUR[0]]
sub_done = sub_t[1] + LINE_DUR[1]
BODY_T = sub_done + 0.1

# ---------- etiquetas por cena ----------
labels, seen = [], set()
for i, r in enumerate(edl['ranges']):
    b = r['beat']
    if b in SCENES and b not in seen:
        seen.add(b)
        end_beat = max(offs[j]+durs[j] for j, x in enumerate(edl['ranges']) if x['beat'] == b)
        labels.append((offs[i], min(offs[i]+3.0, end_beat-0.05), *SCENES[b]))

# ---------- HTML ----------
spans = ''.join(f'<span id="c{k}" class="ch">{"&nbsp;" if ch == " " else ch}</span>' for k, ch in enumerate(TITLE))
sub_svg = ''.join(
    f'<g id="sl{k}" class="subline"><text x="0" y="{52 + k*54}" class="subtext">{t}</text></g>' for k, t in enumerate(SUB_LINES))
lab_html = '\n      '.join(
    f'<div id="lab{k}" class="clip lab" data-start="{a:.3f}" data-duration="{b-a:.3f}"><div class="t">{hh}</div><div class="d">{dd}</div></div>'
    for k, (a, b, hh, dd) in enumerate(labels))
js = [f'      tl.set("#c{k}", {{ opacity: 1 }}, {t:.3f});' for k, t in enumerate(char_t)]
for k, t in enumerate(sub_t):
    js.append(f'      tl.fromTo("#sl{k}", {{ clipPath: "inset(-20% 100% -20% 0%)" }}, {{ clipPath: "inset(-20% 0% -20% 0%)", duration: {LINE_DUR[k]}, ease: "none" }}, {t:.3f});')
    js.append(f'      tl.fromTo("#sl{k} text", {{ strokeDashoffset: 900, fillOpacity: 0 }}, {{ strokeDashoffset: 0, duration: {LINE_DUR[k]}, ease: "power1.out" }}, {t:.3f});')
    js.append(f'      tl.to("#sl{k} text", {{ fillOpacity: 1, duration: 0.25, ease: "power1.out" }}, {t+LINE_DUR[k]*0.55:.3f});')
js.append(f'      tl.set("#body-t", {{ opacity: 1 }}, {BODY_T:.3f});')
js.append(f'      tl.to("#intro-in", {{ opacity: 0, duration: 0.2, ease: "power1.in" }}, {text_end-0.2:.3f});')

html = f'''<!doctype html>
<html lang="pt">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Caos de fim de dia — textos</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Inter"; src: url("fonts/Inter-Bold.ttf"); font-weight: 700; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: transparent; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter"; font-weight: 700; }}
      .clip {{ position: absolute; left: 0; right: 0; }}
      .sh {{ }}  /* sem sombreado, a pedido da Rute */
      #intro {{ top: 0; bottom: 0; }}
      #intro-in {{ position: absolute; inset: 0; }}
      #title {{ position: absolute; left: 84px; top: 690px; width: 880px; font-size: 112px; line-height: 0.95; letter-spacing: -0.02em; color: {WINTER_WHITE}; text-align: left; }}
      .ch {{ opacity: 0; }}
      #sub {{ position: absolute; left: 84px; top: 940px; width: 960px; height: 130px; overflow: visible; }}
      .subtext {{ font-family: "Inter"; font-weight: 700; font-size: 50px; letter-spacing: -0.01em; fill: #FFFFFF; stroke: #FFFFFF; stroke-width: 1.4px; stroke-dasharray: 900; }}
      #body {{ position: absolute; left: 0; right: 0; top: 1110px; text-align: center; font-size: 44px; color: #FFFFFF; }}
      #body-t {{ opacity: 0; }}
      .lab {{ top: 1330px; display: flex; flex-direction: column; align-items: center; text-align: center; color: {WINTER_WHITE}; font-size: 40px; line-height: 1.1; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.3f}" data-width="1080" data-height="1920">
      <div id="intro" class="clip" data-start="0" data-duration="{text_end:.3f}">
        <div id="intro-in">
          <div id="title" class="sh">{spans}</div>
          <svg id="sub" viewBox="0 0 960 130">{sub_svg}</svg>
          <div id="body" class="sh"><span id="body-t">{BODY}</span></div>
        </div>
      </div>
      {lab_html.replace('class="clip lab"', 'class="clip lab sh"')}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
(SLOT/'index.html').write_text(html)

# ---------- efeitos sonoros (sintetizados) ----------
rng = np.random.default_rng(7)
n = int(total*SR) + SR
sfx = np.zeros(n)
def click(t, amp):  # tecla: estalido curto + "toc" grave
    L = int(0.045*SR); tt = np.arange(L)/SR
    noise = rng.standard_normal(L) * np.exp(-tt/0.006)
    noise = np.diff(np.concatenate([[0], noise]))            # puxar para agudos
    thock = np.sin(2*np.pi*(170+rng.uniform(-20, 20))*tt) * np.exp(-tt/0.012) * 0.5
    i = int(t*SR); sfx[i:i+L] += amp*(noise*0.6 + thock)
# teclas REAIS: recortadas de um som de teclado (biblioteca do HyperFrames/media-use), uma por letra
real = SLOT/'.media/audio/sfx/sfx_001.mp3'
keys = []
if real.exists():
    pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(real), '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                                       capture_output=True, check=True).stdout, np.int16).astype(float) / 32768
    env = np.convolve(np.abs(pcm), np.ones(96)/96, 'same')
    thr, i, L = env.max()*0.25, 0, int(0.06*SR)
    while i < len(env):
        if env[i] > thr:
            st = max(0, i-int(0.004*SR)); keys.append(pcm[st:st+L] * np.hanning(2*L)[L:] ** 0.3); i += int(0.07*SR)
        else: i += 1
    keys = [k/np.abs(k).max() for k in keys if len(k) == L]
print(f'teclas reais encontradas: {len(keys)}')
for k, t in enumerate(char_t):
    if keys:
        kk = keys[k % len(keys)] * (1.1 if TITLE[k] == ' ' else rng.uniform(0.75, 1.0))
        j = int(t*SR); sfx[j:j+len(kk)] += kk
    else:
        click(t, 1.15 if TITLE[k] == ' ' else rng.uniform(0.7, 1.0))
def scribble(t0, dur):  # caneta no papel: ruído agudo com traços (amplitude a pulsar)
    L = int(dur*SR); tt = np.arange(L)/SR
    noise = np.diff(np.concatenate([[0], rng.standard_normal(L)]))
    strokes = np.clip(np.sin(2*np.pi*6.5*tt + 1.8*np.sin(2*np.pi*1.7*tt)), 0, None)**0.6
    env = strokes * np.minimum(1, tt/0.04) * np.minimum(1, (dur-tt)/0.06)
    i = int(t0*SR); sfx[i:i+L] += 0.35*noise*env
for k, t in enumerate(sub_t):
    scribble(t, LINE_DUR[k])
sfx = sfx / (np.abs(sfx).max()+1e-9) * 10**(-14/20)      # pico a -14 dBFS (fica por baixo da voz)
raw = SLOT/'sfx_raw.wav'
with wave.open(str(raw), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((sfx*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(raw), '-af', 'highpass=f=120,lowpass=f=9000', '-ac', '2', str(E/'sfx.wav')], check=True)
json.dump({'text_end': text_end, 'teaser_end': teaser_end, 'labels': labels}, open(SLOT/'timings.json', 'w'), indent=1)
print(f'teaser {teaser_end:.2f}s · textos iniciais até {text_end:.2f}s · título {T0:.2f}-{title_done:.2f} · subtítulo {sub_t[0]:.2f}-{sub_done:.2f} · corpo {BODY_T:.2f}')
for a, b, hh, dd in labels: print(f'  {a:6.2f}-{b:6.2f}  {hh} {dd}')
