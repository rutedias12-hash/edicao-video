"""Póster "aves brancas" pintado: cada ave é feita de pinceladas (com pelos do pincel,
falhas de tinta e traço irregular), num fundo cor de areia também pintado.

Uso: python3 aves_pintura.py [teste]
"""
import math
import sys
import numpy as np
from PIL import Image, ImageDraw

FUNDO = np.array([229, 215, 190], np.float32) / 255
BRANCO = np.array([247, 243, 234], np.float32) / 255
ESCURO = np.array([58, 54, 50], np.float32) / 255
SOMBRA = np.array([214, 200, 176], np.float32) / 255

# x, y (fração), tamanho (fração da altura), rotação, asa de cima, asa de baixo, curva
AVES = [
    (0.15, 0.26, 0.30, -6, -52, 46, 0.22),
    (0.47, 0.48, 0.33, 10, -76, 40, 0.12),
    (0.76, 0.20, 0.26, -16, -42, 60, 0.24),
    (0.90, 0.66, 0.29, 4, -60, 34, 0.18),
    (0.19, 0.78, 0.27, -3, -34, 26, 0.26),
    (0.62, 0.86, 0.24, 18, -68, 54, 0.10),
]


def ruido(rng, h, w, escalas, aniso=1.0):
    total = np.zeros((h, w), np.float32)
    pt = 0
    for esc, peso in escalas:
        gh, gw = max(2, int(h / esc)), max(2, int(w / (esc * aniso)))
        base = rng.standard_normal((gh, gw)).astype(np.float32)
        total += np.asarray(Image.fromarray(base, "F").resize((w, h), Image.BICUBIC)) * peso
        pt += peso
    return total / pt


def _caixa(a, r, eixo):
    pad = [(0, 0), (0, 0)]
    pad[eixo] = (r + 1, r)
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=eixo, dtype=np.float32)
    n = a.shape[eixo]
    return (np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=eixo)
            - np.take(c, np.arange(n), axis=eixo)) / (2 * r + 1)


def blur(a, r):
    r = max(1, int(round(r * 0.9)))
    for _ in range(2):
        a = _caixa(_caixa(a, r, 0), r, 1)
    return a


def bezier(p0, c, p1, n=50):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1


class Tela:
    def __init__(self, W, H, seed):
        self.W, self.H = W, H
        self.u = H / 1000
        self.rng = np.random.default_rng(seed)
        self.img = np.empty((H, W, 3), np.float32)

    def pincelada(self, pts, larg, cor, opac=0.95, seco=0.35, variacao=0.06):
        """Pinta uma pincelada ao longo de pts (N,2) com largura larg (N,) em píxeis."""
        rng, u = self.rng, self.u
        n = len(pts)
        # tremor da mão
        trem = np.cumsum(rng.standard_normal((n, 2)), 0)
        trem -= np.linspace(0, 1, n)[:, None] * trem[-1]
        pts = pts + trem * 0.25 * u
        d = np.gradient(pts, axis=0)
        d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
        nrm = np.stack([-d[:, 1], d[:, 0]], 1)

        m = larg.max() + 6 * u
        x0, y0 = int(max(0, pts[:, 0].min() - m)), int(max(0, pts[:, 1].min() - m))
        x1, y1 = int(min(self.W, pts[:, 0].max() + m)), int(min(self.H, pts[:, 1].max() + m))
        if x1 <= x0 or y1 <= y0:
            return
        cob = Image.new("L", (x1 - x0, y1 - y0), 0)
        luz = Image.new("L", (x1 - x0, y1 - y0), 128)
        dc, dl = ImageDraw.Draw(cob), ImageDraw.Draw(luz)
        npelos = int(np.clip(larg.max() / (1.1 * u), 8, 140))
        esp = max(1, int(round(larg.max() / npelos * 2.0)))
        t = np.linspace(0, 1, n)
        for _ in range(npelos):
            f = rng.uniform(-0.5, 0.5)
            a = opac * rng.uniform(0.55, 1.0)
            # pelos das bordas acabam mais cedo; tinta a acabar no fim (pincel seco)
            fim = 1 - seco * rng.uniform(0, 1) * (0.3 + abs(f) * 1.4)
            ini = rng.uniform(0, 0.06) * (0.5 + abs(f))
            p = pts + nrm * (f * larg)[:, None] + rng.normal(0, 0.15 * u, (n, 2))
            p -= (x0, y0)
            keep = (t >= ini) & (t <= fim)
            # falhas de tinta ao longo do pelo
            falha = rng.uniform(0, 1, n) < seco * 0.25 * t ** 2
            seg = []
            for i in range(n):
                if keep[i] and not falha[i]:
                    seg.append(tuple(p[i]))
                elif len(seg) > 1:
                    dc.line(seg, fill=int(a * 255), width=esp, joint="curve")
                    dl.line(seg, fill=int(128 + rng.normal(0, 60)), width=esp)
                    seg = []
                else:
                    seg = []
            if len(seg) > 1:
                dc.line(seg, fill=int(a * 255), width=esp, joint="curve")
                dl.line(seg, fill=int(np.clip(128 + rng.normal(0, 60), 0, 255)), width=esp)
        c = blur(np.asarray(cob, np.float32) / 255, 0.7 * u)
        l = (blur(np.asarray(luz, np.float32), 0.7 * u) - 128) / 128
        reg = self.img[y0:y1, x0:x1]
        col = cor[None, None, :] * (1 + l[..., None] * variacao)
        reg[:] = reg * (1 - c[..., None]) + col * c[..., None]


