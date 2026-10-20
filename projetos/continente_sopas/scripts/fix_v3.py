"""Correções sobre a versão 'continenteReels.mov' da Rute (textos e SFX dela já na imagem/som).

1) Teaser: os 3 planos de sopa trocados (mesma técnica do replace_teaser.py — textos dela preservados).
2) Jantar do Henrique (26,07–28,57 s): restos de sopa dentro da taça apagados (preenchimento suave; borda intacta).
3) Som do "Espera, filho" (11,467–14,667 s): sai o choro, entram dois resmungos curtos do Henrique (8:02 e 9:24 do original).
   O resto do som da Rute fica igual.
Uso: python3 scripts/fix_v3.py → videos/rute_v3/continenteReels_corrigido.mp4
"""
import os, subprocess
from pathlib import Path
import numpy as np, cv2

V = Path(__file__).resolve().parents[2]
SRC, HER, CLEAN = V/'continente_sopas.mov', V/'rute_v3/continenteReels.mov', V/'edit/final_4k.mp4'
OUT = V/'rute_v3/continenteReels_corrigido.mp4'
W, H, FPS, SR = 2160, 3840, 30, 48000
SIZE = W*H*3

def reader(args, fmt='rgb24'):
    return subprocess.Popen(['ffmpeg', '-v', 'error', *args, '-pix_fmt', fmt, '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
def read(p):
    b = p.stdout.read(SIZE)
    return np.frombuffer(b, np.uint8).reshape(H, W, 3) if len(b) == SIZE else None
def pcm(f, ss, t, ch=2):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{ss:.4f}', '-t', f'{t:.4f}', '-i', str(f), '-vn', '-ac', str(ch), '-ar', str(SR),
                        '-f', 's16le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.int16).astype(np.float32).reshape(-1, ch) / 32768

# ---------- 1) teaser: planos novos + moldes dos textos ----------
FR, SP, HEAD = 9, 3.0, 72
SLOTS = {2: 132.0, 6: 2446.0, 7: 1259.4}
new = {}
for slot, s in SLOTS.items():
    p = reader(['-ss', f'{s:.3f}', '-t', f'{FR/FPS*SP+0.2:.3f}', '-i', str(SRC), '-vf',
                f'scale=-2:{H},setpts=(PTS-STARTPTS)/{SP},fps={FPS},trim=end_frame={FR}'])
    new[slot] = [read(p) for _ in range(FR)]; p.wait()
def frame_at(f, n):
    p = reader(['-i', str(f), '-vf', f'select=eq(n\\,{n})', '-vsync', '0', '-frames:v', '1']); x = read(p); p.wait(); return x
def dilate(m, r):
    return cv2.dilate(m.astype(np.uint8), np.ones((2*r+1, 2*r+1), np.uint8)).astype(bool)
MAG = np.array([161, 0, 50], np.float32)
h80, c80 = frame_at(HER, 80).astype(np.float32), frame_at(CLEAN, 80).astype(np.float32)
d80 = np.abs(h80 - c80).max(2)
M_TITLE = dilate(np.sqrt(((h80 - MAG) ** 2).sum(2)) < 90, 6); M_TITLE[1950:] = False
M_WHITE = dilate((h80.min(2) > 185) & (d80 > 40), 6)

# ---------- 2) taça: preenchimento estático calculado na mediana do plano ----------
F0, F1 = 782, 857                                   # frames do plano (26,067–28,567 s)
X0, Y0, X1, Y1 = 100, 2250, 480, 2480
pb = reader(['-ss', f'{F0/FPS:.4f}', '-t', f'{(F1-F0)/FPS:.4f}', '-i', str(HER), '-vf', f'crop={X1-X0}:{Y1-Y0}:{X0}:{Y0}'], 'bgr24')
crop = np.frombuffer(pb.stdout.read(), np.uint8).reshape(-1, Y1-Y0, X1-X0, 3); pb.wait()
med = np.median(crop, 0).astype(np.uint8)
hsv = cv2.cvtColor(med, cv2.COLOR_BGR2HSV)
inner = np.zeros(med.shape[:2], np.uint8); cv2.ellipse(inner, (180, 86), (136, 34), 0, 0, 360, 1, -1)
M = ((hsv[..., 1] > 115) & (hsv[..., 0] <= 30)).astype(np.uint8) & inner
M = cv2.dilate(M, np.ones((7, 7), np.uint8)) & inner
fill = cv2.GaussianBlur(cv2.inpaint(cv2.GaussianBlur(med, (0, 0), 1.2), M*255, 20, cv2.INPAINT_TELEA), (0, 0), 2.5)
fill = cv2.cvtColor(fill, cv2.COLOR_BGR2RGB).astype(np.float32)
A_BOWL = cv2.GaussianBlur(M.astype(np.float32), (0, 0), 1.5)[..., None]

if not os.environ.get('SKIP_VIDEO'):  # SKIP_VIDEO=1 → refaz só o som (reaproveita rute_v3/video.mkv)
    # ---------- vídeo: um único passe ----------
    her = reader(['-i', str(HER)]); clean = reader(['-i', str(CLEAN), '-frames:v', str(HEAD)])
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', str(V/'rute_v3/video.mkv')], stdin=subprocess.PIPE)
    i = 0
    while True:
        h = read(her)
        if h is None: break
        out = h
        if i < HEAD:
            c = read(clean); slot = i // FR
            if slot in SLOTS:
                hf = h.astype(np.float32); d = np.abs(h.astype(np.int16) - c.astype(np.int16)).max(2).astype(np.float32)
                a_mag = np.clip((75 - np.sqrt(((hf - MAG) ** 2).sum(2))) / 40, 0, 1) * M_TITLE * np.clip((d - 18) / 22, 0, 1)
                wh = np.clip((hf.min(2) - 165) / 45, 0, 1)
                a_wh = wh * np.clip((d - 25) / 25, 0, 1) * M_WHITE
                cur = (wh > 0.5) & (d > 60); cur[:300] = False; cur[1950:] = False
                a_cur = (cur & (cur.sum(0) > 120)[None, :]).astype(np.float32)
                a = np.maximum.reduce([a_mag, a_wh, a_cur]); a = cv2.dilate(a, np.ones((3, 3), np.uint8))[..., None]
                out = (hf * a + new[slot][i % FR] * (1 - a)).astype(np.uint8)
        elif F0 <= i < F1:
            out = h.copy(); reg = out[Y0:Y1, X0:X1].astype(np.float32)
            out[Y0:Y1, X0:X1] = (reg * (1 - A_BOWL) + fill * A_BOWL).astype(np.uint8)
        enc.stdin.write(out.tobytes()); i += 1
    enc.stdin.close(); enc.wait(); clean.kill()
    print('frames:', i)


# ---------- 3) som ----------
full = pcm(HER, 0, 999)
T0 = 11.4666                                         # início do plano "Espera, filho. Espera." no vídeo da Rute
VOICE = 0.90                                         # a voz dela começa aos 0,93 s (medido); troca até aqui
s0 = int(round(T0*SR)); nv = int(round(VOICE*SR))
# a) antes da voz: sai o choro → som ambiente do próprio plano (sem a camada de choro) + resmungo 1
amb = pcm(SRC, 585.5 + 0.10, VOICE)[:nv] * 1.70
def add(buf, ss, dur, at, gain):
    x = pcm(SRC, ss, dur); L = len(x); t = np.arange(L)
    x = x * (np.minimum(1, t/(0.06*SR)) * np.minimum(1, (L-t)/(0.10*SR)))[:, None] * gain
    k = int(at*SR); m = max(0, min(L, len(buf)-k)); buf[k:k+m] += x[:m]
add(amb, 482.64 + 0.10 - 0.05, 0.85, 0.08, 1.70)     # resmungo 1 (8:02 do original)
xf = int(0.02*SR); r = np.linspace(0, 1, xf)[:, None]
amb[:xf] = full[s0:s0+xf]*(1-r) + amb[:xf]*r          # entrada suave
amb[-xf:] = amb[-xf:]*(1-r) + full[s0+nv-xf:s0+nv]*r  # passa para a voz original dela
full[s0:s0+nv] = amb
# a2) fim do choro por baixo do 1.º "Espera" (0,90–1,50 s): subtrair a camada de choro que lá tinha sido posta
cry = pcm(SRC, 566.3 + 0.10, 1.5); L = len(cry); t = np.arange(L)
cry = cry * (10**(2/20)) * (np.minimum(1, t/(0.08*SR)) * np.minimum(1, (L-t)/(0.15*SR)))[:, None]
a0, a1 = s0 + nv, s0 + int(1.5*SR)
seg_her = full[a0:a1].copy(); c_seg = cry[nv:nv+(a1-a0)]; b_seg = pcm(SRC, 585.5 + 0.10 + VOICE, 0.6)[:a1-a0]
best = None
for lag in range(-240, 241, 8):                       # procurar o alinhamento exato (±5 ms)
    cl = np.roll(c_seg, lag, 0)
    X = np.stack([b_seg[:, 0], cl[:, 0]], 1); co, *_ = np.linalg.lstsq(X, seg_her[:, 0], rcond=None)
    err = ((seg_her[:, 0] - X @ co) ** 2).mean()
    if best is None or err < best[0]: best = (err, lag, co)
err, lag, co = best
before = 20*np.log10(np.sqrt((seg_her**2).mean())+1e-9)
full[a0:a1] = seg_her - co[1] * np.roll(c_seg, lag, 0)
print(f'choro por baixo da voz: desfasamento {lag/48:.2f} ms, fator {co[1]:.2f}; nível {before:.1f} → {20*np.log10(np.sqrt((full[a0:a1]**2).mean())+1e-9):.1f} dB')
# b) resmungo 2, baixinho, na pausa entre "Espera, filho." e "Espera." (voz dela intacta)
add(full, 564.54 + 0.10 - 0.05, 0.40, T0 + 1.98, 1.70 * 0.5)  # pausa: 1,99–2,37 s
pk = np.abs(full[s0:s0+int(3.2*SR)]).max(); print('pico do trecho:', round(20*np.log10(pk+1e-9), 2), 'dBFS')
lim = 0.98                                            # limitador suave só nos raros picos acima de -0,2 dBFS
ax = np.abs(full); over = ax > lim
full[over] = np.sign(full[over]) * (lim + (1-lim) * np.tanh((ax[over]-lim)/(1-lim)))
print('amostras limitadas:', int(over.sum()), '· pico final:', round(20*np.log10(np.abs(full).max()+1e-9), 2), 'dBFS')
(V/'rute_v3/audio.raw').write_bytes((np.clip(full, -1, 1)*32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V/'rute_v3/video.mkv'), '-f', 's16le', '-ar', str(SR), '-ac', '2',
                '-i', str(V/'rute_v3/audio.raw'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                '-shortest', '-tag:v', 'avc1', '-movflags', '+faststart', str(OUT)], check=True)
print('pronto:', OUT)
