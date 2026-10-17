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
MUSIC_OFFSET = 13.10  # subida da faixa (29,24 s) cai quando aparece o sofá-cama (16,14 s)
MUSIC_GAIN_DB = -8    # nível da música nas partes sem voz
MUSIC_DUCK_DB = -13   # quanto a música baixa enquanto ela fala
DUCK_WINDOWS = [(0.0, 19.00)]   # a voz é contínua do início até "aconselhamos."
GRADE = "eq=contrast=1.04:saturation=1.06:gamma=1.01,colorbalance=rm=0.015:bm=-0.015"

ROT = "transpose=2"                     # horizontal filmado de cima → rodar 90° (encosto à esquerda)
ROT2 = "transpose=1"                    # 2.ª sala: rodar ao contrário para ela ficar de cabeça para cima
def crop(x):                            # recorte 9:16 de um plano horizontal 3840x2160
    return f"crop=1215:2160:{x}:0"

# Gancho: começa ~2,2x aproximado na cara dela e afasta (ease-in-out cúbico em 1,8 s) até ao plano 9:16 completo.
# Sobe a resolução antes do zoompan para o movimento não "tremer".
_P = "min(on/54,1)"; _E = f"if(lt({_P},0.5),4*pow({_P},3),1-pow(-2*{_P}+2,3)/2)"
ZOOM_OUT = (crop(1000) + ",scale=2430:4320:flags=lanczos,fps=30,"
            f"zoompan=z='2.2-1.2*{_E}':x='(iw-iw/zoom)/2':"
            f"y='max(0,min(ih-ih/zoom,(0.26+0.24*{_E})*ih-ih/zoom/2))':d=1:s=1080x1920:fps=30")

# (fonte, início, duração na saída, geometria, nota[, velocidade])
SEGMENTS = [
    ("IMG_6297", 1.18, 3.42, ZOOM_OUT, "gancho (zoom out)"),
    ("IMG_6298", 0.40, 1.35, ROT, "descansar"),
    ("IMG_6300", 0.90, 1.35, ROT, "ler"),
    ("IMG_6305", 3.00, 1.35, ROT, "trabalhar"),
    ("IMG_6306", 4.00, 1.35, ROT, "relaxar"),
    ("IMG_6303", 0.80, 3.48, ROT, "arcas (2x: abre a arca e mexe lá dentro)", 2.0),
    ("IMG_6307", 2.70, 1.10, ROT2, "chaise redonda  ← \"Chaise longue redonda\""),
    ("IMG_6309", 4.60, 1.32, ROT2, "encosto ajustável  ← \"encosto de cabeça ajustável\""),
    ("IMG_6310", 10.30, 0.47, "", "stop 1 (fechado)  ← \"transforma-se\""),
    ("IMG_6314", 2.00, 0.47, "", "stop 2"),
    ("IMG_6315", 3.00, 0.48, "", "stop 3"),
    ("IMG_6316", 1.80, 1.26, "", "stop 4 (cama) ← \"cama\""),
    ("SPLIT", 0.0, 2.60, "", "ecrã dividido em 3: ler / relaxar / trabalhar ← \"Por isso, claro que aconselhamos.\""),
]

# (fonte, início, fim, início_na_saída[, ganho dB para igualar as vozes]) — limites com folga sobre as palavras
FECHO_DB = 10.5   # ganho da nota de voz para igualar as falas do vídeo (~-17 dB RMS)
VOICE = [
    ("IMG_6297", 1.18, 4.60, 0.00, 2.0),     # E será que depois de seis meses ainda aconselhamos este sofá?
    ("IMG_6302", 4.10, 6.86, 3.52),          # nós personalizamos absolutamente tudo neste sofá,  (sobre as atividades)
    ("IMG_6302", 12.66, 15.08, 6.28),        # desde o comprimento, cor, arrumação,
    ("IMG_6303", 0.06, 3.44, 8.87, 4.0),     # Ele tem duas arcas escondidas nos braços do sofá.
    # Gravação de fecho (nota de voz, 3.ª versão): partida entre "redonda," e "encosto"; pausas encurtadas
    ("fecho/fecho.m4a", 15.80, 16.74, 12.36, FECHO_DB - 4),   # Chaise longue redonda,
    ("fecho/fecho.m4a", 16.74, 20.90, 13.36, FECHO_DB + 1),   # encosto de cabeça ajustável e transforma-se de sofá a cama sem esforço.
    ("fecho/fecho.m4a", 22.56, 24.06, 17.50, FECHO_DB + 4),   # Por isso, claro que aconselhamos.
]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def ffprobe_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode())


