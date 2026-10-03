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

- Base `#000`, superfícies `#0b0b0b`/`#141414`, tiles de produto claros `#f2f2f2`
- Acento `#c20000` (vermelho Xtreme) / `#e01a0e` no hover
- Tipografia: **DM Sans** (400–900), display em 900 com tracking fechado
- Um arquivo: `index.html` com CSS e JS inline. Sem build, sem dependência além da fonte do Google.

## Rodar

```bash
python3 -m http.server 4178
```

Depois abra `http://localhost:4178`.

## Onde mexer

- **Número do WhatsApp**: constante `WHATS` no script, perto do fim do `index.html`.
- **Recomendação do quiz**: objetos `CAT` (catálogo), `Q2` (segunda pergunta por perfil) e `TRILHAS` (perfil+característica → 3 modelos por nível).
- **Modelos e preços**: cards em `#modelos` e o objeto `CAT` — os dois precisam andar juntos.
