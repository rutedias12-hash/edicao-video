"""Troca planos do teaser no vídeo editado pela Rute (com textos já 'colados' na imagem), mantendo os textos dela.

Como: a versão dela coincide imagem a imagem com a nossa exportação limpa (final_4k.mp4) — confirmado.
Para cada frame a trocar: máscara do texto = onde a imagem dela difere da limpa; resultado = texto dela por cima do plano novo.
O som dela fica intacto (stream copy do áudio).
Uso: python3 scripts/replace_teaser.py → rute_v2/sopaContinente_teaser.mp4 (+ head_check.mkv para verificação)
"""
import subprocess
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parents[2]          # pasta videos/
SRC = V/'continente_sopas.mov'
HER = V/'rute_v2/sopaContinente.mov'
CLEAN = V/'edit/final_4k.mp4'
OUT = V/'rute_v2/sopaContinente_teaser.mp4'
W, H, FPS, SP = 2160, 3840, 30, 3.0
FR = 9                                            # 0,3 s por plano
SLOTS = {2: 132.0, 6: 2446.0, 7: 1259.4}          # plano do teaser → início na fonte (3× mais rápido)
HEAD = 8 * FR                                     # 72 frames = 2,4 s de teaser
SIZE = W * H * 3

def reader(args):
    return subprocess.Popen(['ffmpeg', '-v', 'error', *args, '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
def read(p):
    b = p.stdout.read(SIZE)
    return np.frombuffer(b, np.uint8).reshape(H, W, 3) if len(b) == SIZE else None

# planos novos, extraídos e acelerados exatamente como os do teaser (cut.py: escala → acelerar → 30 fps)
new = {}
for slot, s in SLOTS.items():
    p = reader(['-ss', f'{s:.3f}', '-t', f'{FR/FPS*SP+0.2:.3f}', '-i', str(SRC), '-vf',
                f'scale=-2:{H},setpts=(PTS-STARTPTS)/{SP},fps={FPS},trim=end_frame={FR}'])
    new[slot] = [read(p) for _ in range(FR)]; p.wait()
    assert all(f is not None for f in new[slot]), f'plano {slot}: frames em falta'

def frame_at(f, n):
    p = reader(['-i', str(f), '-vf', f'select=eq(n\\,{n})', '-vsync', '0', '-frames:v', '1']); x = read(p); p.wait(); return x
def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r+1, max(1, r//3)):
        for dx in range(-r, r+1, max(1, r//3)):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out
MAG = np.array([161, 0, 50], np.float32)
h80, c80 = frame_at(HER, 80).astype(np.float32), frame_at(CLEAN, 80).astype(np.float32)
d80 = np.abs(h80 - c80).max(2)
M_TITLE = dilate(np.sqrt(((h80 - MAG) ** 2).sum(2)) < 90, 6); M_TITLE[1950:] = False
M_WHITE = dilate((h80.min(2) > 185) & (d80 > 40), 6)
print('molde título px', int(M_TITLE.sum()), '· molde textos brancos px', int(M_WHITE.sum()))

her, clean = reader(['-i', str(HER), '-frames:v', str(HEAD)]), reader(['-i', str(CLEAN), '-frames:v', str(HEAD)])
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                        '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '10', '-pix_fmt', 'yuv420p', str(V/'rute_v2/head.mkv')],
                       stdin=subprocess.PIPE)
for i in range(HEAD):
    h, c = read(her), read(clean)
    assert h is not None and c is not None, f'frame {i} em falta'
    slot = i // FR
    if slot in SLOTS:
        hf = h.astype(np.float32)
        d = np.abs(h.astype(np.int16) - c.astype(np.int16)).max(2).astype(np.float32)
        # 1) título magenta: cor magenta E dentro do molde das letras (nada fora das letras passa)
        dist = np.sqrt(((hf - MAG) ** 2).sum(2))
        a_mag = np.clip((75 - dist) / 40, 0, 1) * M_TITLE * np.clip((d - 18) / 22, 0, 1)  # + só letras já escritas (diferem da imagem limpa)
        # 2) legendas brancas: brancas, diferentes da imagem limpa E dentro do molde
        whiteness = np.clip((hf.min(2) - 165) / 45, 0, 1)
        a_wh = whiteness * np.clip((d - 25) / 25, 0, 1) * M_WHITE
        # 3) cursor do typewriter: barra branca vertical na zona do título (colunas com uma tira branca comprida)
        cur = (whiteness > 0.5) & (d > 60); cur[:300] = False; cur[1950:] = False
        cols = cur.sum(0) > 120
        a_cur = (cur & cols[None, :]).astype(np.float32)
        a = np.maximum.reduce([a_mag, a_wh, a_cur])
        a = np.maximum.reduce([a, np.roll(a, 1, 0), np.roll(a, -1, 0), np.roll(a, 1, 1), np.roll(a, -1, 1)])[..., None]
        out = (h * a + new[slot][i % FR] * (1 - a)).astype(np.uint8)
    else:
        out = h
    enc.stdin.write(out.tobytes())
enc.stdin.close(); enc.wait(); her.kill(); clean.kill()

# juntar: cabeça nova (72 frames) + resto do vídeo dela; som dela inteiro, sem alterações
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V/'rute_v2/head.mkv'), '-i', str(HER), '-filter_complex',
                f'[1:v]trim=start_frame={HEAD},setpts=PTS-STARTPTS[t];[0:v][t]concat=n=2:v=1:a=0[v]',
                '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p',
                '-c:a', 'copy', '-tag:v', 'avc1', '-movflags', '+faststart', str(OUT)], check=True)
print('pronto:', OUT)
