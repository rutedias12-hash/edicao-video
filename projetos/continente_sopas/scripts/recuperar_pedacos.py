"""Recupera os pedaços (videos/hq_pedacos) usados em edl_vozoff.json a partir dos clipes originais do iPhone,
acertando cada plano ao frame contra a versão aprovada (ReelsSopaContinentev4.mp4, 1080p, = edl_vozoff).
Guarda em edit/pedacos_map.json: {fonte: {file, clip_start (s no clipe onde o plano começa)}} e
cria videos/hq_pedacos/<fonte>.mov (pedaço com 1 s de margem antes; ALTURA = 1920 pré-visualização, 3840 final).
Uso: ALTURA=1920 python3 recuperar_pedacos.py
"""
import json, os, subprocess
from pathlib import Path
import numpy as np
V = Path(__file__).resolve().parents[2]; E = V/'edit'
REF = V/'continente/ficheiro/ReelsSopaContinentev4.mp4'
HQ, OUT = V/'clipes_hq', V/'hq_pedacos'; OUT.mkdir(exist_ok=True)
ALT = int(os.environ.get('ALTURA', '1920'))
edl = json.load(open(E/'edl_vozoff.json'))
durs = json.load(open(E/'duracoes.json')); names = sorted(durs)
cum = dict(zip(names, np.cumsum([0] + [durs[n] for n in names])[:-1]))
hq = json.load(open(E/'hq_map.json')); mont = {r['quote']: r['start'] for r in json.load(open(E/'edl_montagem.json'))['ranges']}
MAPF = E/'pedacos_map.json'
mapa = json.load(open(MAPF)) if MAPF.exists() else {}

def gray(args, fps):
    b = subprocess.run(['ffmpeg', '-v', 'error', *args, '-an', '-vf', f'fps={fps},scale=54:96', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 96*54).astype(np.float32)

def estimativa(src):
    if src.startswith('p_caos'):
        t = {'p_caos1': 153, 'p_caos3': 692, 'p_caos5': 145, 'p_caos4': 177}[src]
        f = max(n for n in names if cum[n] <= t); return f, t - cum[f], 4.0
    if src.startswith('p_sopa'): return 'IMG_6588.MOV', 18.0, 18.0
    if src == 'p_emb_cut': return 'IMG_6634.MOV', 7.0, 7.0
    k = src[1:3]; h = hq[k]; t = mont[h['quote']]; f = h['file']
    a = max(0.0, t - cum[f] - 1.0)
    return f, a + h['start'], 1.2

# tempos de cada fonte na versão aprovada
usos, t = [], 0.0
for r in edl['ranges']:
    d = round((r['end'] - r['start'])*30)/30
    usos.append((r['source'], r['start'], t, min(d, 0.8)))
    for c in r.get('cutaways', []):
        if len(c) > 3: usos.append((c[3], c[0], t + c[2], min(c[1], 0.8)))
    t += d
for src, st, T, d in usos:
    if src in mapa: continue
    f, est, W = estimativa(src)
    ref = gray(['-ss', f'{T:.3f}', '-t', f'{d:.3f}', '-i', str(REF)], 30)
    w0 = max(0.0, est - W)
    cand = gray(['-ss', f'{w0:.3f}', '-t', f'{2*W + d + 0.2:.3f}', '-i', str(HQ/f)], 60)
    n = len(ref)
    e, lag = min((np.abs(cand[l:l+2*n:2] - ref).mean(), l) for l in range(0, len(cand) - 2*n + 1))
    ini = w0 + lag/60
    mapa[src] = {'file': f, 'clip_start_plano': round(ini, 4), 'start_edl': st, 'erro': round(float(e), 2)}
    print(f'{src:14s} {f} plano aos {ini:7.3f}s do clipe · erro {e:.1f} (estimativa {est:.2f})', flush=True)
    json.dump(mapa, open(MAPF, 'w'), indent=1)
# pedaços: começam 1 s antes do início do plano usado; o EDL passa a usar start=1.0 (ou menos se o clipe começa antes)
for src, m in mapa.items():
    a = max(0.0, m['clip_start_plano'] - 1.0); m['piece_a'] = round(a, 4)
    usado = max(r['end'] - r['start'] for r in edl['ranges'] if r['source'] == src) if any(r['source'] == src for r in edl['ranges']) else 2.0
    D = 1.0 + usado*1.3 + 1.5
    p = OUT/f'{src}.mov'
    if not p.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', str(HQ/m['file']), '-t', f'{D:.3f}', '-map', '0:v:0', '-map', '0:a:0',
                        '-vf', f'scale=-2:{ALT}', '-c:v', 'libx264', '-preset', 'fast', '-crf', '12', '-pix_fmt', 'yuv420p',
                        '-c:a', 'pcm_s16le', str(p)], check=True)
json.dump(mapa, open(MAPF, 'w'), indent=1)
print('pedaços prontos:', len(mapa))
