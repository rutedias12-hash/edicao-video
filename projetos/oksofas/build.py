"""Monta a base do anúncio OK Sofás (9:16, 1080x1920, 30 fps).

Vídeo: extrai cada segmento (rotação/recorte + cor) → concat -c copy.
Áudio: só as vozes escolhidas, colocadas no tempo de saída, fades de 30 ms.
Sobreposições (HyperFrames, WebM com alfa): setpts deslocado para a janela.

  python edit/build.py base      # base.mp4 (vídeo + vozes)
  python edit/build.py final     # final.mp4 (base + overlays + loudness)
"""
import json, subprocess, sys
from pathlib import Path

ED = Path(__file__).resolve().parent
SRC = ED.parent
FPS = 30
LOUDNESS = -17        # LUFS (era -14; pedido para baixar o volume)
MUSIC_OFFSET = 25.82  # subida da faixa (29,24 s) cai no 1.º corte da montagem (3,42 s)
MUSIC_GAIN_DB = -8    # nível da música nas partes sem voz
MUSIC_DUCK_DB = -13   # quanto a música baixa enquanto ela fala
DUCK_WINDOWS = [(0.0, 3.42), (10.02, 18.58)]   # janelas de voz na saída
GRADE = "eq=contrast=1.04:saturation=1.06:gamma=1.01,colorbalance=rm=0.015:bm=-0.015"

ROT = "transpose=2"                     # horizontal filmado de cima → rodar 90° (encosto à esquerda)
ROT2 = "transpose=1"                    # 2.ª sala: rodar ao contrário para ela ficar de cabeça para cima
def crop(x):                            # recorte 9:16 de um plano horizontal 3840x2160
    return f"crop=1215:2160:{x}:0"

# (fonte, início, duração na saída, geometria, nota[, velocidade])
SEGMENTS = [
    ("IMG_6297", 1.12, 3.42, crop(1000), "gancho"),
    ("IMG_6298", 0.40, 1.00, ROT, "descansar"),
    ("IMG_6300", 0.90, 1.00, ROT, "ler"),
    ("IMG_6305", 3.00, 1.00, ROT, "trabalhar"),
    ("IMG_6306", 4.00, 1.00, ROT, "relaxar"),
    ("IMG_6301", 0.00, 1.00, ROT, "brincar"),
    ("IMG_6307", 2.70, 1.60, ROT2, "chaise redonda"),
    ("IMG_6302", 4.10, 2.76, crop(2400), "personalizamos"),
    ("IMG_6309", 4.60, 2.42, ROT2, "encosto ajustável"),
    ("IMG_6303", 0.80, 3.38, ROT, "arcas (2x: abre a arca e mexe lá dentro)", 2.0),
    ("IMG_6310", 10.30, 0.40, "", "stop 1 (fechado)"),
    ("IMG_6314", 2.00, 0.40, "", "stop 2"),
    ("IMG_6315", 3.00, 0.40, "", "stop 3"),
    ("IMG_6316", 1.80, 4.00, "", "stop 4 (cama) + fundo do cartão final"),
]

# (fonte, início, fim, início_na_saída[, ganho dB para igualar as vozes]) — limites com folga sobre as palavras
VOICE = [
    ("IMG_6297", 1.12, 4.54, 0.00, 2.0),     # E será que depois de seis meses ainda aconselhamos este sofá?
    ("IMG_6302", 4.10, 6.86, 10.02),    # nós personalizamos absolutamente tudo neste sofá,
    ("IMG_6302", 12.66, 15.08, 12.78),  # desde o comprimento, cor, arrumação,
    ("IMG_6303", 0.06, 3.44, 15.20, 4.0),    # Ele tem duas arcas escondidas nos braços do sofá.
]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def ffprobe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


