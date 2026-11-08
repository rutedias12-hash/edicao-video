"""Versão com a voz nova (áudio 85, 2026-11-08), a partir de edl_vozoff.json (versão aprovada a 23/10):
- mesmos clipes e mesmos cortes; fontes = pedaços recuperados dos clipes originais (pedacos_map.json);
- 1.ª metade (até à sopa): sem mexer em nada (a voz é que foi apertada: apertar_voz.py);
- 2.ª metade: sai o plano "a jantar tranquilamente" e os planos ficam acelerados VEL× (pedido da Rute: "acelera ligeiramente");
  o fecho (embalagem com aproximação) mantém a velocidade.
- Voz: parte A (voz85_A) acaba 0,25 s antes do "Eu descobri"; parte B dividida em 4 frases, cada uma a entrar na sua cena.
Gera edl_voz85.json + voz85_tempos.json. Uso: python3 scripts/build_edl_voz85.py
"""
import json, subprocess
from pathlib import Path
import numpy as np
E = Path(__file__).resolve().parents[1]; V = E.parent
VEL = 1.15
# v2 (Rute: 'há muitos momentos sem voz off'): velocidade por cena na 2.ª metade, mais nos planos lentos
VEL_CENA = {'jantar_henrique': 1.3, 'banho': 1.5, 'pijama': 1.35, 'deitar': 1.45, 'clara': 1.8, 'sopa_taca': 1.45, 'mesa': 1.2}
FECHO = 1.9   # o fecho (embalagem com aproximação) fica mais curto, à mesma velocidade
GAP = 0.35    # silêncio entre frases da voz
base = json.load(open(E/'edl_vozoff.json')); M = json.load(open(E/'pedacos_map.json'))
SEC = [('chegada', 0), ('cozinha', 3), ('sopa', 13), ('jantar_henrique', 16), ('banho', 20), ('pijama', 24), ('deitar', 26),
       ('clara', 30), ('sopa_taca', 32), ('mesa', 34), ('fecho', 36)]
FORA = {35}
ini_sec = {i: n for n, i in SEC}
src, out, secs, t = {}, [], {}, 0.0
for i, r in enumerate(base['ranges']):
    if i in ini_sec: secs[ini_sec[i]] = round(t, 4)
    if i in FORA: continue
    r = dict(r); m = M[r['source']]
    src[r['source']] = str(V/'hq_pedacos'/f"{r['source']}.mov")
    d = r['end'] - r['start']
    r['start'] = round(m['clip_start_plano'] - m['piece_a'], 4); r['end'] = round(r['start'] + d, 4)
    for c in r.get('cutaways', []):
        mc = M[c[3]]; c[0] = round(mc['clip_start_plano'] - mc['piece_a'], 4); src[c[3]] = str(V/'hq_pedacos'/f'{c[3]}.mov')
    cena = [n for n, j in SEC if j <= i][-1]
    if cena in VEL_CENA: r['speed'] = VEL_CENA[cena]
    if cena == 'fecho': r['end'] = round(r['start'] + FECHO, 4); d = FECHO
    out.append(r)
    t += max(1, round(d / r.get('speed', 1.0) * 30)) / 30
secs['fim'] = round(t, 4)
json.dump({'version': 1, 'sources': src, 'ranges': out, 'total_duration_s': round(t, 3)}, open(E/'edl_voz85.json', 'w'), indent=1, ensure_ascii=False)

# ---- voz: parte B dividida em frases ----
SR = 48000
def ler(f):
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-f', 's16le', '-'], capture_output=True, check=True).stdout,
                         np.int16).reshape(-1, 2)
def escrever(y, nome, pal):
    (V/'voz'/'t.raw').write_bytes(y.tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', str(V/'voz'/'t.raw'), str(V/'voz'/f'{nome}.wav')], check=True)
    (V/'voz'/'t.raw').unlink(); json.dump(pal, open(V/'voz'/f'{nome}_palavras.json', 'w'), ensure_ascii=False, indent=0)
# v2: voz da 2.ª parte um pouco mais lenta (pedido da Rute), sem mudar o tom (atempo)
LENTO = 0.92
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V/'voz/voz85_B.wav'), '-af', f'atempo={LENTO}', str(V/'voz/voz85_B_lento.wav')], check=True)
B = ler(V/'voz/voz85_B_lento.wav')
PB = [dict(w, ini=round(w['ini']/LENTO, 3), fim=round(w['fim']/LENTO, 3)) for w in json.load(open(V/'voz/voz85_B_palavras.json'))]
frases, cur = [], []
for w in PB:
    cur.append(w)
    if w['texto'][-1] in '.?' or w['texto'] == 'rotina,': frases.append(cur); cur = []
if cur: frases.append(cur)
assert len(frases) == 4, [' '.join(w['texto'] for w in f) for f in frases]
nomes = []
for k, f in enumerate(frases):
    a = max(0.0, f[0]['ini'] - 0.04); b = f[-1]['fim'] + 0.08
    if k + 1 < len(frases): b = min(b, frases[k+1][0]['ini'] - 0.02)
    y = B[int(a*SR):int(b*SR)].copy(); F = int(0.01*SR); r = np.linspace(0, 1, F)[:, None]
    y = (y.astype(float)); y[:F] *= r; y[-F:] *= r[::-1]
    escrever(y.astype(np.int16), f'voz85_B{k+1}', [dict(w, ini=round(w['ini']-a, 3), fim=round(w['fim']-a, 3)) for w in f])
    nomes.append((f'voz85_B{k+1}', len(y)/SR))
dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)]))
pa = json.load(open(V/'voz/voz85_A_palavras.json'))
vozes = [['voz85_A', round(secs['sopa'] + 0.1 - 0.25 - pa[-1]['fim'], 3)]]
fim_ant = secs['sopa'] + 7.3
for (nome, d), cena in zip(nomes, ['jantar_henrique', 'banho', 'deitar', 'clara']):
    t0 = round(max(secs[cena] + 0.1, fim_ant + GAP) if cena != 'jantar_henrique' else secs[cena] + 0.15, 3); vozes.append([nome, t0]); fim_ant = t0 + d
tempos = {'secoes': secs, 'vozes': vozes}
json.dump(tempos, open(E/'voz85_tempos.json', 'w'), indent=1)
print(json.dumps(tempos, indent=1)); print('voz acaba aos', round(fim_ant, 2), 's de', secs['fim'])
