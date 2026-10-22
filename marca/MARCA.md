# Marca Rute Dias — manual para a edição

Fonte de verdade: `marca/fontes/guia-de-marca.png` (branding sheet).
Fontes e guia são descarregados por `bash marca/download.sh` (corre também no `setup.sh`).
Variáveis prontas a usar: `marca/marca.css`. Ecrã de exemplo com tudo aplicado: `marca/exemplo.html`.

**Personalidade:** editorial, sofisticada, feminina, luminosa. Calma, nunca agitada.
**Logótipo:** não há. A assinatura é o nome "Rute Dias" escrito em New Icon Script, na cor Cherry Burgundy.

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
- Texto sobre o vídeo: Espresso dentro de uma caixa Winter White ou Champagne (opacidade 85–92 %) ou,
  sobre imagem escura, Winter White diretamente.

## Tipografia
| Função | Fonte | Tamanho em vídeo 1080×1920 |
|---|---|---|
| Título principal | La Luxes | 96–140 px |
| Destaque / assinatura | New Icon Script | 72–120 px, **só palavras ou frases curtas** |
| Subtítulo | Hind Siliguri SemiBold/Medium | 48–64 px |
| Corpo e legendas | Hind Siliguri Regular/Medium | 40–52 px |

**Nota sobre La Luxes:** o ficheiro no Drive é a versão *La Luxes Serif* (só maiúsculas, direita).
O guia mostra *La Luxes Ital* (itálico, com minúsculas). Enquanto a versão Ital não for adicionada ao Drive,
os títulos saem em maiúsculas elegantes, como em `marca/exemplo.html`.

(O guia indica tamanhos em pt para publicações no Instagram; em vídeo vertical usam-se cerca do dobro.)
Para vídeo horizontal 1920×1080, multiplicar os tamanhos por ~0,75.

Rótulos pequenos ao estilo do guia: Hind Siliguri em maiúsculas, com espaçamento entre letras largo (≈0,3em).

## Animações (estilo)
- **Entradas:** aparecer + subir ligeiramente (20–40 px), 0,6–0,8 s, curva suave (`--suave`). Sem saltos nem ressaltos.
- **Saídas:** desvanecer em 0,4–0,5 s.
- **New Icon Script:** a palavra "escreve-se" da esquerda para a direita (revelação com máscara), 0,8–1,2 s.
- **Linhas finas** (1–2 px, Espresso ou Burgundy) que se desenham por baixo de títulos, como no guia.
- **Palavra-chave:** muda para Burgundy ou ganha um sublinhado Burgundy no instante em que é dita.
- **Transições entre secções:** fundido simples ou cortina Winter White/Champagne. Nada de zooms rápidos, giros ou efeitos chamativos.
- Muito espaço vazio à volta do texto; no máximo dois tipos de letra por ecrã.

## Atenção às licenças
- **New Icon Script**: licença "Free for Personal Use" (exfont.com). Para vídeos comerciais ou de clientes
  é preciso comprar a licença comercial.
- **La Luxes**: confirmar a licença de origem.
- **Hind Siliguri**: livre (Google Fonts, licença OFL).
Por isso as fontes **não** vão para o GitHub (o repositório é público); ficam só no Drive.
