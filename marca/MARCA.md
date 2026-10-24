# Marca Rute Dias — manual para a edição

Fonte de verdade: `marca/fontes/guia-de-marca.png` (branding sheet).
Fontes e guia são descarregados por `bash marca/download.sh` (corre também no `setup.sh`).
Variáveis prontas a usar: `marca/marca.css`. Ecrã de exemplo (com o título a escrever-se): `marca/exemplo.html`.

**Estilo nos vídeos (decidido pela Rute):** **simples**, ao estilo dos vlogs de referência.
Sem sombras, sem caixas enfeitadas, animações mínimas.
**Logótipo:** não há.

## Cores
| Nome | Código | Para quê |
|---|---|---|
| Winter White | `#F2EFE6` | Fundo principal, capas, ecrãs de título, espaço negativo |
| Champagne | `#E8D8C5` | Fundos alternativos, caixas de texto, elementos gráficos, contraste suave |
| Espresso | `#493A33` | Texto principal, subtítulos, linhas e ícones |
| Cherry Burgundy | `#6F172B` | Só destaques: palavras-chave, sublinhados, chamadas, assinatura |

Regras:
- Usar apenas estas quatro cores. Nada de branco puro, preto puro ou cores fora da paleta.
- O Burgundy é a cor de assinatura: usar pouco (uma palavra ou um detalhe por ecrã) para manter o impacto.
- Texto sobre o vídeo: diretamente sobre a imagem, **sem sombra e sem caixa**. **Texto base (legendas, horas,
  rótulos) sempre claro: Winter White** — nunca castanho. Escolher a posição do texto onde o fundo é mais
  escuro, em vez de mudar a cor ou pôr sombra.
- **Tons escuros (Espresso, Burgundy) só em destaques.**
- **Regra do destaque:** a cor de destaque é o Cherry Burgundy. **Quando o burgundy não se lê** sobre a imagem
  (fundo escuro ou avermelhado), usa-se **Champagne**. Teste: contraste de pelo menos 3:1 entre a cor e
  as partes **mais escuras** do fundo por trás do texto (20.º percentil); se o burgundy não chegar, Champagne.
- **Títulos do yapping sobre caixa** (exceção à regra "sem caixa", pedida pela Rute): o título do gancho e os títulos
  de secção ficam sobre uma **caixa retangular Burgundy**, cheia e de cantos retos, que aparece inteira quando o título
  começa a escrever-se. Letras numa cor fixa: maiúsculas **Winter White**, palavra em Sloop **Champagne**.
  Nunca mudar a cor das letras conforme o fundo (a Rute não gostou).
- Destaques nas legendas: Espresso ou Burgundy; se o tom escuro não chegar a 3:1 sobre as partes mais escuras
  do fundo, Champagne. Implementado em `marca/exemplo.html`.

## Tipografia (vídeos)
Guia: Sloop (títulos, destaques, assinaturas) + sans serif (subtítulos, corpo, informação).
**A sans serif dos vídeos é a Montserrat** (escolha da Rute; substitui a Proxima Nova e a "Sistema").

| Formato | Títulos | Legendas e texto | Destaques |
|---|---|---|---|
| **Vlog** | Montserrat | Montserrat | algumas palavras na mesma fonte num tom escuro da paleta; outras em Sloop |
| **Yapping** | Montserrat maiúsculas + palavra principal em Sloop por cima; secções em Montserrat Regular | Montserrat | Sloop |

- **Sloop só no yapping** (palavra principal do título e destaques), **nunca engrossada** (sem negrito). No vlog, a única exceção são algumas palavras das legendas.
- **Sloop:** "Sloop Script Regular.ttf", no Drive da Rute (descarregada por `marca/download.sh`). Tem todos os acentos.
- **Letras e linhas apertadas** (pedido da Rute): espaçamento entre letras -0,06 em nos títulos,
  -0,035 em no texto, 0,04 em nos rótulos em maiúsculas; altura de linha 0,78 nos títulos, 1,2 no texto.

Para vídeo horizontal 1920×1080, multiplicar os tamanhos por ~0,75.

## Margens de segurança (Reels do Instagram)
Todo o texto tem de ficar **dentro da zona segura** do vídeo 1080×1920, para não ficar tapado pela interface:
- **cima: 220 px** (nome da conta, áudio);
- **baixo: 420 px** (legenda do post, nome, botões);
- **direita: 120 px** (coluna de ícones: gosto, comentar, partilhar);
- **esquerda: 60 px**.
Valores em `marca/marca.css` (`--seg-topo`, `--seg-base`, `--seg-dir`, `--seg-esq`). O título ajusta o tamanho para caber
(com o cursor) entre a margem esquerda e a coluna de ícones. Antes de renderizar, verificar num frame de cada
elemento que nenhum píxel de texto (acentos e caudas incluídos) sai da zona segura.

## Animações (só duas)
1. **Títulos: máquina de escrever.** O texto escreve-se letra a letra (~14 letras por segundo) com uma
   **barra de cursor** fina (`|`, mesma cor do texto, ~0,08 em de largura) à frente. Quando acaba, o cursor
   pisca 2–3 vezes (ligado 0,5 s / desligado 0,5 s) e desaparece. Durante a escrita toca o som
   **`marca/sons/teclado.wav`**, cortado à duração da escrita (desvanecimento de 0,05 s no fim).
2. **Tudo o resto: só aparecer.** (As legendas mostram uma palavra de cada vez; cada palavra só aparece e só desaparece.) Legendas, horas, rótulos, listas, imagens: entram de uma vez (sem
   desvanecer, sem deslizar, sem crescer) e saem de uma vez.

Proibido: sombras, contornos, brilhos, ressaltos, zooms, rotações, linhas que se desenham.
**Exceção:** os vídeos de yapping começam com um **zoom in** suave no gancho, que volta atrás no fim do gancho (ver `FORMATOS.md`).

## Atenção às licenças
- **Montserrat**: livre (Google Fonts, licença OFL).
- **Sloop Script** (Synergie SoftWare, 1999): confirmar que a licença permite uso comercial em vídeo.
Por isso as fontes **não** vão para o GitHub (o repositório é público); ficam só no Drive.
