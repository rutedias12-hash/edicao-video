"""Corta o vídeo a partir de edl.json.
- Duração de cada plano arredondada a frames inteiros (30 fps) e som com exatamente as mesmas amostras → sem desvio acumulado.
- AV_OFFSET: o som da gravação original chega ~0,10 s atrasado (microfone sem fios; medido na porta a fechar aos 15,1 s),
  por isso o som de cada plano é lido 0,10 s mais à frente.
- "cutaways": [[inicio_na_fonte, duracao, aos_x_segundos_do_segmento(, fonte)], ...] — imagem de outro momento por cima do som (B-roll).
- "mute": true — plano sem som.
- "crop": "w:h:x:y" — aproximar a imagem (sobre o 4K original).
- "zoom": [z0, z1] — aproximação lenta (ease in-out).
- "bowl_clean": true — apaga restos de sopa na taça (jantar do Henrique).
- "speed": 1.25 — plano acelerado (duração final = (end-start)/speed).
- "av_offset": 0.06 — atraso do som próprio desta fonte (por defeito 0,10 s, medido no vídeo longo).
- "audio_layers": [[inicio_na_fonte, duracao, aos_x_segundos, ganho_dB], ...] — som extra por baixo.
Uso: python3 scripts/cut.py   → cuts.mp4"""
import json, os, subprocess
from pathlib import Path
E = Path(__file__).resolve().parent.parent
FPS, SR, AV_OFFSET, FADE = int(os.environ.get('FPS', '30')), 48000, 0.10, 0.03   # FPS=60 → montagem a 60 fps
EDLF = os.environ.get('EDL', 'edl.json')   # EDL=edl_montagem.json → outra montagem, sem mexer na anterior
edl = json.load(open(E/EDLF))
NAME = Path(EDLF).stem.replace('edl', 'cuts', 1)
src = {k: v for k, v in edl['sources'].items()}
H = int(os.environ.get('H', '1920')); W = H * 9 // 16   # H=3840 → exportação 4K
TAG = ('' if H == 1920 else f'_{H}') + ('' if EDLF == 'edl.json' else '_' + Path(EDLF).stem)
d_seg = E/f'clips_graded{TAG}'; d_seg.mkdir(exist_ok=True)
run = lambda c: subprocess.run(c, check=True)