def fundo(tela):
    H, W, u, rng = tela.H, tela.W, tela.u, tela.rng
    manchas = ruido(rng, H, W, [(400 * u, 1.0), (150 * u, 0.6)])
    grao = ruido(rng, H, W, [(1.5 * u, 1.0)])
    trama = (np.sin(np.arange(W) * 2 * math.pi / (3.2 * u))[None, :] +
             np.sin(np.arange(H) * 2 * math.pi / (3.2 * u))[:, None]) * 0.5
    luz = 1 + 0.03 * (1 - np.linspace(0, 1, H))[:, None]
    tela.img[:] = FUNDO * (luz + manchas * 0.03 + grao * 0.012 + trama * 0.006)[..., None]
    # pinceladas largas de fundo, quase horizontais, em tons de areia
    for _ in range(int(220)):
        x = rng.uniform(-0.1, 1.0) * W
        y = rng.uniform(0, 1) * H
        comp = rng.uniform(0.15, 0.45) * H
        ang = rng.normal(0, 0.12)
        p0 = np.array([x, y])
        p1 = p0 + comp * np.array([math.cos(ang), math.sin(ang)])
        c = (p0 + p1) / 2 + rng.normal(0, 0.03 * H, 2)
        pts = bezier(p0, c, p1, 30)
        larg = np.full(30, rng.uniform(25, 70) * u) * (1 - 0.3 * np.linspace(0, 1, 30))
        tom = FUNDO * rng.uniform(0.975, 1.035) + rng.normal(0, 0.006, 3)
        tela.pincelada(pts, larg, tom.astype(np.float32), opac=rng.uniform(0.25, 0.55),
                       seco=0.8, variacao=0.03)


def ave(tela, x, y, tam, rot, a_cima, a_baixo, curva):
    rng, W, H = tela.rng, tela.W, tela.H
    s = tam * H
    r = math.radians(rot)
    M = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
    cen = np.array([x * W, y * H])

    def T(p):
        return (np.asarray(p) @ M.T) * s + cen

    def pinta(p0, c, p1, w0, w1, cor, n=45, **kw):
        pts = T(bezier(np.array(p0), np.array(c), np.array(p1), n))
        t = np.linspace(0, 1, n)
        larg = (w0 * (1 - t ** 2.2) + w1 * t ** 2.2) * s
        tela.pincelada(pts, larg, cor, **kw)

    pontas = []
    for ang, cv in ((a_cima, curva), (a_baixo, -curva)):
        a = math.radians(ang)
        dirc = np.array([math.cos(a), math.sin(a)])
        perp = np.array([-dirc[1], dirc[0]])
        ombro = np.array([-0.12, 0.0])
        ponta = ombro + 0.80 * dirc
        pontas.append((ombro, ponta, dirc, perp, cv))
        # sombra ligeira por baixo (tinta castanha a espreitar)
        for k in range(5):
            off = (k - 2) * 0.045
            base = ombro + perp * off * 1.3 + dirc * 0.02 * abs(k - 2)
            fim = ponta - dirc * (0.06 * abs(k - 2)) + perp * off * 0.35
            c = (base + fim) / 2 + perp * (cv * 0.9 + off * 0.3) + rng.normal(0, 0.008, 2)
            pinta(base, c, fim, 0.10, 0.04, BRANCO, opac=0.97, seco=0.22)
    # corpo, cabeça e cauda
    for k in range(3):
        off = (k - 1) * 0.045
        pinta((-0.48, off * 0.6), (-0.1, off * 1.3), (0.22, off * 1.4), 0.10, 0.11, BRANCO, seco=0.18)
    for k in range(3):
        ang = (k - 1) * 0.16
        pinta((0.40, ang * 0.7), (0.25, ang * 0.4), (0.08, ang * 0.2), 0.10, 0.11, BRANCO, n=25, seco=0.15)
    pinta((-0.54, 0), (-0.46, 0), (-0.36, 0), 0.10, 0.15, BRANCO, n=15, seco=0.05)
    # pontas escuras das asas e bico
    for ombro, ponta, dirc, perp, cv in pontas:
        for k in range(3):
            off = (k - 1) * 0.022
            ini = ombro + 0.72 * (ponta - ombro) + perp * (cv * 0.16 + off)
            fim = ponta + dirc * 0.035 + perp * off * 0.3
            c = (ini + fim) / 2 + perp * cv * 0.06
            pinta(ini, c, fim, 0.06, 0.012, ESCURO, n=25, opac=0.92, seco=0.55, variacao=0.15)
    pinta((-0.50, 0), (-0.55, 0), (-0.62, 0.0), 0.04, 0.008, ESCURO, n=12, opac=0.9, seco=0.2,
          variacao=0.15)


def render(nome, W, H):
    tela = Tela(W, H, seed=11)
    fundo(tela)
    for a in AVES:
        ave(tela, *a)
    img = (np.clip(tela.img, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(img).save(nome, dpi=(300, 300))
    print(nome, W, H)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teste":
        render("pintura_teste.png", 1400, 1000)
    else:
        render("aves_pintura_70x50.png", 7000, 5000)
        render("aves_pintura_40x30.png", 4724, 3543)
        render("aves_pintura_A4.png", 3508, 2480)
