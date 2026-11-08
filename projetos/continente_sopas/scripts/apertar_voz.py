"""Divide a voz condensada (vozNN.wav) em duas partes (antes/depois da sopa) e, na parte 1, encurta ainda mais
os silêncios (pedido da Rute 2026-11-08: na 1.ª metade não alongar planos, cortar pausas na voz).
Silêncio = trechos de 10 ms abaixo de LIM dB. Cada silêncio passa a: fim de frase FRASE s, vírgula VIRG s, resto RESTO s.
Uso: python3 apertar_voz.py 85 <índice da última palavra da parte 1> <duração máxima da parte 1>
Saída: videos/voz/vozNN_A.wav, vozNN_B.wav + _palavras.json
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
V = Path(__file__).resolve().parents[2]/'voz'
n, last, maxd = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
SR = 48000
x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(V/f'voz{n}.wav'), '-f', 's16le', '-'], capture_output=True, check=True).stdout,
                  np.int16).astype(np.float32).reshape(-1, 2)/32768
P = json.load(open(V/f'voz{n}_palavras.json'))
corte = (P[last]['fim'] + P[last+1]['ini'])/2
def wr(y, nome, pal):
    (V/'t.raw').write_bytes((np.clip(y, -1, 1)*32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', str(V/'t.raw'), str(V/f'{nome}.wav')], check=True)
    (V/'t.raw').unlink(); json.dump(pal, open(V/f'{nome}_palavras.json', 'w'), ensure_ascii=False, indent=0)
# parte B: sem mexer, começa 0,04 s antes da 1.ª palavra
b0 = P[last+1]['ini'] - 0.04
wr(x[int(b0*SR):], f'voz{n}_B', [dict(w, ini=round(w['ini']-b0, 3), fim=round(w['fim']-b0, 3)) for w in P[last+1:]])
A = x[:int(min(corte, P[last]['fim'] + 0.08)*SR)]
PA = P[:last+1]
H = int(0.01*SR)
INTERNO = 0.07
def fazer(LIM, FRASE, VIRG, RESTO):
    m = A.mean(1); nb = len(m)//H
    db = 20*np.log10(np.sqrt((m[:nb*H].reshape(nb, H)**2).mean(1)) + 1e-9)
    sil = db < LIM; runs = []; s = None
    for i, v in enumerate(list(sil) + [False]):
        if v and s is None: s = i
        if not v and s is not None: runs.append((s*0.01, i*0.01)); s = None
    keep, t, mapa = [], 0.0, []   # mapa: (t_orig, t_novo)
    cur = 0.0
    for a, b in runs:
        if a <= 0.0 or b >= len(A)/SR - 0.005: continue
        # dentro de uma palavra (oclusivas p/t/c têm um silêncio curto lá dentro) fica pelo menos INTERNO s
        dentro = any(w['ini'] + 0.03 < (a+b)/2 < w['fim'] - 0.03 for w in PA)
        antes = [w for w in PA if w['fim'] <= a + 0.06]
        p = antes[-1]['texto'][-1] if antes else ''
        alvo = INTERNO if dentro else FRASE if p in '.?!:' else VIRG if p == ',' else RESTO
        if b - a <= alvo: continue
        c0, c1 = a + alvo/2, b - alvo/2          # tira o meio do silêncio
        keep.append((cur, c0)); cur = c1
    keep.append((cur, len(A)/SR))
    out, novo = [], 0.0; F = int(0.005*SR)
    for a, b in keep:
        seg = A[int(a*SR):int(b*SR)].copy()
        if len(seg) > 2*F:
            r = np.linspace(0, 1, F)[:, None]; seg[:F] *= r; seg[-F:] *= r[::-1]
        mapa.append((a, b, novo)); out.append(seg); novo += len(seg)/SR
    f = lambda t: next(nv + (t - a) for a, b, nv in mapa if t <= b + 1e-6) if t <= mapa[-1][1] else novo
    pal = [dict(w, ini=round(f(w['ini']), 3), fim=round(f(w['fim']), 3)) for w in PA]
    return np.concatenate(out), pal
for cfg in [(-45, .18, .10, .05), (-42, .16, .09, .04), (-40, .14, .08, .03), (-38, .12, .07, .03), (-36, .12, .06, .03)]:
    y, pal = fazer(*cfg)
    print(cfg, f'{len(A)/SR:.2f} → {len(y)/SR:.2f} s')
    if len(y)/SR <= maxd: break
wr(y, f'voz{n}_A', pal)
