"""Tira um pedaço de um clipe original do iPhone (com som) que corresponde a uma janela do vídeo longo, e acerta imagem e som.
Uso: python3 hq_piece.py <nome_saida> <IMG_xxxx.MOV> <inicio_no_video_longo> <duracao> [--sem-som]
Imprime JSON: {piece, video_start, dur, av_offset}  (av_offset = atraso do som a usar no cut.py para esta fonte)
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parents[2]
name, img, T0, D = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
nosound = '--sem-som' in sys.argv
d = json.load(open(V/'hq_pedacos/duracoes.json')); n = sorted(d)
cum = dict(zip(n, np.cumsum([0] + [d[x] for x in n])[:-1]))
rough = T0 - cum[img]; a = max(0, rough - 1.0)
piece = V/'hq_pedacos'/f'{name}.mov'
cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', str(V/'clipes_hq'/img), '-t', f'{D+2.0:.3f}', '-map', '0:v:0']
cmd += (['-an'] if nosound else ['-map', '0:a:0', '-c:a', 'pcm_s16le'])
subprocess.run(cmd + ['-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p', str(piece)], check=True)
def gray(args):
    b = subprocess.run(['ffmpeg', '-v', 'error', *args, '-vf', 'fps=60,scale=54:96', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, 96*54).astype(np.float32)
src = gray(['-ss', f'{T0:.3f}', '-t', f'{D:.3f}', '-i', str(V/'continente_sopas.mov')])[::2]
pc = gray(['-i', str(piece)])
e, lag = min((np.abs(pc[l:l+2*len(src):2] - src).mean(), l) for l in range(0, len(pc) - 2*len(src) + 1))
vs = lag/60; out = {'piece': piece.name, 'video_start': round(vs, 4), 'dur': D, 'erro_imagem': round(float(e), 2)}
if not nosound:
    def pcm(f, ss, t):
        return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(ss), '-t', str(t), '-i', str(f), '-vn', '-ac', '1', '-ar', '16000',
                                             '-f', 's16le', '-'], capture_output=True).stdout, np.int16).astype(float)
    L = pcm(V/'continente_sopas.mov', T0, D); P = pcm(piece, 0, D+2.0)
    asv = int(np.argmax(np.correlate(P, L, 'valid')))/16000
    out['av_offset'] = round(0.10 + asv - vs, 4)   # mesmo alinhamento som/imagem que usámos no vídeo longo (+0,10 s)
print(json.dumps(out))