# Ecrã dividido: 3 faixas 1080x640 com os planos horizontais originais (ela deitada ao comprido),
# a entrar uma de cada vez de cima para baixo, alternando o lado (esq., dir., esq.), ease-out cúbico.
SPLIT_PANELS = [("IMG_6300", 4.0, "ler", -1), ("IMG_6306", 6.0, "relaxar", 1), ("IMG_6305", 8.0, "trabalhar", -1)]
CLEAN = {"IMG_6310", "IMG_6314", "IMG_6315", "IMG_6316"}   # stop-motion: tirar as manchas do tecido (tools/manchas.py)
SPLIT_STEP, SPLIT_SLIDE = 0.40, 0.45


def make_split(out, dur, bg_clip):
    # fundo: o último frame do sofá-cama (já limpo) parado, enquanto as faixas entram
    inputs = ["-sseof", "-0.05", "-i", str(bg_clip)]
    fc = [f"[0:v]tpad=stop_mode=clone:stop_duration={dur + 1:.2f},trim=duration={dur:.3f},setpts=PTS-STARTPTS[bg]"]
    last = "bg"
    for k, (src, ss, _, side) in enumerate(SPLIT_PANELS, start=1):
        inputs += ["-ss", f"{ss:.3f}", "-t", f"{dur:.3f}", "-i", str(SRC / f"{src}.MOV")]
        fc.append(f"[{k}:v]crop=3645:2160,scale=1080:640:flags=lanczos,setsar=1,fps={FPS},{GRADE}[p{k}]")
        t0 = (k - 1) * SPLIT_STEP
        e = f"(1-pow(1-min(max((t-{t0})/{SPLIT_SLIDE},0),1),3))"
        x = f"{side}*1080*(1-{e})"
        fc.append(f"[{last}][p{k}]overlay=x='{x}':y={(k - 1) * 640}:eof_action=pass[s{k}]")
        last = f"s{k}"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-t", f"{dur:.3f}",
         "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(out)])


def build_base():
    clips = ED / "clips_graded"; clips.mkdir(exist_ok=True)
    segs, t = [], 0.0
    for i, (src, ss, dur, geo, note, *spd) in enumerate(SEGMENTS):
        speed = spd[0] if spd else 1.0
        out = clips / f"seg_{i:02d}_{src}.mp4"
        if src == "SPLIT":
            print(f"  [{i:02d}] {t:6.2f}s  {note}")
            make_split(out, dur, segs[-1]); segs.append(out); t += dur
            continue
        vf = ",".join(p for p in [geo, f"setpts=PTS/{speed}" if speed != 1 else "", "scale=1080:1920:flags=lanczos", "setsar=1", GRADE] if p)
        print(f"  [{i:02d}] {t:6.2f}s  {src} {ss:.2f}+{dur:.2f}  {note}")
        run(["ffmpeg", "-y", "-ss", f"{ss:.3f}", "-t", f"{dur * speed:.3f}", "-i", str(SRC / f"{src}.MOV"), "-t", f"{dur:.3f}",
             "-vf", vf, "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "17",
             "-pix_fmt", "yuv420p", str(out)])
        if src in CLEAN:
            raw = out.with_name(out.stem + "_manchas.mp4")
            out.replace(raw)
            subprocess.run([sys.executable, str(ED / "tools" / "manchas.py"), str(raw), str(out)], check=True)
        segs.append(out); t += dur
    lst = ED / "_concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in segs))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(ED / "base_video.mp4")])

    # Vozes: cada uma com fades de 30 ms, atrasada para o tempo de saída e misturada
    inputs, parts = [], []
    for k, (src, a, b, at, *gain) in enumerate(VOICE):
        d = b - a
        inputs += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(SRC / (src if "." in src else f"{src}.MOV"))]
        parts.append(f"[{k}:a]aresample=48000,highpass=f=80,volume={gain[0] if gain else 0}dB,alimiter=limit=0.89:level=0,afade=t=in:st=0:d=0.03,afade=t=out:st={d-0.03:.3f}:d=0.03,"
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
