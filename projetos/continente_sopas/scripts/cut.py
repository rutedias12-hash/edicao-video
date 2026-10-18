"""Corta o vídeo a partir de edl.json.
- Duração de cada plano arredondada a frames inteiros (30 fps) e som com exatamente as mesmas amostras → sem desvio acumulado.
- AV_OFFSET: o som da gravação original chega ~0,10 s atrasado (microfone sem fios; medido na porta a fechar aos 15,1 s),
  por isso o som de cada plano é lido 0,10 s mais à frente.
- "cutaways": [[inicio_na_fonte, duracao, aos_x_segundos_do_segmento], ...] — imagem de outro momento por cima do som (B-roll).
- "mute": true — plano sem som.
- "crop": "w:h:x:y" — aproximar a imagem (sobre o 4K original).
- "zoom": [z0, z1] — aproximação lenta (ease in-out).
- "speed": 1.25 — plano acelerado (duração final = (end-start)/speed).
- "audio_layers": [[inicio_na_fonte, duracao, aos_x_segundos, ganho_dB], ...] — som extra por baixo.
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
    sp = r.get('speed', 1.0)  # >1 = mais rápido (o som mantém o tom)
    n = max(1, round((r['end'] - r['start']) / sp * FPS)); d = n / FPS; ns = round(d * SR)
    durs.append(d)
    vout, aout = d_seg/f'v_{i:02d}.mp4', d_seg/f'a_{i:02d}.wav'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]:.3f}', '-t', f'{d*sp+0.2:.3f}', '-i', s]
    crop = f"crop={r['crop']}," if r.get('crop') else ''  # aproximar (punch-in), ex. "1080:1920:240:600" na imagem 4K
    if r.get('zoom'):  # [z_inicio, z_fim]: aproximação lenta e suave (ease in-out) sobre o 4K
        z0, z1 = r['zoom']
        ez = f"({z0}+({z1}-{z0})*(1-cos(PI*min(on/{n},1)))/2)"
        base = f"zoompan=z='{ez}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps={FPS}"
    else:
        base = f'{crop}scale=-2:1920,fps={FPS}'
    fc = [f'[0:v]{base},setpts=(PTS-STARTPTS)/{sp}[b0]']; cur = '[b0]'
    for k, (cs, cd, at) in enumerate(r.get('cutaways') or [], start=1):
        if d - (at + cd) < 0.15: cd = d - at + 0.1  # B-roll a acabar mesmo no fim: cobre até ao último frame (evita 'flash')
        cmd += ['-ss', f'{cs:.3f}', '-t', f'{cd+0.2:.3f}', '-i', s]
        fc.append(f'[{k}:v]scale=-2:1920,fps={FPS},trim=duration={cd},setpts=PTS-STARTPTS+{at}/TB[c{k}]')
        fc.append(f"{cur}[c{k}]overlay=0:0:eof_action=pass:enable='between(t,{at},{at+cd-0.001})'[b{k}]"); cur = f'[b{k}]'
    fc.append(f'{cur}trim=end_frame={n},setpts=PTS-STARTPTS[v]')
    run(cmd + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
               '-pix_fmt', 'yuv420p', '-r', str(FPS), str(vout)])
    vol = 'volume=0,' if r.get('mute') else ''
    acmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{r["start"]+AV_OFFSET:.3f}', '-t', f'{d*sp+0.2:.3f}', '-i', s]
    tempo = f'atempo={sp},' if sp != 1.0 else ''
    afc = [f'[0:a]aresample={SR},{tempo}{vol}apad,atrim=end_sample={ns}[m0]']; mix = ['[m0]']
    for k, (ls, ldur, at, gain) in enumerate(r.get('audio_layers') or [], start=1):
        acmd += ['-ss', f'{ls+AV_OFFSET:.3f}', '-t', f'{ldur:.3f}', '-i', s]
        afc.append(f'[{k}:a]aresample={SR},volume={gain}dB,afade=t=in:d=0.08,afade=t=out:st={ldur-0.15:.3f}:d=0.15,'
                   f'adelay={int(at*1000)}:all=1,apad,atrim=end_sample={ns}[m{k}]'); mix.append(f'[m{k}]')
    afc.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,atrim=end_sample={ns},"
               f'afade=t=in:st=0:d={FADE},afade=t=out:st={d-FADE:.4f}:d={FADE}[a]')
    run(acmd + ['-filter_complex', ';'.join(afc), '-map', '[a]', '-ac', '2', '-c:a', 'pcm_s16le', str(aout)])
    vlist.append(vout); alist.append(aout); print(f'  {i:02d} {d:.3f}s {r["quote"][:40]}', flush=True)
for name, lst in (('v', vlist), ('a', alist)):
    (d_seg/f'{name}_list.txt').write_text(''.join(f"file '{p}'\n" for p in lst))
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(d_seg/'v_list.txt'), '-f', 'concat', '-safe', '0',
     '-i', str(d_seg/'a_list.txt'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s16le', str(E/'cuts.mkv')])
json.dump(durs, open(d_seg/'durs.json', 'w'))
print(f'cuts.mkv pronto: {sum(durs):.3f}s')
