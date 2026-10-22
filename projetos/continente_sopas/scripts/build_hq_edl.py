"""edl_montagem.json + hq_pedacos/hq_map.json → edl_montagem_hq.json (mesmos planos, a partir dos clipes originais do iPhone)."""
import json
from pathlib import Path
E = Path(__file__).resolve().parent.parent; V = E.parent
edl = json.load(open(E/'edl_montagem.json')); m = json.load(open(V/'hq_pedacos/hq_map.json'))
srcs, R = {}, []
for i, r in enumerate(edl['ranges']):
    k = f'{i:02d}'; assert k in m, f'falta o pedaço do plano {k}'
    p = m[k]; sid = p['piece'][:-4]; srcs[sid] = str(V/'hq_pedacos'/p['piece'])
    x = dict(r); x.update(source=sid, start=p['start'], end=round(p['start'] + p['dur'], 4)); R.append(x)
out = dict(edl); out.update(sources=srcs, ranges=R)
json.dump(out, open(E/'edl_montagem_hq.json', 'w'), ensure_ascii=False, indent=1)
print(len(R), 'planos → edl_montagem_hq.json')
