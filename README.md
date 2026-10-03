# Xtreme Ears — site

Site institucional e de geração de demanda da Xtreme Ears. Não é loja: **todo caminho leva o músico ao time comercial no WhatsApp.**

## A decisão

O in-ear moldado é caro e feito por encomenda a partir do molde do ouvido de cada pessoa. Ninguém compra isso num carrinho — e, se comprar, compra errado. Por isso o site não tem checkout: ele qualifica o músico (o que toca, onde toca, o que falta no retorno), indica um ponto de partida e entrega a conversa pronta para o comercial fechar.

Duas portas de entrada para o mesmo lugar:

1. **Quiz "Encontre seu fone"** — 3 perguntas (objetivo → sonoridade → nível). Recomenda um modelo principal e uma alternativa, e abre o WhatsApp com objetivo e modelos já na mensagem.
2. **Formulário "Fale com um especialista"** — nome, cidade, perfil, modelo de interesse e contexto de uso. Abre o WhatsApp com tudo escrito; o músico só revisa e manda.

Nada é enviado para servidor. Não há formulário parado numa caixa de entrada: a conversa começa na hora, com contexto.

Os cards de modelo também alimentam o funil — clicar em "Falar sobre" pré-seleciona aquele modelo no formulário.

## Estrutura da página

| Seção | Papel no funil |
|---|---|
| Hero | Promessa + duas portas (falar agora / descobrir modelo) |
| Por que moldado | Justifica o preço antes de mostrar o preço |
| Encontre seu fone | Qualificação ativa → WhatsApp |
| Linha PRO (moldados) | 9 modelos com driver, crossover, specs e preço "a partir de" |
| Linha universal | Entrada para quem ainda não está pronto para o moldado |
| Como funciona | Explica por que a venda é acompanhada (pré-molde, fonoaudiólogo, aprovação) |
| Quem usa | Prova social — artistas e o catálogo de nomes |
| Depois da compra | Garantia e assistência: tira o medo do ticket alto |
| Dúvidas | FAQ com as objeções reais (incl. "mais drivers = melhor som?") |
| Fale com um especialista | Handoff comercial |
| CTA final + rodapé | Última porta + contatos |

## Conteúdo

Modelos, preços, specs (drivers, crossover, impedância, sensibilidade, resposta de frequência), processo de pré-molde, política de garantia, FAQ e lista de artistas vieram do site e do catálogo atuais da Xtreme Ears (`xtremeears.com.br`). Imagens de produto e as fotos de palco são assets da própria marca.

**Preços são "a partir de"** — a personalização (cápsula, faceplate, cabo, logo) é orçada no atendimento. Ao atualizar, conferir contra a loja.

## Design

Referência: beatsbydre.com — tipografia display pesada e fechada, hero full-bleed, rails horizontais de produto com tiles claros, pílulas de CTA, respiro generoso. Aqui em preto puro, que é a cor da marca.

- Preto e branco puros, como a marca: base `#000`, superfícies `#0b0b0b`/`#141414`, tiles de produto em branco
- Acento é o próprio branco — CTA é pílula branca com texto preto. Não há cor de destaque
- Tipografia: **DM Sans** (400–900), display em 900 com tracking fechado
- Sem build. `assets/site.css` e `assets/site.js` são compartilhados pela home e pelas 13 páginas; a única dependência externa é a fonte do Google e o `embed.js` do Instagram.

## Modelos: a seção fala por área sonora

A linha não é apresentada como tabela de drivers. É dividida por **onde o som pesa**, porque é assim que o músico escolhe:

| área | pra quem | modelos |
|---|---|---|
| **Grave** | bateristas, baixistas, percussionistas, DJs | XE ONE+/PRO · XE3/PRO · XE6/PRO |
| **Médio** | vocalistas, guitarristas, tecladistas | XE4/PRO · XE5/PRO · XE8/PRO |
| **Agudo e detalhe** | técnicos de som, produtores, audiófilos | XE ONEMAX/PRO · XE12/PRO · XE14/PRO |

O "indicado para" de cada card é a recomendação oficial da marca, transcrita das tarjas das próprias fotos do catálogo. O resto da copy fala em bumbo, refrão, naipe de sopro e PA — não em dB/mW.

As trilhas do quiz (`TRILHAS` no script) ficam **dentro** da área que a resposta indica, pra não contradizer essa seção. Ao mexer numa, confira a outra.

## Uma página por modelo

Cada fone tem a sua própria página, em `/<slug>/` — o vendedor manda o link do modelo exato no WhatsApp e o músico abre a apresentação completa: pra quem é, como soa, configuração dos drivers, specs, o que vem na caixa, depoimento em vídeo, processo e CTA.

