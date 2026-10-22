"""Póster "aves brancas": pintura em tons de areia com aves estilizadas.

Uso: python3 aves.py  ->  gera aves_70x50.png, aves_40x30.png, aves_A4.png
"""
import math
import numpy as np
from PIL import Image, ImageDraw

RNG = np.random.default_rng(7)

FUNDO = np.array([229, 215, 190], np.float32) / 255
AVE = np.array([246, 241, 231], np.float32) / 255
PONTA = np.array([62, 58, 53], np.float32) / 255
CONTORNO = np.array([196, 178, 150], np.float32) / 255

# (x, y) em fração da largura/altura, tamanho em fração da altura,
# rotação (graus), ângulo da asa de cima e da asa de baixo, curva das asas.
AVES = [
    (0.15, 0.25, 0.28, -6, -50, 48, 0.20),
    (0.46, 0.48, 0.32, 10, -78, 42, 0.10),
    (0.75, 0.20, 0.25, -16, -40, 62, 0.24),
    (0.91, 0.64, 0.28, 4, -62, 36, 0.16),
    (0.18, 0.77, 0.26, -3, -32, 24, 0.26),
    (0.62, 0.86, 0.23, 18, -70, 55, 0.08),
]


def ruido(h, w, escalas, aniso=1.0):
    """Ruído suave (soma de várias escalas), valores aprox. -1..1."""
    total = np.zeros((h, w), np.float32)
    peso_total = 0
    for esc, peso in escalas:
        gh = max(2, int(h / esc))
        gw = max(2, int(w / (esc * aniso)))
        base = RNG.standard_normal((gh, gw)).astype(np.float32)
        img = Image.fromarray(base, "F").resize((w, h), Image.BICUBIC)
        total += np.asarray(img) * peso
        peso_total += peso
    return total / peso_total


def _caixa(a, r, eixo):
    pad = [(0, 0), (0, 0)]
    pad[eixo] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=eixo, dtype=np.float32)
    n = a.shape[eixo]
    fim = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=eixo)
    ini = np.take(c, np.arange(0, n), axis=eixo)
    return (fim - ini) / (2 * r + 1)


def blur(a, r):
    """Desfocagem aproximadamente gaussiana (3 passagens de caixa)."""
    r = max(1, int(round(r * 0.9)))
    a = a.astype(np.float32)
    for _ in range(3):
        a = _caixa(_caixa(a, r, 0), r, 1)
    return a


def bezier(p0, c, p1, n=60):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1, t[:, 0]


