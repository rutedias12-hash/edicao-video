"""Montagem com voz off (áudios 81 e 82 da Rute): a partir de edl_montagem_hq.json, acrescenta 4 clipes de caos
antes da sopa e acerta a duração de cada clipe às frases da voz. Gera edl_vozoff.json + vozoff_tempos.json
(início de cada secção e onde entra cada voz), usado pelo lettering e pela mistura do som.
Durações em múltiplos de 1/30 s (servem a 30 e a 60 fps). Uso: python3 scripts/build_edl_vozoff.py
"""
import json, subprocess
from pathlib import Path

E = Path(__file__).resolve().parents[1]
P = E.parents[0]/'hq_pedacos'
base = json.load(open(E/'edl_montagem_hq.json'))
R = base['ranges']
src = dict(base['sources'])
for k in ['p_caos1', 'p_caos2', 'p_caos3', 'p_caos4']:
    src[k] = str(P/f'{k}.mov')
novos = {  # início (no pedaço) do momento escolhido no vídeo longo
    'caos1': {'source': 'p_caos1', 'start': 0.9 + 0.2, 'quote': '(imagem) Henrique na cadeira, ela corre para o forno (2:33)'},
    'caos3': {'source': 'p_caos3', 'start': 0.7333 + 0.2, 'quote': '(imagem) com o Henrique ao colo, mão na testa (11:32)'},
    'caos2': {'source': 'p_caos2', 'start': 0.8833 + 0.2, 'quote': '(imagem) passa a correr atrás do Henrique (2:46)'},
    'caos4': {'source': 'p_caos4', 'start': 0.8667 + 0.2, 'quote': '(imagem) a correr para o lava-loiça (2:57)'},
}
# (clipe, duração) — índices = edl_montagem_hq.json; secções marcadas para o lettering
SEQ = [
    ('chegada', [(0, 1.5), (1, 1.5), (2, 1.6)]),
    ('cozinha', [(3, 0.95), (4, 1.0), (5, 1.05), (6, 1.0), (7, 1.0), (8, 1.0),
                 ('caos1', 1.0), ('caos3', 1.0), ('caos2', 1.0), ('caos4', 1.65)]),
    ('sopa', [(9, None), (10, None), (11, None)]),
    ('jantar_henrique', [(12, 1.0), (13, 1.0), (14, 1.1), (15, 1.3)]),
    ('banho', [(16, 1.0), (17, 0.95), (18, 1.6), (19, 0.94)]),
    ('pijama', [(20, 0.82), (21, 0.82)]),
    ('deitar', [(22, 0.81), (23, 0.81), (24, 0.81), (25, 1.0)]),
    ('clara', [(26, 1.95), (27, 1.95)]),
    ('sopa_taca', [(28, 1.6), (29, 1.25)]),
    ('mesa', [(30, 1.35), (31, 1.35)]),
    ('fecho', [(32, 2.35)]),
]
dur_peca = lambda s: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src[s]]))
out, secs, t = [], {}, 0.0
for nome, clipes in SEQ:
    secs[nome] = round(t, 4)
    for c, d in clipes:
        r = dict(novos[c] if isinstance(c, str) else R[c])
        r.pop('label', None); r.pop('beat', None)
        if d is not None:
            d = round(d * 30) / 30
            livre = dur_peca(r['source']) - r['start'] - 0.05
            assert d <= livre + 1e-6, f'{c}: pedaço curto ({livre:.2f} s < {d})'
            r['end'] = round(r['start'] + d, 4)
            r['mute'] = True
        out.append(r); t += round((r['end'] - r['start']) * 30) / 30
secs['fim'] = round(t, 4)
json.dump({'version': 1, 'sources': src, 'ranges': out, 'total_duration_s': round(t, 3)},
          open(E/'edl_vozoff.json', 'w'), indent=1, ensure_ascii=False)
# vozes: o 81 acaba 0,25 s antes do "Eu descobri" (0,1 s depois do início do bloco da sopa);
# o 82 começa 0,05 s depois do fim do bloco da sopa
v81 = json.load(open(E.parents[0]/'voz/voz81_palavras.json'))
inicio81 = secs['sopa'] + 0.1 - 0.25 - v81[-1]['fim']
tempos = {'secoes': secs, 'voz81': round(inicio81, 3), 'voz82': round(secs['jantar_henrique'] + 0.05, 3)}
json.dump(tempos, open(E/'vozoff_tempos.json', 'w'), indent=1)
print(json.dumps(tempos, indent=1))
