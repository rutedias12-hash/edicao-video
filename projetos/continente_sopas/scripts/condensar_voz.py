"""Tira respirações, pausas e silêncios das gravações de voz off (videos/voz/audioNN.m4a), a partir dos tempos
de cada palavra (ElevenLabs, videos/voz/audioNN_scribe.json).
- Dentro da frase: pausas > 0,12 s ficam com 0,06 s. Depois de vírgula: 0,15 s. Fim de frase (. ? ! …): 0,25 s.
- Cada pedaço leva 0,04 s antes e 0,06 s depois da palavra (não corta consoantes); entra e sai com 12 ms de transição.
Saída: videos/voz/vozNN.wav (48 kHz estéreo) + vozNN_palavras.json (tempos das palavras no áudio novo).
Uso: python3 scripts/condensar_voz.py 81 82
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parents[2]/'voz'
SR, PRE, POS, XF = 48000, 0.04, 0.06, 0.012
for n in sys.argv[1:]:
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(V/f'audio{n}.m4a'), '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'],
                                     capture_output=True, check=True).stdout, np.int16).astype(np.float32).reshape(-1, 2) / 32768
    W = [w for w in json.load(open(V/f'audio{n}_scribe.json'))['words'] if w.get('type') == 'word']
    # blocos de fala contínua: junta palavras separadas por pausas curtas
    blocos, cur = [], [W[0]['start'], W[0]['end'], [W[0]]]
    for w in W[1:]:
        gap = w['start'] - cur[1]
        if gap > 0.12 or cur[2][-1]['text'][-1] in '.,?!…':
            blocos.append(cur); cur = [w['start'], w['end'], [w]]
        else:
            cur[1] = w['end']; cur[2].append(w)
    blocos.append(cur)
    out, palavras, t = [], [], 0.0
    for k, (a, b, ws) in enumerate(blocos):
        a0, b0 = max(0, a - PRE), min(len(x)/SR, b + POS)
        if k + 1 < len(blocos):   # não invadir a palavra seguinte
            b0 = min(b0, blocos[k+1][0] - 0.02)
        if k: a0 = max(a0, blocos[k-1][1] + 0.02)
        seg = x[int(a0*SR):int(b0*SR)].copy()
        f = int(XF*SR); r = np.linspace(0, 1, f)[:, None]
        seg[:f] *= r; seg[-f:] *= r[::-1]
        for w in ws:
            palavras.append({'texto': w['text'], 'ini': round(t + (w['start'] - a0), 3), 'fim': round(t + (w['end'] - a0), 3)})
        out.append(seg); t += len(seg)/SR
        if k + 1 < len(blocos):
            fim = ws[-1]['text'][-1]
            pausa = 0.25 if fim in '.?!…' else 0.15 if fim == ',' else 0.06
            pausa = min(pausa, max(0.0, blocos[k+1][0] - b))   # nunca mais do que a pausa original
            pausa = max(0.0, pausa - PRE - (b0 - b))
            if pausa > 0: out.append(np.zeros((int(pausa*SR), 2), np.float32)); t += int(pausa*SR)/SR
    y = np.concatenate(out)
    (V/f'voz{n}.raw').write_bytes((np.clip(y, -1, 1)*32767).astype(np.int16).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', str(V/f'voz{n}.raw'), str(V/f'voz{n}.wav')], check=True)
    (V/f'voz{n}.raw').unlink()
    json.dump(palavras, open(V/f'voz{n}_palavras.json', 'w'), ensure_ascii=False, indent=0)
    print(f'{n}: {len(x)/SR:.2f} s → {len(y)/SR:.2f} s · {len(blocos)} blocos de fala')