def asa(ombro, angulo, comp, largura, curva):
    a = math.radians(angulo)
    p0 = np.array(ombro)
    p1 = p0 + comp * np.array([math.cos(a), math.sin(a)])
    meio = (p0 + p1) / 2
    perp = np.array([-math.sin(a), math.cos(a)])
    c = meio + perp * curva * comp
    pts, t = bezier(p0, c, p1)
    d = np.gradient(pts, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    w = largura * (1 - t ** 1.8) ** 0.7 * (1 + 0.35 * (1 - t) ** 2)
    lado_a = pts + nrm * w[:, None] / 2
    lado_b = pts - nrm * w[:, None] / 2
    poli = np.vstack([lado_a, lado_b[::-1]])
    # ponta escura: último bocado da asa
    k = int(len(t) * 0.80)
    ponta = np.vstack([lado_a[k:], lado_b[k:][::-1]])
    return poli, ponta


def corpo():
    cima = [(-0.56, 0.0), (-0.50, -0.045), (-0.40, -0.085), (-0.20, -0.095),
            (0.08, -0.08), (0.22, -0.075), (0.40, -0.12)]
    baixo = [(0.42, 0.0), (0.40, 0.12), (0.22, 0.075),
             (0.08, 0.08), (-0.20, 0.10), (-0.40, 0.085), (-0.50, 0.045)]
    return np.array(cima + baixo)


def bico():
    return np.array([(-0.62, 0.0), (-0.50, -0.035), (-0.48, 0.0), (-0.50, 0.035)])


def transforma(p, cx, cy, s, rot):
    r = math.radians(rot)
    m = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
    return (p @ m.T) * s + np.array([cx, cy])


def render(nome, W, H):
    mask = Image.new("L", (W, H), 0)
    tips = Image.new("L", (W, H), 0)
    dm, dt = ImageDraw.Draw(mask), ImageDraw.Draw(tips)
    for x, y, tam, rot, a_cima, a_baixo, curva in AVES:
        s = tam * H
        cx, cy = x * W, y * H
        partes = [corpo()]
        pontas = [bico()]
        for ang, cv in ((a_cima, curva), (a_baixo, -curva)):
            poli, ponta = asa((-0.09, 0.0), ang, 0.80, 0.30, cv)
            partes.append(poli)
            pontas.append(ponta)
        for p in partes:
            dm.polygon([tuple(q) for q in transforma(p, cx, cy, s, rot)], fill=255)
        for p in pontas:
            dt.polygon([tuple(q) for q in transforma(p, cx, cy, s, rot)], fill=255)

    u = H / 1000  # unidade de escala
    m = np.asarray(mask, np.float32) / 255
    t = np.asarray(tips, np.float32) / 255

    # bordas irregulares, como pinceladas
    borda = ruido(H, W, [(30 * u, 1.0), (10 * u, 0.25)])
    m = blur(m, 3 * u) + borda * 0.15
    m = np.clip((m - 0.5) / 0.12 + 0.5, 0, 1)
    tb = blur(t, 1.2 * u)
    t = tb + ruido(H, W, [(10 * u, 1.0)]) * 0.12 * np.clip(tb * 4, 0, 1)
    t = np.clip((t - 0.5) / 0.15 + 0.5, 0, 1) * m

    # contorno castanho ligeiro, desviado (como tinta por baixo)
    sh = max(1, int(3 * u))
    desvio = np.zeros_like(m)
    desvio[sh:, sh:] = m[:-sh, :-sh]
    cont = np.clip(desvio - m, 0, 1)
    cont = blur(cont, 1.5 * u) * 0.45

    # fundo: manchas largas + pinceladas horizontais + grão de tela
    manchas = ruido(H, W, [(400 * u, 1.0), (160 * u, 0.6)])
    pinc = ruido(H, W, [(25 * u, 1.0), (70 * u, 0.7)], aniso=4)
    grao = ruido(H, W, [(1.5 * u, 1.0)])
    trama = (np.sin(np.arange(W) * 2 * math.pi / (3.2 * u))[None, :] +
             np.sin(np.arange(H) * 2 * math.pi / (3.2 * u))[:, None]) * 0.5
    luz = 1 + 0.035 * (1 - np.linspace(0, 1, H))[:, None]  # mais claro em cima
    fundo = FUNDO[None, None, :] * (luz + manchas * 0.035 + pinc * 0.022
                                     + grao * 0.012 + trama * 0.006)[..., None]
    # salpicos claros de textura (tinta mais espessa)
    claro = np.clip(ruido(H, W, [(12 * u, 0.6), (45 * u, 1.0)], aniso=2.5) - 0.45, 0, 1) * 0.22
    fundo = fundo + (np.array([1, 0.98, 0.94])[None, None, :] - fundo) * claro[..., None]

    # tinta branca das aves com pinceladas
    pa = ruido(H, W, [(12 * u, 1.0), (40 * u, 0.6)], aniso=2)
    ave = AVE[None, None, :] * (1 + pa * 0.018 + grao * 0.01 + trama * 0.004)[..., None]
    # um pouco de transparência irregular, deixa ver o fundo
    cob = np.clip(0.93 + ruido(H, W, [(25 * u, 1.0)]) * 0.08, 0.8, 1)
    ave = ave * cob[..., None] + fundo * (1 - cob[..., None])

    ponta = PONTA[None, None, :] * (1 + pa * 0.15)[..., None]

    img = fundo * (1 - cont[..., None]) + CONTORNO[None, None, :] * cont[..., None]
    img = img * (1 - m[..., None]) + ave * m[..., None]
    img = img * (1 - t[..., None]) + ponta * t[..., None]
    img = (np.clip(img, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(img).save(nome, dpi=(300, 300))
    print(nome, W, H)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        render("aves_teste.png", 1400, 1000)
    else:
        render("aves_70x50.png", 8268, 5906)
        render("aves_40x30.png", 4724, 3543)
        render("aves_A4.png", 3508, 2480)
