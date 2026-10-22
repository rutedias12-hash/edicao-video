"""Extrai, dos clipes originais do iPhone (videos/clipes_hq, 4K 60 fps), os pedaços usados na montagem.

O vídeo longo (continente_sopas.mov) é a sequência dos clipes IMG_6555… por ordem (confirmado; desvio ≤ 0,5 s).
Para cada plano de edl_montagem.json: descobre o clipe e a posição, extrai um pedaço com 1 s de margem
(4K, fps original, alta qualidade) e acerta o início exato comparando imagens com o vídeo longo.
Guarda em videos/hq_pedacos/ + hq_map.json. Pode correr várias vezes (vai acrescentando à medida que chegam clipes).
Uso: python3 scripts/hq_extract.py
"""
import json, os, subprocess
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parents[2]
HQ, OUT = V/'clipes_hq', V/'hq_pedacos'
OUT.mkdir(exist_ok=True)
LONG = V/'continente_sopas.mov'
MAPF = OUT/'hq_map.json'
durs = json.load(open(OUT/'duracoes.json')) if (OUT/'duracoes.json').exists() else {}   # duração de cada IMG (fica depois de apagar)
for f in sorted(HQ.glob('IMG_*.MOV')):
    if f.name not in durs:
        durs[f.name] = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)]))
json.dump(durs, open(OUT/'duracoes.json', 'w'), indent=1)
names = sorted(durs)
cum = dict(zip(names, np.cumsum([0] + [durs[n] for n in names])[:-1]))
end_known = cum[names[-1]] + durs[names[-1]]
edl = json.load(open(V/'edit/edl_montagem.json'))
done = json.load(open(MAPF)) if MAPF.exists() else {}
PAD = 1.0

def gray(args, n=None):
    b = subprocess.run(['ffmpeg', '-v', 'error', *args, '-vf', 'fps=60,scale=54:96', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 96*54).astype(np.float32)

for i, r in enumerate(edl['ranges']):
    key = f'{i:02d}'
    if key in done: continue
    t = r['start']
    if t >= end_known: continue
    name = max(n for n in names if cum[n] <= t)
    f = HQ/name
    if not f.exists():
        print(f'{key}: {name} já apagado mas sem pedaço — falta!'); continue
    rough = t - cum[name]; d = r['end'] - r['start']
    a = max(0.0, rough - PAD)
    piece = OUT/f'p{key}_{name[:-4]}.mov'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', str(f), '-t', f'{d + 2*PAD:.3f}', '-an',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', str(piece)], check=True)
    # acertar: imagens do plano no vídeo longo (30 fps) vs pedaço (60 fps) → desvio exato
    src = gray(['-ss', f'{t:.3f}', '-t', f'{d:.3f}', '-i', str(LONG)])[::2]      # 30 fps → amostras a cada 1/30 s
    pc = gray(['-i', str(piece)])
    best = None
    for lag in range(0, len(pc) - 2*len(src) + 1):                                 # passo de 1/60 s
        e = np.abs(pc[lag:lag + 2*len(src):2] - src).mean()
        if best is None or e < best[0]: best = (e, lag)
    e, lag = best
    start = lag / 60
    done[key] = {'piece': piece.name, 'start': round(start, 4), 'dur': d, 'file': name, 'erro': round(float(e), 2),
                 'quote': r['quote'], 'desvio_vs_estimativa': round(start - (rough - a), 3)}
    print(f'{key} {name} {r["quote"][:40]:40s} início {start:.3f}s no pedaço · erro {e:.1f} · desvio {start-(rough-a):+.3f}s', flush=True)
    json.dump(done, open(MAPF, 'w'), indent=1, ensure_ascii=False)
print('planos prontos:', len(done), 'de', len(edl['ranges']), '· clipes conhecidos até', round(end_known, 1), 's do vídeo longo')
