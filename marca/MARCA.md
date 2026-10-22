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
- Texto sobre o vídeo: diretamente sobre a imagem, **sem sombra e sem caixa**. Winter White por defeito;
  Espresso quando o fundo é claro. Escolher o plano/posição para o texto se ler bem, em vez de pôr sombra.
- **Regra do destaque:** a cor de destaque é o Cherry Burgundy. **Quando o burgundy não se lê** sobre a imagem
  (fundo escuro ou avermelhado), usa-se **Champagne**. Teste: contraste de pelo menos 3:1 entre a cor e
  as partes **mais escuras** do fundo por trás do texto (20.º percentil); se o burgundy não chegar, Champagne.
- O mesmo para o texto normal: Winter White precisa de 3:1 sobre as partes **mais claras** (80.º percentil);
  se não chegar, Espresso (e os destaques em Champagne passam a Burgundy). Implementado em `marca/exemplo.html`.

## Tipografia (vídeos)
Guia atualizado: Sloop (títulos, destaques, assinaturas) + Proxima Nova (subtítulos, corpo, informação).
Nos vídeos usa-se assim:

| Formato | Títulos | Legendas e texto | Destaques |
|---|---|---|---|
| **Vlog** | "Sistema" | "Sistema" | algumas palavras na mesma fonte noutro tom da paleta; outras em Sloop |
| **Yapping** | Sloop | Proxima Nova | Sloop |

- **Sloop só no yapping** (títulos e destaques). No vlog, a única exceção são algumas palavras das legendas.
- **"Sistema"** = a letra do sistema do telemóvel / do CapCut (a do iPhone, SF Pro). Nos vídeos usa-se a
  **Inter**, gratuita e quase igual (a SF Pro é da Apple e a licença não permite usá-la fora dos aparelhos Apple).
- **Proxima Nova:** as versões DEMO do Drive não têm acentos (ã, ç, é…) e não podem ser publicadas. Enquanto a
  Rute não puser a versão completa, usa-se **Montserrat** (a mais parecida).
- **Sloop:** ainda não está no Drive. Para pré-visualizações usa-se Mrs Saint Delafield; num vídeo final,
  pedir o ficheiro à Rute antes de renderizar.
- **Espaçamento entre letras apertado** em tudo: títulos -0,03 em, texto -0,015 em, rótulos em maiúsculas 0,1 em.

Para vídeo horizontal 1920×1080, multiplicar os tamanhos por ~0,75.

## Animações (só duas)
1. **Títulos: máquina de escrever.** O texto escreve-se letra a letra (~14 letras por segundo) com uma
   **barra de cursor** fina (`|`, mesma cor do texto, ~0,08 em de largura) à frente. Quando acaba, o cursor
   pisca 2–3 vezes (ligado 0,5 s / desligado 0,5 s) e desaparece. Durante a escrita toca o som
   **`marca/sons/teclado.wav`**, cortado à duração da escrita (desvanecimento de 0,05 s no fim).
2. **Tudo o resto: só aparecer.** (As legendas aparecem palavra a palavra, mas cada palavra também só aparece.) Legendas, horas, rótulos, listas, imagens: entram de uma vez (sem
   desvanecer, sem deslizar, sem crescer) e saem de uma vez.

Proibido: sombras, contornos, brilhos, ressaltos, zooms, rotações, linhas que se desenham.

## Atenção às licenças
- **Inter**, **Montserrat** e **Mrs Saint Delafield**: livres (Google Fonts, licença OFL).
- **Proxima Nova**: paga (Mark Simonson). As versões "Fontspring DEMO" são só para testar, não para publicar.
- **Sloop**: confirmar a licença quando a Rute enviar o ficheiro.
Por isso as fontes **não** vão para o GitHub (o repositório é público); ficam só no Drive.
