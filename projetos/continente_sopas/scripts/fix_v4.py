"""Sobre rute_v3/continenteReels_corrigido.mp4: troca o plano do jantar do Henrique (26,067–28,567 s, frames 782–856)
por um plano da mesma atividade SEM fala (36:11,6–36:14,1 do original): imagem sem letras + som ambiente do próprio plano.
Restos de sopa na taça apagados como na fix_v3. Resto do vídeo e do som inalterados.
Uso: python3 scripts/fix_v4.py → videos/rute_v4/continenteReels_v4.mp4
"""
import subprocess
from pathlib import Path
import numpy as np, cv2

V = Path(__file__).resolve().parents[2]
SRC, BASE = V/'continente_sopas.mov', V/'rute_v3/continenteReels_corrigido.mp4'
OUTD = V/'rute_v4'; OUTD.mkdir(exist_ok=True)
OUT = OUTD/'continenteReels_v4.mp4'
W, H, FPS, SR = 2160, 3840, 30, 48000
F0, F1 = 782, 857                      # plano a trocar (75 frames = 2,5 s)
NEW_START = 2171.6                     # início do plano novo na fonte (imagem); som +0,10 s (atraso do microfone)
AV_OFFSET, GAIN = 0.10, 1.70           # GAIN: mesmo nível que o resto do som da Rute (medido antes)
SIZE = W*H*3
N = F1 - F0

def reader(args, fmt='rgb24'):
    return subprocess.Popen(['ffmpeg', '-v', 'error', *args, '-pix_fmt', fmt, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
def read(p):
    b = p.stdout.read(SIZE)
    return np.frombuffer(b, np.uint8).reshape(H, W, 3) if len(b) == SIZE else None
def pcm(f, ss, t):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.4f}', '-t', f'{t:.4f}', '-i', str(f), '-vn', '-ac', '2', '-ar', str(SR),
                        '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32).reshape(-1, 2) / 32768

# plano novo (4K nativo, 30 fps)
pn = reader(['-ss', f'{NEW_START:.3f}', '-t', f'{N/FPS+0.2:.3f}', '-i', str(SRC), '-vf', f'fps={FPS},trim=end_frame={N}'])
newf = [read(pn) for _ in range(N)]; pn.wait()
assert all(f is not None for f in newf), 'frames em falta no plano novo'

# taça: restos de sopa apagados (máscara pela cor, preenchimento suave; borda da taça intacta)
X0, Y0, X1, Y1 = 100, 2250, 480, 2480
med = np.median(np.stack([f[Y0:Y1, X0:X1] for f in newf]), 0).astype(np.uint8)
bgr = cv2.cvtColor(med, cv2.COLOR_RGB2BGR); hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
inner = np.zeros(med.shape[:2], np.uint8); cv2.ellipse(inner, (180, 86), (136, 34), 0, 0, 360, 1, -1)
M = ((hsv[..., 1] > 115) & (hsv[..., 0] <= 30)).astype(np.uint8) & inner
M = cv2.dilate(M, np.ones((7, 7), np.uint8)) & inner
fill = cv2.GaussianBlur(cv2.inpaint(cv2.GaussianBlur(bgr, (0, 0), 1.2), M*255, 20, cv2.INPAINT_TELEA), (0, 0), 2.5)
fill = cv2.cvtColor(fill, cv2.COLOR_BGR2RGB).astype(np.float32)
A = cv2.GaussianBlur(M.astype(np.float32), (0, 0), 1.5)[..., None]
cv2.imwrite(str(OUTD/'taca_antes_depois.png'), cv2.cvtColor(np.concatenate([med, (med*(1-A)+fill*A).astype(np.uint8)], 1), cv2.COLOR_RGB2BGR))
print('px de sopa apagados:', int(M.sum()))

# vídeo
base = reader(['-i', str(BASE)])
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', str(OUTD/'video.mkv')], stdin=subprocess.PIPE)
i = 0
while True:
    f = read(base)
    if f is None: break
    if F0 <= i < F1:
        f = newf[i-F0].copy(); reg = f[Y0:Y1, X0:X1].astype(np.float32)
        f[Y0:Y1, X0:X1] = (reg*(1-A) + fill*A).astype(np.uint8)
    enc.stdin.write(f.tobytes()); i += 1
enc.stdin.close(); enc.wait()
print('frames:', i)

# som: janela do plano trocada pelo som ambiente do plano novo (sem fala), com transições de 20 ms
full = pcm(BASE, 0, 999)
s0, n = int(round(F0/FPS*SR)), int(round(N/FPS*SR))
win = pcm(SRC, NEW_START + AV_OFFSET, N/FPS + 0.05)[:n] * GAIN
xf = int(0.02*SR); r = np.linspace(0, 1, xf)[:, None]
win[:xf] = full[s0:s0+xf]*(1-r) + win[:xf]*r
win[-xf:] = win[-xf:]*(1-r) + full[s0+n-xf:s0+n]*r
full[s0:s0+n] = win
print('nível do som novo:', round(20*np.log10(np.sqrt((win**2).mean())+1e-9), 1), 'dB · pico', round(20*np.log10(np.abs(win).max()+1e-9), 1), 'dBFS')
(OUTD/'audio.raw').write_bytes((np.clip(full, -1, 1)*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUTD/'video.mkv'), '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', str(OUTD/'audio.raw'),
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-tag:v', 'avc1',
                '-movflags', '+faststart', str(OUT)], check=True)
print('pronto:', OUT)
