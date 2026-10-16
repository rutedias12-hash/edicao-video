"""Corta o vídeo a partir de edl.json (como o render.py do video-use) e suporta 'cutaways':
imagens de outro momento por cima do som de um segmento (B-roll).
Cada range pode ter "cutaways": [[inicio_na_fonte, duracao, aos_x_segundos_do_segmento], ...]
Uso: python3 scripts/cut.py   → cuts.mp4"""
import json, subprocess, sys
from pathlib import Path
E = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(E.parent.parent / 'tools/video-use/helpers'))
from render import extract_segment, concat_segments  # noqa: E402

edl = json.load(open(E/'edl.json'))
src = {k: Path(v) for k, v in edl['sources'].items()}
segdir = E/'clips_graded'; segdir.mkdir(exist_ok=True)
paths = []
for i, r in enumerate(edl['ranges']):
    out = segdir/f'seg_{i:02d}_{r["source"]}.mp4'
    dur = r['end'] - r['start']
    extract_segment(src[r['source']], r['start'], dur, '', out, rate='30')
    cws = r.get('cutaways') or []
    if cws:
        tmp = out.with_suffix('.base.mp4'); out.rename(tmp)
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', str(tmp)]
        fc, cur = [], '[0:v]'
        for k, (s, d, at) in enumerate(cws, start=1):
            cmd += ['-ss', f'{s:.3f}', '-t', f'{d:.3f}', '-i', str(src[r['source']])]
            fc.append(f'[{k}:v]scale=-2:1920,fps=30,setpts=PTS-STARTPTS+{at}/TB[c{k}]')
            fc.append(f"{cur}[c{k}]overlay=0:0:enable='between(t,{at},{at+d-0.001})'[v{k}]"); cur = f'[v{k}]'
        cmd += ['-filter_complex', ';'.join(fc), '-map', cur, '-map', '0:a', '-c:v', 'libx264', '-preset', 'fast',
                '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'copy', '-movflags', '+faststart', str(out)]
        subprocess.run(cmd, check=True); tmp.unlink()
    paths.append(out); print(f'  seg {i:02d} ok ({dur:.2f}s{", cutaways" if cws else ""})', flush=True)
concat_segments(paths, E/'cuts.mp4', E)
print('cuts.mp4 pronto')
