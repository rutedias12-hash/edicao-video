"""Gera legendas.ass e acerta os tempos dos textos HyperFrames a partir de edl.json + duração real dos segmentos."""
import json, subprocess, re
from pathlib import Path
E = Path(__file__).resolve().parent.parent
edl = json.load(open(E/'edl.json'))
w = [x for x in json.load(open(E/'transcripts/continente_sopas.json'))['words'] if x.get('type') == 'word']
durs = json.load(open(E/'clips_graded/durs.json'))
offs = [sum(durs[:i]) for i in range(len(durs))]; total = sum(durs)

# ---------- legendas ----------
fix = {'continente,': 'Continente,'}
manual = {"FAMILIA": [(0.05, 2.9, "Posso ficar com mais sopa?"), (3.1, 3.68, "Podes, podes.")]}
cues = []
for i, r in enumerate(edl['ranges']):
    off = offs[i]
    if r['beat'] in manual and r['label']:
        for a, b, t in manual[r['beat']]: cues.append([off+a, off+b, t, off+durs[i]])
        continue
    if r['quote'].startswith('(imagem)') or r['beat'] in manual: continue
    ws = [x for x in w if x['start'] >= r['start']-0.02 and x['end'] <= r['end']+0.05]
    groups, cur = [], []
    for x in ws:
        cur.append(x); e = x['text'][-1]
        if e in '.?!' or (e == ',' and len(cur) >= 3) or len(cur) >= 6: groups.append(cur); cur = []
    if cur: groups.append(cur)
    for j in range(len(groups)-1, 0, -1):
        if len(groups[j]) == 1 and len(groups[j-1]) <= 6: groups[j-1] += groups.pop(j)
    for g in groups:
        cues.append([g[0]['start']-r['start']-0.10+off, g[-1]['end']-r['start']-0.10+off, " ".join(fix.get(c['text'], c['text']) for c in g), off+durs[i]])
# frases cortadas a meio: juntar pedaços curtos à legenda anterior quando seguidos
merged = []
for c in cues:
    if merged and len(c[2].split()) <= 2 and c[0]-merged[-1][1] < 0.6 and merged[-1][2][-1] in ',' and len(merged[-1][2].split()) <= 6:
        merged[-1] = [merged[-1][0], c[1], merged[-1][2]+" "+c[2], c[3]]
    else: merged.append(c)
for c in merged: c[2] = c[2][0].upper()+c[2][1:] if (c is merged[0] or merged[merged.index(c)-1][2][-1] in '.?!') else c[2]
fecho_t = next(offs[i] for i, r in enumerate(edl['ranges']) if r['label'] == 'FECHO')
out = []
for k, (a, b, t, segend) in enumerate(merged):
    nxt = merged[k+1][0] if k+1 < len(merged) else b+0.4
    b = min(b+0.25, nxt-0.03, segend) if nxt > b else min(b, segend)
    out.append((max(0, a-0.03), min(b, fecho_t-0.05), t))
ts = lambda s: f"0:{int(s//60):02d}:{s%60:05.2f}"
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Vlog,Poppins Medium,54,&H00FFFFFF,&H00FFFFFF,&H50000000,&H64000000,0,0,0,0,100,100,0,0,1,1.2,2,2,90,90,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(E/'legendas.ass', 'w') as f:
    f.write(hdr)
    for a, b, t in out: f.write(f"Dialogue: 0,{ts(a)},{ts(b)},Vlog,,0,0,0,,{t}\n")

# ---------- textos HyperFrames (index.html gerado) ----------
labs = [(offs[i], r['label']) for i, r in enumerate(edl['ranges']) if r['label']]
prod_end = next(offs[i]+durs[i] for i, r in reversed(list(enumerate(edl['ranges']))) if r['beat'] == 'PRODUTO')
first = labs[0][0]
clips, js = [], []
def show(sel, a, b, d=0.5):
    js.append(f'      show("{sel}", {a:.2f}, {b:.2f}, {d});')
clips.append(f'<div id="ad" class="clip soft" data-start="0" data-duration="3.4"><span id="ad-t">Publicidade · Parceria Continente</span></div>')
clips.append(f'<div id="title" class="clip soft" data-start="0.05" data-duration="{first-0.1:.2f}"><div id="title-a" class="script">Vlog Noite</div><div id="title-b" class="caps">A REALIDADE DE UMA FAMÍLIA DE 4</div><div id="title-c" class="sub">o jantar que (quase) aconteceu</div></div>')
show("#ad-t", 0.1, 3.4); show("#title-a", 0.1, first-0.05, 0.5); show("#title-b", 0.35, first-0.05, 0.4); show("#title-c", 0.6, first-0.05, 0.4)
fecho = None
for k, (t, l) in enumerate(labs):
    nxt = labs[k+1][0] if k+1 < len(labs) else total
    if l == 'FECHO': fecho = t; continue
    if l == 'PRODUTO':
        a, b = t+0.1, prod_end-0.15
        clips.append(f'<div id="product" class="clip soft" data-start="{a:.2f}" data-duration="{b-a:.2f}"><div id="product-card"><div class="name">Sopa Receita do Chef</div><div class="desc">abóbora, camarão e coentros · Continente</div></div></div>')
        show("#product-card", a, b, 0.6); continue
    a = t+0.05; b = min(t+3.0, nxt-0.1)
    if '|' in l:
        tm, what = l.split('|'); inner = f'<div id="lb{k}-a" class="time">{tm}</div><div id="lb{k}-b" class="what">{what}</div>'
        show(f"#lb{k}-a", a, b); show(f"#lb{k}-b", a+0.15, b)
    else:
        inner = f'<div id="lb{k}-b" class="what">{l}</div>'; show(f"#lb{k}-b", a, b)
    clips.append(f'<div id="lb{k}" class="clip label soft" data-start="{a:.2f}" data-duration="{b-a:.2f}">{inner}</div>')
a = fecho+0.1
clips.append(f'<div id="end-shade" class="clip" data-start="{fecho:.2f}" data-duration="{total-fecho:.2f}"><div id="shade-in" class="shade"></div></div>')
clips.append(f'<div id="end" class="clip soft" data-start="{a:.2f}" data-duration="{total-a:.2f}"><div id="e-a" class="script">jantar salvo</div><div id="e-b" class="caps">SOPAS RECEITA DO CHEF</div><div id="e-c" class="brand">CONTINENTE</div></div>')
js.append(f'      tl.fromTo("#shade-in", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease }}, {fecho:.2f});')
for sel, dt, d in [("#e-a", 0.1, 0.7), ("#e-b", 0.45, 0.5), ("#e-c", 0.75, 0.5)]:
    js.append(f'      tl.fromTo("{sel}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: {d}, ease }}, {fecho+dt:.2f});')
tpl = (E/'scripts/overlay_template.html').read_text()
html = tpl.replace('%%DURATION%%', f'{total:.2f}').replace('%%CLIPS%%', '\n      '.join(clips)).replace('%%JS%%', '\n'.join(js))
(E/'animations/slot_1/index.html').write_text(html)
json.dump({'total': total, 'fecho': fecho}, open(E/'animations/slot_1/timings.json', 'w'))
for a, b, t in out: print(f"{a:6.2f}-{b:6.2f} {t}")
print(labs, round(total, 2))