def build_base():
    clips = ED / "clips_graded"; clips.mkdir(exist_ok=True)
    segs, t = [], 0.0
    for i, (src, ss, dur, geo, note, *spd) in enumerate(SEGMENTS):
        speed = spd[0] if spd else 1.0
        out = clips / f"seg_{i:02d}_{src}.mp4"
        vf = ",".join(p for p in [geo, f"setpts=PTS/{speed}" if speed != 1 else "", "scale=1080:1920:flags=lanczos", "setsar=1", GRADE] if p)
        print(f"  [{i:02d}] {t:6.2f}s  {src} {ss:.2f}+{dur:.2f}  {note}")
        run(["ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur * speed:.3f}", "-i", str(SRC / f"{src}.MOV"), "-t", f"{dur:.3f}",
             "-vf", vf, "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
             "-pix_fmt", "yuv420p", str(out)])
        segs.append(out); t += dur
    lst = ED / "_concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in segs))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(ED / "base_video.mp4")])

    # Vozes: cada uma com fades de 30 ms, atrasada para o tempo de saída e misturada
    inputs, parts = [], []
    for k, (src, a, b, at, *gain) in enumerate(VOICE):
        d = b - a
        inputs += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(SRC / f"{src}.MOV")]
        parts.append(f"[{k}:a]aresample=48000,volume={gain[0] if gain else 0}dB,afade=t=in:st=0:d=0.03,afade=t=out:st={d-0.03:.3f}:d=0.03,"
                     f"adelay={int(at*1000)}:all=1[v{k}]")
    mix = "".join(f"[v{k}]" for k in range(len(VOICE)))
    fc = ";".join(parts) + f";{mix}amix=inputs={len(VOICE)}:normalize=0,apad[a]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", "[a]", "-t", f"{t:.3f}",
         "-c:a", "pcm_s16le", str(ED / "voice.wav")])
    run(["ffmpeg", "-y", "-i", str(ED / "base_video.mp4"), "-i", str(ED / "voice.wav"),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(ED / "base.mp4")])
    print(f"base.mp4  {ffprobe_dur(ED / 'base.mp4'):.2f}s (esperado {t:.2f}s)")


def build_final():
    overlays = json.loads((ED / "overlays.json").read_text())
    inputs, fc, last = ["-i", str(ED / "base.mp4")], [], "0:v"
    for k, o in enumerate(overlays, start=1):
        inputs += ["-c:v", "libvpx-vp9", "-i", str(ED / o["file"])]
        st = o["start"]
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{st}/TB,format=yuva420p[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{st},{st + o['duration']})'[b{k}]")
        last = f"b{k}"
    fc.append(f"[{last}]format=yuv420p[vout]")
    # Música (opcional): assets/music.* — começa em MUSIC_OFFSET s da faixa, baixa sob as vozes
    # (sidechain), fade-out no fim. Depois normaliza tudo junto.
    music = sorted(ED.glob("assets/music.*"))
    if music:
        total = ffprobe_dur(ED / "base.mp4")
        k = len(overlays) + 1
        inputs += ["-ss", f"{MUSIC_OFFSET:.3f}", "-i", str(music[0])]
        g, r = 10 ** (MUSIC_DUCK_DB / 20), 0.25   # baixa a música nas janelas de voz, rampas de 0,25 s
        inside = "max(" * (len(DUCK_WINDOWS) - 1) + ",".join(
            f"clip(min((t-{a - r:.2f})/{r},({b + r:.2f}-t)/{r}),0,1)" + (")" if i else "")
            for i, (a, b) in enumerate(DUCK_WINDOWS))
        fc.append(f"[{k}:a]aresample=48000,volume={MUSIC_GAIN_DB}dB,atrim=0:{total:.3f},"
                  f"volume='1-{1 - g:.4f}*{inside}':eval=frame,"
                  f"afade=t=in:st=0:d=0.3,afade=t=out:st={total - 1.5:.3f}:d=1.5[md]")
        fc.append("[0:a][md]amix=inputs=2:normalize=0:duration=first[mix]")
        src_a = "mix"
    else:
        src_a = "0:a"
    fc.append(f"[{src_a}]loudnorm=I={LOUDNESS}:TP=-1.5:LRA=11[aout]")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(ED / "final.mp4")])
    print(f"final.mp4  {ffprobe_dur(ED / 'final.mp4'):.2f}s")


if __name__ == "__main__":
    {"base": build_base, "final": build_final}[sys.argv[1]]()
