"""Corta o vídeo a partir de edl.json.
- Duração de cada plano arredondada a frames inteiros (30 fps) e som com exatamente as mesmas amostras → sem desvio acumulado.
- AV_OFFSET: o som da gravação original chega ~0,10 s atrasado (microfone sem fios; medido na porta a fechar aos 15,1 s),
  por isso o som de cada plano é lido 0,10 s mais à frente.
- "cutaways": [[inicio_na_fonte, duracao, aos_x_segundos_do_segmento], ...] — imagem de outro momento por cima do som (B-roll).
- "mute": true — plano sem som.
- "crop": "w:h:x:y" — aproximar a imagem (sobre o 4K original).
Uso: python3 scripts/cut.py   → cuts.mp4"""
import json, subprocess
from pathlib import Path
E = Path(__file__).resolve().parent.parent
FPS, SR, AV_OFFSET, FADE = 30, 48000, 0.10, 0.03
edl = json.load(open(E/'edl.json'))
src = {k: v for k, v in edl['sources'].items()}
d_seg = E/'clips_graded'; d_seg.mkdir(exist_ok=True)
run = lambda c: subprocess.run(c, check=True)
vlist, alist, durs = [], [], []
for i, r in enumerate(edl['ranges']):
    s = src[r['source']]
    n = max(1, round((r['end'] - r['start']) * FPS)); d = n / FPS; ns = round(d * SR)
    durs.append(d)
    vout, aout = d_seg/f'v_{i:02d}.mp4', d_seg/f'a_{i:02d}.wav'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]:.3f}', '-t', f'{d+0.2:.3f}', '-i', s]
    crop = f"crop={r['crop']}," if r.get('crop') else ''  # aproximar (punch-in), ex. "1080:1920:240:600" na imagem 4K
    fc = [f'[0:v]{crop}scale=-2:1920,fps={FPS},setpts=PTS-STARTPTS[b0]']; cur = '[b0]'
    for k, (cs, cd, at) in enumerate(r.get('cutaways') or [], start=1):
        cmd += ['-ss', f'{cs:.3f}', '-t', f'{cd+0.2:.3f}', '-i', s]
        fc.append(f'[{k}:v]scale=-2:1920,fps={FPS},trim=duration={cd},setpts=PTS-STARTPTS+{at}/TB[c{k}]')
        fc.append(f"{cur}[c{k}]overlay=0:0:eof_action=pass:enable='between(t,{at},{at+cd-0.001})'[b{k}]"); cur = f'[b{k}]'
    fc.append(f'{cur}trim=end_frame={n},setpts=PTS-STARTPTS[v]')
    run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
               '-pix_fmt', 'yuv420p', '-r', str(FPS), str(vout)])
    vol = 'volume=0,' if r.get('mute') else ''
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]+AV_OFFSET:.3f}', '-t', f'{d+0.2:.3f}', '-i', s, '-vn',
         '-af', f'aresample={SR},{vol}apad,atrim=end_sample={ns},afade=t=in:st=0:d={FADE},afade=t=out:st={d-FADE:.4f}:d={FADE}',
         '-ac', '2', '-c:a', 'pcm_s16le', str(aout)])
    vlist.append(vout); alist.append(aout); print(f'  {i:02d} {d:.3f}s {r["quote"][:40]}', flush=True)
for name, lst in (('v', vlist), ('a', alist)):
    (d_seg/f'{name}_list.txt').write_text(''.join(f"file '{p}'\n" for p in lst))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(d_seg/'v_list.txt'), '-f', 'concat', '-safe', '0',
     '-i', str(d_seg/'a_list.txt'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(E/'cuts.mkv')])
json.dump(durs, open(d_seg/'durs.json', 'w'))
print(f'cuts.mkv pronto: {sum(durs):.3f}s')