As 12 páginas são **geradas**, não escritas à mão:

```bash
python3 tools/gerar-paginas.py
```

Os dados ficam na lista `MODELOS` dentro do script. Escritas separadamente, 12 páginas divergiriam na primeira correção de nav, rodapé ou processo. **Não edite o HTML gerado** — mexa no script e rode de novo.

Specs, configuração de drivers e "indicado para" vêm do catálogo e das tarjas das fotos oficiais. Não invente número ali.

## Vídeo e prova social

**Hero.** O fundo é um `<video>` com a foto da Lauana Prado como `poster`. Sem `assets/hero.mp4` no lugar, o navegador mostra o poster — ou seja, hoje se comporta como a foto de antes. Basta largar um `hero.mp4` em `assets/` para virar fundo em vídeo, sem tocar em código.

**Player.** O botão na hero abre um modal com o reel da Lauana (`DOO-skcDgb7`). Limitação real do embed do Instagram: **o vídeo não toca dentro do site** — clicar no play leva o visitante pro Instagram, que ainda mostra muro de cadastro. Por isso o rótulo do botão diz "abre no Instagram". Só um arquivo de vídeo próprio resolve isso de verdade.

**Depoimentos.** A seção `#dizendo` usa embeds oficiais do Instagram (`blockquote.instagram-media` + `embed.js`), com reels reais do @xtremeears. Vantagem: atribuição e contagem de curtidas ao vivo, sem rehospedar vídeo de ninguém. Desvantagem: o embed é um iframe branco de outro domínio, então não dá pra estilizar por dentro — destoa do preto do site, e some se o post for apagado.

Reels em uso, por área, em `REEL_POR_AREA` (páginas de modelo) e na seção `#dizendo` da home:

| reel | quem |
|---|---|
| `DOO-skcDgb7` | Lauana Prado — hero |
| `DdpiEGPMb8i` | Heitor Gomes, baixista |
| `C9fyU-ZBS3a` | Dinho Ouro Preto, Capital Inicial |
| `DdkE-7uSR2n` | Paulo Farat, engenheiro de som |
| `Dd2HSHGSWDA` | Lucas Lima, Pagode dos Ex |
| `DduYbIxSL9d` | Léo, Pagode dos Ex |
| `DdcW6XpSr9c` | audiometria e pré-molde |

## Fotos de produto

As imagens do catálogo vinham com tarja preta de propaganda queimada na arte ("INDICADO PARA BATERISTAS…", "LANÇAMENTO!"), fundo branco, escalas e enquadramentos diferentes. `tools/knockout.html` resolve tudo numa passada — sirva a pasta das fontes com `tools/writer.py` e abra:

1. **corta a tarja** — acha a faixa pelo trecho contínuo de preto na linha e estende por densidade (o texto branco da tarja quebra a faixa e engana a detecção simples);
2. **tira o fundo** — flood fill a partir da borda, então brilho interno do produto não é perdido; o alfa é uma rampa por luminância, com a borda escurecida pra não virar franja branca;
3. **enquadra pelas cápsulas** — erode a máscara até o cabo sumir, separa os blocos, descarta reflexo e caco de cabo, e escala pelo corpo do fone. É isso que faz todos os cards terem o produto do mesmo tamanho, independente do cabo da foto;
4. exporta WebP com transparência, ~50 KB cada.

Quando a própria composição atrapalha (laço de cabo por cima no ONEMAX, reflexo espelhado embaixo no XE6), o job aceita uma `zona` — a faixa de altura onde procurar as cápsulas.

Cada modelo usa foto da **sua própria** página de produto, escolhida pra que nenhum par se repita: roxo, azul-petróleo, madeira clara, laranja, rosa, bege, cinza marmorizado, madeira escura, preto; verde, azul translúcido e preto nos universais. O faceplate é escolhido pelo cliente, então são exemplos do catálogo. Ao trocar uma foto, rode a comparação de cor média pra garantir que nenhuma ficou parecida demais com outra.

## Rodar

```bash
python3 -m http.server 4178
```

Depois abra `http://localhost:4178`.

## Onde mexer

- **Número do WhatsApp**: constante `WHATS` no script, perto do fim do `index.html`.
- **Recomendação do quiz**: objetos `CAT` (catálogo), `Q2` (segunda pergunta por perfil) e `TRILHAS` (perfil+característica → 3 modelos por nível).
- **Modelos e preços**: cards em `#modelos` e o objeto `CAT` — os dois precisam andar juntos.
