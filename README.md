# Xtreme Ears: site (v2, 3D)

Site de conversão da Xtreme Ears. Não é loja: todo caminho termina no WhatsApp do comercial
(5511950295494) com a mensagem já escrita (modelo, configuração montada no 3D, respostas do quiz).

## Páginas

| URL | O que faz |
|---|---|
| `/` | Hero 3D que abre o XE12/PRO conforme a rolagem, linha PRO com filtro por área, quiz de 3 perguntas, teaser do molde em 3D, artistas, história da empresa, FAQ e formulário pro WhatsApp |
| `/molde/` | O molde contado em 3D com rolagem: molde de silicone → aprovado → concha de acrílico → drivers → faceplate. Checklist pra levar ao fonoaudiólogo, linha do tempo e FAQ |
| `/<slug>/` | Uma página por fone (9 moldados + 3 universais). Moldados têm visualizador 3D com "abrir o fone", foco por faixa, configurador de concha/faceplate/acabamento que vai junto na mensagem do WhatsApp, e barra fixa de compra |

## Gerar

```bash
python3 tools/gerar.py
```

Não edite HTML gerado. Ao mexer em `assets/xe.css`, `xe.js` ou `iem3d.js`, troque `V` em `tools/gerar.py`.

- `tools/dados.py`: contato, drivers por faixa (`BANDAS`), visual de vitrine (`VISUAL`), artistas por modelo, FAQ.
- `tools/gerar-paginas.py`: só fornece os textos e specs do catálogo (`MODELOS`). É da v1; **não rode ele direto**, ele recria as páginas antigas.
- `assets/iem3d.js`: o fone em Three.js, montado por código. Um driver de armadura balanceada pra cada driver do catálogo, colorido pela faixa (roxo subgrave, laranja grave, azul médio, amarelo agudo, cinza "não divulgado" no XE14).
- `assets/render/*.webp`: fotos dos cards, renderizadas do mesmo 3D por `tools/render.html` (Chrome headless).

## Fontes dos fatos (pesquisa de 06/11/2026)

xtremeears.com.br (fale-conosco, perguntas-frequentes, como-comprar-1, manutencao-e-garantia,
por-que-os-pre-moldes-do-seu-ouvido-sao-importantes, artistas, políticas de troca e envio) e o especial
da Canaltech de 29/01/2020 (André Goldstein, XE2/PRO em 2010).

Fora do site por falta de fonte: parcelamento, custo da moldagem, CNPJ, impressão 3D/escaneamento,
nota no Google e no Reclame Aqui. O ano de fundação diverge (2009 x 2010); o site usa o fato firme: XE2/PRO em 2010.

O processo físico do molde (tampão de espuma, silicone) é descrito como costuma ser feito; o que vem da marca é:
só fonoaudiólogo, concha completa, segunda curva, aprovação por foto/vídeo/videochamada, envio com rastreio e nome+pedido.
