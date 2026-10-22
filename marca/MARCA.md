# Marca Rute Dias — manual para a edição

Fonte de verdade: `marca/fontes/guia-de-marca.png` (branding sheet).
Fontes e guia são descarregados por `bash marca/download.sh` (corre também no `setup.sh`).
Variáveis prontas a usar: `marca/marca.css`. Ecrã de exemplo (com o título a escrever-se): `marca/exemplo.html`.

**Estilo nos vídeos (decidido pela Rute):** **simples**, ao estilo dos vlogs de referência.
Letra sans serif, sem sombras, sem caixas enfeitadas, animações mínimas.
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
- Texto sobre o vídeo: diretamente sobre a imagem, **sem sombra e sem caixa**. Winter White por defeito;
  Espresso quando o fundo é claro. Escolher o plano/posição para o texto se ler bem, em vez de pôr sombra.

## Tipografia (vídeos)
**Só Hind Siliguri** (sans serif). La Luxes e New Icon Script **não** se usam nos vídeos
(a Rute não gostou do resultado); ficam só para outros materiais da marca.

| Função | Peso | Tamanho em vídeo 1080×1920 |
|---|---|---|
| Título | SemiBold | 64–80 px, minúsculas (frase normal) |
| Hora / número | Medium | 44 px |
| Rótulo pequeno | Medium, maiúsculas, espaçamento ≈0,3em | 22–26 px |
| Legendas e texto | Regular | 34–40 px (vlog); 60–68 px SemiBold (yapping, palavra a palavra) |

Para vídeo horizontal 1920×1080, multiplicar os tamanhos por ~0,75.

## Animações (só duas)
1. **Títulos: máquina de escrever.** O texto escreve-se letra a letra (~14 letras por segundo) com uma
   **barra de cursor** fina (`|`, mesma cor do texto, ~0,08 em de largura) à frente. Quando acaba, o cursor
   pisca 2–3 vezes (ligado 0,5 s / desligado 0,5 s) e desaparece. Durante a escrita toca o som
   **`marca/sons/teclado.wav`**, cortado à duração da escrita (desvanecimento de 0,05 s no fim).
2. **Tudo o resto: só aparecer.** Legendas, horas, rótulos, listas, imagens: entram de uma vez (sem
   desvanecer, sem deslizar, sem crescer) e saem de uma vez.

Proibido: sombras, contornos, brilhos, ressaltos, zooms, rotações, linhas que se desenham, letra manuscrita.

## Atenção às licenças
- **New Icon Script**: licença "Free for Personal Use" (exfont.com). Para vídeos comerciais ou de clientes
  é preciso comprar a licença comercial.
- **La Luxes**: confirmar a licença de origem.
- **Hind Siliguri**: livre (Google Fonts, licença OFL).
Por isso as fontes **não** vão para o GitHub (o repositório é público); ficam só no Drive.