def clean_bowl(vout, n):
    """Apaga os restos de sopa dentro da taça (mesa do jantar do Henrique; câmara fixa).
    Máscara pela cor (laranja saturado) dentro do interior da taça; preenchimento suave; borda intacta."""
    import numpy as np, cv2
    k = H / 3840; X0, Y0, X1, Y1 = [int(round(v*k)) for v in (100, 2250, 480, 2480)]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(vout), '-pix_fmt', 'bgr24', '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).copy()
    med = np.median(fr[:, Y0:Y1, X0:X1], 0).astype(np.uint8)
    hsv = cv2.cvtColor(med, cv2.COLOR_BGR2HSV)
    inner = np.zeros(med.shape[:2], np.uint8)
    cv2.ellipse(inner, (int(180*k), int(86*k)), (int(136*k), int(34*k)), 0, 0, 360, 1, -1)
    M = ((hsv[..., 1] > 115) & (hsv[..., 0] <= 30)).astype(np.uint8) & inner
    r7 = max(3, int(7*k) | 1)
    M = cv2.dilate(M, np.ones((r7, r7), np.uint8)) & inner
    fill = cv2.GaussianBlur(cv2.inpaint(cv2.GaussianBlur(med, (0, 0), 1.2*k), M*255, max(5, int(20*k)), cv2.INPAINT_TELEA), (0, 0), 2.5*k).astype(np.float32)
    A = cv2.GaussianBlur(M.astype(np.float32), (0, 0), 1.5*k)[..., None]
    reg = fr[:, Y0:Y1, X0:X1].astype(np.float32)
    fr[:, Y0:Y1, X0:X1] = (reg*(1-A) + fill*A).astype(np.uint8)
    cv2.imwrite(str(vout.with_suffix('.taca.png')), np.concatenate([med, fr[n//2, Y0:Y1, X0:X1]], 1))
    tmp = vout.with_suffix('.tmp.mp4')
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', str(tmp)], stdin=subprocess.PIPE)
    pr.stdin.write(fr.tobytes()); pr.stdin.close(); pr.wait(); tmp.replace(vout)
    print(f'    taça limpa: {int(M.sum())} px de sopa apagados')

vlist, alist, durs = [], [], []
for i, r in enumerate(edl['ranges']):
    s = src[r['source']]
    sp = r.get('speed', 1.0)  # >1 = mais rápido (o som mantém o tom)
    n = max(1, round((r['end'] - r['start']) / sp * FPS)); d = n / FPS; ns = round(d * SR)
    durs.append(d)
    vout, aout = d_seg/f'v_{i:02d}.mp4', d_seg/f'a_{i:02d}.wav'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]:.3f}', '-t', f'{d*sp+0.2:.3f}', '-i', s]
    crop = f"crop={r['crop']}," if r.get('crop') else ''  # aproximar (punch-in), ex. "1080:1920:240:600" na imagem 4K
    if r.get('zoom'):  # [z_inicio, z_fim]: aproximação lenta e suave (ease in-out) sobre o 4K
        z0, z1 = r['zoom']
        ez = f"({z0}+({z1}-{z0})*(1-cos(PI*min(on/{n},1)))/2)"
        base = f"zoompan=z='{ez}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS}"
    else:
        base = f'{crop}scale=-2:{H}'
    fc = [f'[0:v]{base},setpts=(PTS-STARTPTS)/{sp},fps={FPS}[b0]']; cur = '[b0]'  # acelerar ANTES de fixar os 30 fps
    for k, cw in enumerate(r.get('cutaways') or [], start=1):
        cs, cd, at = cw[:3]; csrc = src[cw[3]] if len(cw) > 3 else s   # 4.º elemento opcional: outra fonte
        if d - (at + cd) < 0.15: cd = d - at + 0.1  # B-roll a acabar mesmo no fim: cobre até ao último frame (evita 'flash')
        cmd += ['-ss', f'{cs:.3f}', '-t', f'{cd+0.2:.3f}', '-i', csrc]
        fc.append(f'[{k}:v]scale=-2:{H},fps={FPS},trim=duration={cd},setpts=PTS-STARTPTS+{at}/TB[c{k}]')
        fc.append(f"{cur}[c{k}]overlay=0:0:eof_action=pass:enable='between(t,{at},{at+cd-0.001})'[b{k}]"); cur = f'[b{k}]'
    fc.append(f'{cur}trim=end_frame={n},setpts=PTS-STARTPTS[v]')
    run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
               '-pix_fmt', 'yuv420p', '-r', str(FPS), str(vout)])
    vol = 'volume=0,' if r.get('mute') else ''
    acmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]+r.get('av_offset', AV_OFFSET):.3f}', '-t', f'{d*sp+0.2:.3f}', '-i', s]
    tempo = f'atempo={sp},' if sp != 1.0 else ''
    afc = [f'[0:a]aresample={SR},{tempo}{vol}apad,atrim=end_sample={ns}[m0]']; mix = ['[m0]']
    for k, (ls, ldur, at, gain) in enumerate(r.get('audio_layers') or [], start=1):
        acmd += ['-ss', f'{ls+r.get("av_offset", AV_OFFSET):.3f}', '-t', f'{ldur:.3f}', '-i', s]
        afc.append(f'[{k}:a]aresample={SR},volume={gain}dB,afade=t=in:d=0.08,afade=t=out:st={ldur-0.15:.3f}:d=0.15,'
                   f'adelay={int(at*1000)}:all=1,apad,atrim=end_sample={ns}[m{k}]'); mix.append(f'[m{k}]')
    afc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,atrim=end_sample={ns},"
               f'afade=t=in:st=0:d={FADE},afade=t=out:st={d-FADE:.4f}:d={FADE}[a]')
    if r.get('mute') and not r.get('audio_layers'):   # plano sem som (ex.: pedaços sem faixa de áudio) → silêncio exato
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r={SR}:cl=stereo', '-af', f'atrim=end_sample={ns}',
             '-c:a', 'pcm_s16le', str(aout)])
    else:
        run(acmd + ['-filter_complex', ';'.join(afc), '-map', '[a]', '-ac', '2', '-c:a', 'pcm_s16le', str(aout)])
    if r.get('bowl_clean'): clean_bowl(vout, n)
    vd = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(vout)]))
    assert abs(vd - d) < 0.02, f'segmento {i}: imagem {vd:.3f}s ≠ som {d:.3f}s'  # garante sincronização
    vlist.append(vout); alist.append(aout); print(f'  {i:02d} {d:.3f}s {r["quote"][:40]}', flush=True)
for name, lst in (('v', vlist), ('a', alist)):
    (d_seg/f'{name}_list.txt').write_text(''.join(f"file '{p}'\n" for p in lst))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(d_seg/'v_list.txt'), '-f', 'concat', '-safe', '0',
     '-i', str(d_seg/'a_list.txt'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(E/f'cuts{TAG}.mkv')])
json.dump(durs, open(d_seg/'durs.json', 'w'))
print(f'cuts{TAG}.mkv pronto: {sum(durs):.3f}s')
