#!/usr/bin/env python3
"""
Gera o site inteiro: home, /molde/ e uma página por fone (/xe12-pro/ etc).

    python3 tools/gerar.py

Dados em tools/dados.py (e os textos do catálogo em tools/gerar-paginas.py).
Não edite o HTML gerado: mexa aqui e rode de novo.
"""
import html
import json
import os
import pathlib
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados as D

RAIZ = pathlib.Path(__file__).resolve().parent.parent
V = "20261106c"  # muda a cada deploy que mexa em css/js


def e(t):
    return html.escape(str(t), quote=True)


def zap(msg):
    return f"https://wa.me/{D.WHATS}?text={quote(msg)}"


MOLDADOS = [m for m in D.MODELOS if not m.get("universal")]
UNIVERSAIS = [m for m in D.MODELOS if m.get("universal")]
POR_SLUG = {m["slug"]: m for m in D.MODELOS}


def ndrivers(m):
    if m["slug"] in D.BANDAS:
        return sum(D.BANDAS[m["slug"]][0].values())
    d = m["drivers"][0]
    return int(d.split()[0]) if d[0].isdigit() else 1


def config(m):
    if m["slug"] not in D.BANDAS:
        return None
    bands, ways = D.BANDAS[m["slug"]]
    shell, finish, face, tone = D.VISUAL[m["slug"]]
    return {"bands": bands, "ways": ways, "shell": shell, "finish": finish, "face": face, "logoTone": tone}


BAND_NOME = {"sub": "Subgrave", "bass": "Grave", "nd": "Não divulgado", "mid": "Médio", "high": "Agudo"}
BAND_ORDEM = ["sub", "bass", "nd", "mid", "high"]


def band_dots(m):
    c = config(m)
    if not c:
        return '<span class="dots"><i class="b-dyn"></i></span>'
    out = ""
    for b in BAND_ORDEM:
        out += "".join(f'<i class="b-{b}"></i>' for _ in range(c["bands"].get(b, 0)))
    return f'<span class="dots" aria-hidden="true">{out}</span>'


def img_modelo(m, pre):
    if m.get("universal"):
        return f"{pre}assets/{m['slug']}.webp"
    return f"{pre}assets/render/{m['slug']}.webp"


# ------------------------------------------------------------------ moldura

ICON = {
    "zap": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.6-.3Z"/></svg>',
    "seta": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" d="M5 12h14m-6-6 6 6-6 6"/></svg>',
    "giro": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.8" d="M3 12a9 4 0 1 0 9-4M12 8l-3-2.5M12 8l-3 2.5"/></svg>',
}


def head(titulo, desc, pre, og="assets/og.jpg", extra=""):
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#050505">
<link rel="icon" href="{pre}assets/xe-mark.png" type="image/png">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{pre}{og}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=JetBrains+Mono:wght@400;600&display=swap">
<link rel="stylesheet" href="{pre}assets/xe.css?v={V}">
{extra}</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
'''


def header(pre, ativo=""):
    def a(href, txt, k):
        cls = ' class="on"' if k == ativo else ""
        return f'<a href="{href}"{cls}>{txt}</a>'
    links = (a(f"{pre}#fones", "Fones", "fones") + a(f"{pre}molde/", "O molde", "molde") +
             a(f"{pre}#encontre", "Qual é o meu?", "quiz") + a(f"{pre}#artistas", "Quem usa", "art") +
             a(f"{pre}#empresa", "A Xtreme Ears", "emp") + a(f"{pre}#duvidas", "Dúvidas", "faq"))
    msg = "Olá! Vim pelo site da Xtreme Ears e quero falar com um especialista."
    return f'''<header class="hd" id="hd">
  <a class="hd-logo" href="{pre}" aria-label="Xtreme Ears, início"><img src="{pre}assets/logo-xtreme-branco.png" alt="Xtreme Ears" width="124" height="65"></a>
  <nav class="hd-nav" aria-label="Principal">{links}</nav>
  <a class="btn btn-zap btn-sm hd-cta" href="{zap(msg)}" target="_blank" rel="noopener" data-cta="header">{ICON["zap"]}<span>Falar com especialista</span></a>
  <button class="hd-burger" id="burger" aria-expanded="false" aria-controls="menu" aria-label="Abrir menu"><span></span><span></span></button>
</header>
<div class="menu" id="menu" hidden>
  <nav>{links}</nav>
  <a class="btn btn-zap" href="{zap(msg)}" target="_blank" rel="noopener" data-cta="menu">{ICON["zap"]}Falar com especialista</a>
</div>
'''


def footer(pre):
    moldados = "".join(f'<a href="{pre}{m["slug"]}/">{e(m["nome"])}</a>' for m in MOLDADOS)
    univ = "".join(f'<a href="{pre}{m["slug"]}/">{e(m["nome"])}</a>' for m in UNIVERSAIS)
    return f'''<footer class="ft">
  <div class="wrap ft-in">
    <div class="ft-marca">
      <img src="{pre}assets/logo-xtreme-branco.png" alt="Xtreme Ears" width="150" height="79" loading="lazy">
      <p>In-ear moldado sob medida, projetado e produzido no Brasil desde 2010.</p>
      <p class="ft-redes"><a href="{D.INSTAGRAM}" target="_blank" rel="noopener">Instagram</a><a href="{D.YOUTUBE}" target="_blank" rel="noopener">YouTube</a><a href="{D.LOJA}" target="_blank" rel="noopener">Loja oficial</a></p>
    </div>
    <div><h4>Moldados</h4>{moldados}</div>
    <div><h4>Universais</h4>{univ}<h4 class="mt">Guia</h4><a href="{pre}molde/">Como fazer o molde</a><a href="{pre}#duvidas">Dúvidas</a></div>
    <div class="ft-contato"><h4>Atendimento</h4>
      <a href="{zap("Olá! Vim pelo site da Xtreme Ears.")}" target="_blank" rel="noopener">WhatsApp (11) 95029-5494</a>
      <a href="tel:+551132562692">{D.TELEFONE}</a>
      <a href="mailto:{D.EMAIL}">{D.EMAIL}</a>
      <p>{D.HORARIO}<br>{D.ENDERECO}</p>
    </div>
  </div>
  <div class="wrap ft-base"><span>© 2026 Xtreme Ears</span><span>Garantia de 1 ano · 60 dias para ajuste da concha · Frete grátis</span></div>
</footer>
'''


def scripts(pre, three=True):
    t = (f'<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>\n'
         f'<script src="{pre}assets/iem3d.js?v={V}"></script>\n') if three else ""
    return f'''{t}<script src="{pre}assets/xe.js?v={V}"></script>
</body>
</html>
'''


GARANTIAS = [
    ("1 ano", "de garantia contra defeito de fabricação e entupimento"),
    ("60 dias", "pra ajustar o molde, inclusive refazendo a concha"),
    ("Desde 2010", "projetando e fabricando in-ear moldado no Brasil"),
    ("Frete grátis", "pra todo o Brasil, com rastreio"),
]


def garantias_html():
    return "".join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in GARANTIAS)


def faq_html(itens):
    return "".join(f'''<details class="faq-i rv"><summary>{e(q)}<i></i></summary><p>{e(a)}</p></details>
''' for q, a in itens)


# ------------------------------------------------------------------ cards

def card(m, pre, idx=0):
    area = D.AREAS[m["area"]][0]
    tag = f'<em class="card-flag">{e(m["flag"])}</em>' if m.get("flag") else ""
    n = ndrivers(m)
    return f'''<a class="card rv" href="{pre}{m["slug"]}/" data-area="{m["area"]}" style="--i:{idx}">
  <div class="card-stage"><span class="card-glow"></span><img src="{img_modelo(m, pre)}" alt="{e(m["nome"])}" width="800" height="800" loading="lazy"></div>
  <div class="card-body">
    <div class="card-top"><span class="card-area">{e(area)}</span>{tag}</div>
    <h3>{e(m["nome"])}</h3>
    <p class="card-ass">{e(m["assinatura"])}</p>
    <div class="card-dr">{band_dots(m)}<span><b>{n}</b> {"driver" if n == 1 else "drivers"}</span></div>
    <p class="card-pra">{e(m["indicado"])}</p>
    <div class="card-ft"><span class="card-preco"><small>a partir de</small>R$ {e(m["preco"])}</span><span class="card-ir">Ver {ICON["seta"]}</span></div>
  </div>
</a>'''


# ------------------------------------------------------------------ home

def home():
    pre = ""
    artistas = json.loads((RAIZ / "assets/artistas/_lista.json").read_text())
    faixa = "".join(f'<figure><img src="assets/artistas/{a["arq"]}" alt="{e(a["nome"])}" width="360" height="266" loading="lazy"><figcaption>{e(a["nome"])}</figcaption></figure>' for a in artistas)
    metade = len(artistas) // 2

    cards_m = "\n".join(card(m, pre, i) for i, m in enumerate(MOLDADOS))
    cards_u = "\n".join(card(m, pre, i) for i, m in enumerate(UNIVERSAIS))

    cat = {m["slug"]: {"nome": m["nome"], "preco": m["preco"], "ass": m["assinatura"], "img": img_modelo(m, ""),
                       "pra": m["indicado"], "n": ndrivers(m)} for m in D.MODELOS}

    hero_cfg = json.dumps(config(POR_SLUG["xe12-pro"]))
    msg_geral = "Olá! Vim pelo site da Xtreme Ears e quero ajuda pra escolher o meu in-ear moldado."

    corpo = f'''{head("Xtreme Ears | In-ear moldado sob medida, feito no Brasil",
                    "Fones in-ear moldados no formato do seu ouvido. Projetados e produzidos no Brasil desde 2010, usados por mais de 100 artistas. Garantia de 1 ano e 60 dias pra ajuste da concha.", pre)}
{header(pre)}
<main id="conteudo">

<!-- HERO 3D: o fone gira e abre conforme a rolagem -->
<section class="hero" id="topo" data-hero3d='{hero_cfg}'>
  <div class="hero-sticky">
    <canvas class="hero-canvas" aria-label="Fone in-ear moldado XE12/PRO em 3D. Role a página para abrir o fone."></canvas>
    <div class="hero-fallback"><img src="assets/render/xe12-pro.webp" alt="" width="800" height="800"></div>
    <div class="hero-copy wrap">
      <p class="eyebrow"><span class="pulse"></span>In-ear moldado · feito no Brasil desde 2010</p>
      <h1 class="h1">Feito no formato<br>do <em>seu</em> ouvido.</h1>
      <p class="lede">O retorno que não escorrega, não vaza e deixa você tocar com o volume mais baixo. Cada Xtreme Ears nasce do molde do seu canal auditivo e é montado à mão, driver por driver.</p>
      <div class="hero-ctas">
        <a class="btn btn-pri" href="#encontre" data-cta="hero-quiz">Descobrir o meu fone {ICON["seta"]}</a>
        <a class="btn btn-zap" href="{zap(msg_geral)}" target="_blank" rel="noopener" data-cta="hero-zap">{ICON["zap"]}Falar com especialista</a>
      </div>
      <ul class="hero-prova"><li><b>+100</b> artistas</li><li><b>1 ano</b> de garantia</li><li><b>60 dias</b> pra ajuste</li></ul>
    </div>
    <ol class="hero-steps" aria-hidden="true">
      <li data-s="1"><span class="k">01 · Faceplate</span><b>A tampa é sua.</b> Glitter, carbono, madeira, a sua logo.</li>
      <li data-s="2"><span class="k">02 · Crossover</span><b>Divide o som em vias</b> e manda cada faixa pro driver certo.</li>
      <li data-s="3"><span class="k">03 · 12 drivers</span><b>Subgrave, grave, médio e agudo</b>, cada um com o seu.</li>
      <li data-s="4"><span class="k">04 · Concha</span><b>Acrílico no formato exato</b> do seu canal, até a segunda curva.</li>
    </ol>
    <div class="hero-scroll" aria-hidden="true"><span></span>role pra abrir o fone</div>
  </div>
</section>

<!-- POR QUE MOLDADO -->
<section class="sec wrap porque" id="porque">
  <div class="sec-head rv">
    <p class="kicker">Por que moldado</p>
    <h2 class="h2">Universal encaixa em todo mundo.<br><span class="dim">Moldado encaixa em você.</span></h2>
  </div>
  <div class="vs rv">
    <div class="vs-col">
      <h3>Fone universal</h3>
      <ul><li>Ponteira de silicone que mexe quando você canta ou mastiga</li><li>Vedação muda a cada vez que você coloca</li><li>Som de fora vaza, e a tendência é subir o volume</li><li>Grave muda conforme a ponteira assenta</li></ul>
    </div>
    <div class="vs-col vs-on">
      <h3>Xtreme Ears moldado</h3>
      <ul><li>Concha feita a partir do molde do seu canal, até a segunda curva</li><li>Encaixa igual todas as vezes, do ensaio ao bis</li><li>Vedação de verdade: dá pra ouvir tudo com menos volume</li><li>O som que você aprovou é o som que você ouve no palco</li></ul>
    </div>
  </div>
</section>

<!-- LINHA -->
<section class="sec fones" id="fones">
  <div class="wrap">
    <div class="sec-head sec-head-row rv">
      <div><p class="kicker">A linha PRO</p><h2 class="h2">Nove moldados.<br><span class="dim">Um pra cada palco.</span></h2></div>
      <div class="filtros" role="tablist" aria-label="Filtrar por área">
        <button class="on" data-f="todos">Todos</button><button data-f="grave">Grave</button><button data-f="medio">Médio</button><button data-f="agudo">Agudo e detalhe</button>
      </div>
    </div>
    <p class="fones-dica rv">Cada bolinha é um driver: <span class="legend"><i class="b-sub"></i>subgrave <i class="b-bass"></i>grave <i class="b-mid"></i>médio <i class="b-high"></i>agudo</span></p>
    <div class="grid" id="gridMoldados">
{cards_m}
    </div>
    <div class="univ rv">
      <div class="univ-head"><h3>Ainda não é hora do moldado?</h3><p>Os universais saem em até 2 dias úteis, sem pré-molde. Servem de primeiro in-ear e de reserva depois.</p></div>
      <div class="grid grid-u">
{cards_u}
      </div>
    </div>
  </div>
</section>

<!-- QUIZ -->
<section class="sec wrap quiz" id="encontre">
  <div class="quiz-box rv" data-quiz='{json.dumps(cat, ensure_ascii=False)}'>
    <div class="quiz-side">
      <p class="kicker">30 segundos</p>
      <h2 class="h2">Qual Xtreme Ears<br>é o seu?</h2>
      <p>Três perguntas. No fim você recebe uma indicação e uma alternativa, e já pode mandar tudo pro especialista no WhatsApp.</p>
      <div class="quiz-prog"><i></i></div>
    </div>
    <div class="quiz-main">
      <fieldset class="q on" data-q="0"><legend>O que você faz no palco?</legend>
        <button data-v="grave" data-t="Bateria ou percussão">Bateria ou percussão</button>
        <button data-v="grave" data-t="Baixo">Baixo</button>
        <button data-v="medio" data-t="Voz">Voz</button>
        <button data-v="medio" data-t="Guitarra, violão ou teclado">Guitarra, violão ou teclado</button>
        <button data-v="agudo" data-t="Técnico de som ou produtor">Técnico de som ou produtor</button>
        <button data-v="agudo" data-t="Escuto música com detalhe (audiófilo)">Escuto música com detalhe</button>
      </fieldset>
      <fieldset class="q" data-q="1"><legend>Onde você mais usa?</legend>
        <button data-v="0" data-t="Igreja e ensaios">Igreja e ensaios</button>
        <button data-v="1" data-t="Shows em casas e eventos">Shows em casas e eventos</button>
        <button data-v="2" data-t="Turnê e palcos grandes">Turnê e palcos grandes</button>
        <button data-v="3" data-t="Estúdio e mixagem">Estúdio e mixagem</button>
      </fieldset>
      <fieldset class="q" data-q="2"><legend>Quanto pensa em investir?</legend>
        <button data-v="0" data-t="Até R$ 3 mil">Até R$ 3 mil</button>
        <button data-v="1" data-t="De R$ 3 a 6 mil">De R$ 3 a 6 mil</button>
        <button data-v="2" data-t="De R$ 6 a 12 mil">De R$ 6 a 12 mil</button>
        <button data-v="3" data-t="Quero o topo da linha">Quero o topo da linha</button>
      </fieldset>
      <div class="q q-res" data-q="3" aria-live="polite"></div>
      <button class="quiz-back" type="button" hidden>← voltar</button>
    </div>
  </div>
</section>

<!-- MOLDE (teaser 3D) -->
<section class="sec molde-tz" id="molde">
  <div class="wrap molde-tz-in">
    <div class="molde-tz-3d rv"><canvas data-molde-loop aria-label="Molde de silicone do ouvido se transformando na concha do fone"></canvas><span class="molde-tz-tag" data-molde-tag>Molde de silicone</span></div>
    <div class="molde-tz-txt rv">
      <p class="kicker">O molde</p>
      <h2 class="h2">Tudo começa no molde do seu ouvido.</h2>
      <p class="lede">Um fonoaudiólogo faz o molde do seu ouvido em silicone. É esse molde que vira a concha do seu fone, então ele precisa ser perfeito: concha completa e canal até a segunda curva.</p>
      <ol class="mini-steps">
        <li><b>Você compra ou conversa com o especialista</b> e recebe a lista de fonoaudiólogos perto de você.</li>
        <li><b>Faz o molde</b> e manda foto, vídeo ou faz videochamada com a Xtreme Ears na hora.</li>
        <li><b>Envia pelo correio</b> com rastreio. Em cerca de 4 semanas o fone está pronto.</li>
      </ol>
      <a class="btn btn-ghost" href="molde/">Entender o molde em detalhe {ICON["seta"]}</a>
    </div>
  </div>
</section>

<!-- ARTISTAS -->
<section class="sec artistas" id="artistas">
  <div class="wrap sec-head rv">
    <p class="kicker">Quem usa</p>
    <h2 class="h2">Mais de 100 artistas<br><span class="dim">tocam com Xtreme Ears.</span></h2>
    <p class="lede">De Gilberto Gil a Anitta, de Milton Nascimento a Aquiles Priester. A lista completa está na página oficial de artistas da marca.</p>
  </div>
  <div class="marq" aria-label="Artistas que usam Xtreme Ears">
    <div class="marq-row"><div class="marq-track">{"".join(f'<figure><img src="assets/artistas/{a["arq"]}" alt="{e(a["nome"])}" width="360" height="266" loading="lazy"><figcaption>{e(a["nome"])}</figcaption></figure>' for a in artistas[:metade])}</div></div>
    <div class="marq-row marq-rev"><div class="marq-track">{"".join(f'<figure><img src="assets/artistas/{a["arq"]}" alt="{e(a["nome"])}" width="360" height="266" loading="lazy"><figcaption>{e(a["nome"])}</figcaption></figure>' for a in artistas[metade:])}</div></div>
  </div>
  <div class="wrap palcos">
    <figure class="palco rv"><img src="assets/artista-lauana.jpg" alt="Lauana Prado no palco com o seu Xtreme Ears" width="1920" height="1080" loading="lazy"><figcaption><b>Lauana Prado</b><a href="xe4-pro/">usa o XE4/PRO {ICON["seta"]}</a></figcaption></figure>
    <figure class="palco rv"><img src="assets/artista-falcao.jpg" alt="Marcelo Falcão no palco" width="1920" height="1080" loading="lazy"><figcaption><b>Marcelo Falcão</b><a href="xe12-pro/">usa o XE12/PRO {ICON["seta"]}</a></figcaption></figure>
    <figure class="palco rv"><img src="assets/artista-felipe.jpg" alt="Felipe Amorim no palco" width="1920" height="1080" loading="lazy"><figcaption><b>Felipe Amorim</b><a href="xe14-pro/">usa o XE14/PRO {ICON["seta"]}</a></figcaption></figure>
  </div>
</section>

<!-- EMPRESA -->
<section class="sec wrap empresa" id="empresa">
  <div class="sec-head rv">
    <p class="kicker">A Xtreme Ears</p>
    <h2 class="h2">Engenharia acústica,<br><span class="dim">feita à mão em São Paulo.</span></h2>
  </div>
  <div class="emp-grid">
    <div class="emp-txt rv">
      <p>A Xtreme Ears nasceu porque músico brasileiro queria um in-ear moldado com qualidade de fora e atendimento daqui. Foi fundada por André Goldstein, engenheiro especialista em acústica.</p>
      <p>Em 2010 lançou o XE2/PRO, apontado como o primeiro fone in-ear personalizado projetado e produzido no Brasil. De lá pra cá a linha cresceu até o XE14/PRO, e cada fone continua sendo montado de forma artesanal, a partir do molde de quem vai usar.</p>
      <p>O atendimento é consultivo do começo ao fim: alguém do time conversa com você antes da compra, acompanha a aprovação do molde e cuida da garantia depois.</p>
    </div>
    <ol class="linha-tempo rv">
      <li><b>2010</b><span>Lançamento do XE2/PRO, primeiro in-ear moldado projetado e feito no Brasil</span></li>
      <li><b>15+ anos</b><span>De palco, igreja, estúdio e turnê</span></li>
      <li><b>+100</b><span>Artistas na família Xtreme Ears</span></li>
      <li><b>Hoje</b><span>Nove moldados, de 3 a 14 drivers, e três universais</span></li>
    </ol>
  </div>
  <ul class="garantias rv">{garantias_html()}</ul>
</section>

<!-- FAQ -->
<section class="sec wrap faq" id="duvidas">
  <div class="sec-head rv"><p class="kicker">Dúvidas</p><h2 class="h2">Antes de você perguntar.</h2></div>
  <div class="faq-list">
{faq_html(D.FAQ)}
  </div>
</section>

<!-- FORM -> WHATSAPP -->
<section class="sec cta-final" id="falar">
  <div class="wrap cta-in">
    <div class="rv">
      <p class="kicker">Fale com um especialista</p>
      <h2 class="h2">Conta o que você toca.<br><span class="dim">A gente indica o fone.</span></h2>
      <p class="lede">Nada vai pra caixa de entrada esquecida: o formulário abre o WhatsApp com a sua mensagem pronta. Atendimento de {D.HORARIO.lower()}.</p>
    </div>
    <form class="form rv" id="formZap" novalidate>
      <label>Seu nome<input name="nome" required autocomplete="name" placeholder="Como te chamamos?"></label>
      <label>Cidade<input name="cidade" autocomplete="address-level2" placeholder="Pra indicar o fonoaudiólogo mais perto"></label>
      <label>O que você faz<select name="perfil"><option>Bateria ou percussão</option><option>Baixo</option><option selected>Voz</option><option>Guitarra, violão ou teclado</option><option>Técnico de som ou produtor</option><option>Audiófilo</option></select></label>
      <label>Modelo de interesse<select name="modelo"><option>Ainda não sei</option>{"".join(f"<option>{e(m['nome'])}</option>" for m in D.MODELOS)}</select></label>
      <label class="full">Conta um pouco<textarea name="ctx" rows="3" placeholder="Onde você toca, que fone usa hoje, o que falta no seu retorno"></textarea></label>
      <button class="btn btn-zap full" type="submit">{ICON["zap"]}Abrir conversa no WhatsApp</button>
    </form>
  </div>
</section>

</main>
{footer(pre)}
<a class="fab" href="{zap(msg_geral)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp" data-cta="fab">{ICON["zap"]}</a>
{scripts(pre)}'''
    (RAIZ / "index.html").write_text(corpo)


# ------------------------------------------------------------------ produto

def pagina(m):
    pre = "../"
    c = config(m)
    universal = m.get("universal")
    area_nome, area_frase, area_quem = D.AREAS[m["area"]]
    n = ndrivers(m)
    msg = f"Olá! Vim pela página do {m['nome']} no site da Xtreme Ears e quero falar com um especialista sobre ele."

    # viewer: 3D pros moldados, foto pros universais
    if c:
        swatches_shell = "".join(
            f'<button class="sw" data-shell="{k}" style="--c:{v}" title="{e(n_)}" aria-label="Concha {e(n_)}"></button>'
            for k, n_, v in [("transparente", "Transparente", "rgba(225,235,245,.55)"), ("preto-translucido", "Preto translúcido", "#3a3e45"),
                             ("preto", "Preto", "#111"), ("azul", "Azul", "#2563eb"), ("verde", "Verde", "#16a34a"),
                             ("vermelho", "Vermelho", "#d21f2b"), ("rosa", "Rosa", "#e1408f"), ("rosa-claro", "Rosa claro", "#f5b6d2")])
        swatches_face = "".join(
            f'<button class="sw" data-face="{k}" style="--c:{v}" title="{e(k.capitalize())}" aria-label="Faceplate {e(k)}"></button>'
            for k, v in [("vermelho", "#b3141f"), ("preto", "#121212"), ("azul", "#1d4ed8"), ("verde", "#15803d"), ("rosa", "#db2777"),
                         ("roxo", "#6d28d9"), ("dourado", "#b8892f"), ("prata", "#9aa3ad"), ("branco", "#ececec")])
        finishes = "".join(f'<button class="chip" data-finish="{k}">{v}</button>' for k, v in
                           [("glitter", "Glitter"), ("solido", "Sólido"), ("perola", "Perolado"), ("carbono", "Carbono")])
        bandas_chips = "".join(
            f'<button class="chip chip-b b-{b}" data-focus="{b}"><i></i>{BAND_NOME[b]} <b>{c["bands"][b]}</b></button>'
            for b in BAND_ORDEM if c["bands"].get(b))
        viewer = f'''<div class="pv" data-viewer='{json.dumps(c)}'>
      <canvas class="pv-canvas" aria-label="{e(m["nome"])} em 3D. Arraste para girar."></canvas>
      <img class="pv-fallback" src="{pre}assets/render/{m["slug"]}.webp" alt="{e(m["nome"])}" width="800" height="800">
      <div class="pv-ui">
        <button class="pv-explode" type="button" aria-pressed="false">{ICON["giro"]}<span>Abrir o fone</span></button>
        <span class="pv-hint">arraste pra girar</span>
      </div>
      <div class="pv-bands">{bandas_chips}</div>
    </div>'''
        perso = f'''<div class="perso">
        <div class="perso-row"><span class="perso-lb">Concha <em data-lb="shell"></em></span><div class="sws">{swatches_shell}</div></div>
        <div class="perso-row"><span class="perso-lb">Faceplate <em data-lb="face"></em></span><div class="sws">{swatches_face}</div></div>
        <div class="perso-row"><span class="perso-lb">Acabamento</span><div class="chips">{finishes}</div></div>
        <p class="tiny">A combinação que você montar aqui vai junto na mensagem do WhatsApp. Madeira, aço escovado, cristais e a sua logo gravada também são possíveis, em mais de 20 cores.</p>
      </div>'''
    else:
        viewer = f'''<div class="pv pv-foto"><span class="card-glow"></span><img src="{pre}assets/{m["slug"]}.webp" alt="{e(m["nome"])}" width="1000" height="1000"></div>'''
        perso = ""

    # assinatura sonora
    if c:
        pico = max(c["bands"].values())
        barras = "".join(f'''<button class="sig-b" data-focus="{b}" style="--n:{c["bands"][b] / pico:.3f}">
          <span class="sig-n">{c["bands"][b]}</span><span class="sig-bar b-{b}"><i></i></span><span class="sig-l">{BAND_NOME[b]}</span></button>'''
                         for b in BAND_ORDEM if c["bands"].get(b))
        nota = D.NOTA_BANDAS.get(m["slug"], "")
        assinatura = f'''<section class="pd-sec rv" id="assinatura">
      <p class="kicker">Assinatura sonora</p>
      <h2 class="h3">Quantos drivers cuidam de cada faixa</h2>
      <p class="muted">Toque numa faixa pra ver esses drivers acenderem no 3D.</p>
      <div class="sig">{barras}</div>
      <p class="sig-way">Crossover de <b>{c["ways"]} vias</b>{(". " + e(nota)) if nota else ""}</p>
    </section>'''
    else:
        assinatura = ""

    ouvir = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in m["ouvir"])
    drivers = "".join(f"<li>{e(d)}</li>" for d in m["drivers"])
    specs = "".join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in m["specs"]) or '<div><dt>Configuração</dt><dd>sob consulta</dd></div>'
    caixa_itens = D.CAIXA_MOLDADO if not universal else ["Fone in-ear universal", "Kit de ponteiras de silicone e espuma", "Estojo", "Manual do usuário"]
    caixa = "".join(f"<li>{e(i)}</li>" for i in caixa_itens)

    art = D.ARTISTAS_POR_MODELO.get(m["slug"], [])
    art_html = ""
    if art:
        nome, arq = art[0]
        foto = f'<img src="{pre}assets/artistas/{arq}" alt="{e(nome)}" width="360" height="266" loading="lazy">' if arq else ""
        art_html = f'<div class="pd-art">{foto}<p><span class="kicker">No palco</span><b>{e(nome)}</b> usa {e(m["nome"])}</p></div>'

    prazo = "Pronta entrega: sai em até 2 dias úteis" if universal else "Fica pronto em cerca de 4 semanas depois do molde aprovado"

    irmaos = [o for o in D.MODELOS if o["area"] == m["area"] and o["slug"] != m["slug"]]
    vizinhos = [o for o in MOLDADOS if o["slug"] != m["slug"] and o not in irmaos]
    irmaos = (irmaos + vizinhos)[:3]
    irmaos_html = "\n".join(card(o, pre, i) for i, o in enumerate(irmaos))

    processo = "" if universal else f'''
<section class="sec wrap proc">
  <div class="sec-head rv"><p class="kicker">Como você recebe o seu</p><h2 class="h2">Do primeiro contato<br><span class="dim">ao {e(m["nome"])} no palco.</span></h2></div>
  <ol class="steps">
    <li class="rv"><b>01</b><h3>Conversa</h3><p>Você conta o que toca e onde. O especialista confirma se o {e(m["nome"])} é o certo ou indica outro.</p></li>
    <li class="rv"><b>02</b><h3>Molde</h3><p>Você recebe a lista de fonoaudiólogos perto de você. Concha completa e canal até a segunda curva.</p></li>
    <li class="rv"><b>03</b><h3>Aprovação</h3><p>Foto, vídeo ou videochamada com o time durante a consulta. Só segue molde aprovado.</p></li>
    <li class="rv"><b>04</b><h3>Do seu jeito</h3><p>Cor da concha, faceplate, cabo e a sua logo gravada, se quiser.</p></li>
    <li class="rv"><b>05</b><h3>Entrega</h3><p>Cerca de 4 semanas após o molde chegar. Frete grátis, 1 ano de garantia e 60 dias pra ajuste.</p></li>
  </ol>
  <a class="btn btn-ghost rv" href="{pre}molde/">Tudo sobre o molde {ICON["seta"]}</a>
</section>'''

    faq_prod = [q for q in D.FAQ if not universal or "molde" not in q[1]][:5]

    corpo = f'''{head(f"{m['nome']} | {m['assinatura']} | Xtreme Ears",
                    f"{m['nome']}: {m['chamada']} {n} drivers. Indicado para {m['indicado'].lower()}. A partir de R$ {m['preco']}.",
                    pre, og=img_modelo(m, "")[0:] if True else "")}
{header(pre, "fones")}
<main id="conteudo" class="pd">
  <nav class="crumb wrap" aria-label="Você está em"><a href="{pre}">Início</a><span>/</span><a href="{pre}#fones">Fones</a><span>/</span><b>{e(m["nome"])}</b></nav>

  <div class="pd-grid wrap">
    <div class="pd-stage">{viewer}</div>

    <div class="pd-info">
      <section class="buy" id="comprar">
        <p class="kicker"><span class="area-dot a-{m["area"]}"></span>{e(area_nome)} · {e(area_frase)}</p>
        <h1 class="pd-h1">{e(m["nome"])}</h1>
        <p class="pd-ass">{e(m["assinatura"])}</p>
        <p class="pd-chamada">{e(m["chamada"])}</p>
        <div class="pd-meta">{band_dots(m)}<span><b>{n}</b> {"driver" if n == 1 else "drivers"}{f" · crossover de {c['ways']} vias" if c else ""}</span></div>
        <p class="pd-pra"><span>Indicado para</span>{e(m["indicado"])}</p>
        <div class="pd-preco"><small>a partir de</small><strong>R$ {e(m["preco"])}</strong><span>{"Pronta entrega · frete grátis" if universal else "Personalização orçada na conversa · frete grátis"}</span></div>
        <a class="btn btn-zap btn-lg full" id="ctaZap" href="{zap(msg)}" data-base="{e(msg)}" data-modelo="{e(m["nome"])}" target="_blank" rel="noopener" data-cta="produto">{ICON["zap"]}Quero o meu {e(m["nome"])}</a>
        <p class="pd-prazo">{e(prazo)}</p>
        {perso}
        <ul class="pd-trust"><li><b>1 ano</b> de garantia</li>{"" if universal else "<li><b>60 dias</b> pra ajuste</li>"}<li><b>Feito</b> no Brasil</li></ul>
        {art_html}
      </section>

      {assinatura}

      <section class="pd-sec rv">
        <p class="kicker">Como soa</p>
        <h2 class="h3">{e(m["assinatura"])}</h2>
        <p class="pd-pitch">{e(m["pitch"])}</p>
        <ul class="ouvir">{ouvir}</ul>
      </section>

      <section class="pd-sec rv" id="specs">
        <p class="kicker">Ficha técnica</p>
        <h2 class="h3">Configuração dos drivers</h2>
        <ul class="drv">{drivers}</ul>
        <dl class="specs">{specs}</dl>
      </section>

      <section class="pd-sec rv">
        <p class="kicker">Na caixa</p>
        <ul class="caixa">{caixa}</ul>
      </section>
    </div>
  </div>

{processo}

<section class="sec wrap">
  <ul class="garantias rv">{garantias_html()}</ul>
</section>

<section class="sec wrap">
  <div class="sec-head rv"><p class="kicker">Compare</p><h2 class="h2">Outros que podem servir.</h2></div>
  <div class="grid grid-3">
{irmaos_html}
  </div>
</section>

<section class="sec wrap faq">
  <div class="sec-head rv"><p class="kicker">Dúvidas</p><h2 class="h2">Sobre o {e(m["nome"])}.</h2></div>
  <div class="faq-list">
{faq_html(faq_prod)}
  </div>
</section>
</main>

<div class="bar" id="bar" hidden>
  <div class="bar-in wrap">
    <div class="bar-nome"><b>{e(m["nome"])}</b><span>a partir de R$ {e(m["preco"])}</span></div>
    <a class="btn btn-zap btn-sm" href="{zap(msg)}" data-sync="ctaZap" target="_blank" rel="noopener" data-cta="barra">{ICON["zap"]}<span>Quero o meu</span></a>
  </div>
</div>
{footer(pre)}
{scripts(pre, three=bool(c))}'''
    d = RAIZ / m["slug"]
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(corpo)


# ------------------------------------------------------------------ molde

def molde():
    pre = "../"
    msg = "Olá! Vim pela página do molde no site da Xtreme Ears e quero saber onde fazer o meu pré-molde."
    faq = [
        ("Quem pode fazer o molde?",
         "Só fonoaudiólogo. A Xtreme Ears tem parceria com uma rede de centros auditivos com unidades pelo Brasil, "
         "e você recebe a lista dos mais próximos por e-mail depois da compra, ou na conversa com o especialista."),
        ("Quanto custa a moldagem?",
         "O valor é cobrado pelo fonoaudiólogo e muda de cidade pra cidade. Pergunte ao especialista na hora de pegar a indicação."),
        ("Como sei que o molde ficou bom?",
         "Durante a consulta você pode mandar fotos ou vídeo, ou fazer uma videochamada com a Xtreme Ears. O molde é aprovado ali, "
         "antes de ir pro correio, e só molde aprovado vira fone."),
        ("Como eu envio?",
         "Pelos Correios, com rastreio, identificado com o seu nome e o número do pedido."),
        ("E se mesmo assim o fone não encaixar?",
         "As conchas de acrílico têm 60 dias pra ajuste do molde, o que pode incluir refazer a concha."),
        ("Quanto tempo depois do molde fica pronto?",
         "Cerca de 4 semanas depois que o molde aprovado chega. Se tiver arte no faceplate, conta a partir da arte aprovada também."),
    ]
    corpo = f'''{head("O molde do ouvido | Como funciona o pré-molde | Xtreme Ears",
                    "Como é feito o pré-molde do seu in-ear Xtreme Ears: quem faz, o que precisa ter (concha completa e segunda curva), aprovação por vídeo, envio e prazo.", pre)}
{header(pre, "molde")}
<main id="conteudo">

<section class="mh" data-molde-scroll>
  <div class="mh-sticky">
    <canvas class="mh-canvas" aria-label="Molde de silicone do ouvido se transformando no fone pronto, conforme a rolagem"></canvas>
    <div class="mh-intro wrap">
      <p class="eyebrow">O molde</p>
      <h1 class="h1">O seu fone<br>começa <em>aqui</em>.</h1>
      <p class="lede">Um pedaço de silicone com o formato exato do seu ouvido. Role a página e veja ele virar um Xtreme Ears.</p>
    </div>
    <ol class="mh-steps">
      <li data-s="0"><span class="k">01</span><h2>O molde do seu ouvido</h2><p>O fonoaudiólogo protege o fundo do canal com um tampãozinho de espuma e preenche o ouvido com silicone. Alguns minutos depois, sai o molde.</p></li>
      <li data-s="1"><span class="k">02</span><h2>Concha completa e segunda curva</h2><p>O molde precisa pegar a concha inteira da orelha e passar da segunda curva do canal. É isso que garante vedação e encaixe firme.</p></li>
      <li data-s="2"><span class="k">03</span><h2>Aprovado antes de sair</h2><p>Foto, vídeo ou videochamada com a Xtreme Ears na hora da consulta. Molde com bolha, falha ou canal curto é refeito ali mesmo.</p></li>
      <li data-s="3"><span class="k">04</span><h2>Vira uma concha de acrílico</h2><p>No laboratório, o molde dá forma à concha. O canal é acertado no comprimento de uso e o resto fica idêntico ao seu ouvido.</p></li>
      <li data-s="4"><span class="k">05</span><h2>Drivers, crossover e faceplate</h2><p>Os drivers do modelo que você escolheu são montados à mão lá dentro, e o faceplate fecha o fone com a sua cara.</p></li>
    </ol>
    <div class="mh-bar" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="sec wrap checklist">
  <div class="sec-head rv"><p class="kicker">Checklist do molde</p><h2 class="h2">Leve isso pro fonoaudiólogo.</h2><p class="lede">Molde bom é fone bom. Mostre essa lista na consulta.</p></div>
  <ul class="ck">
    <li class="rv"><b>Concha completa</b><span>O molde ocupa toda a concha da orelha, sem cortes.</span></li>
    <li class="rv"><b>Passa da segunda curva</b><span>O canal vai além da segunda curva. Canal curto é o erro mais comum.</span></li>
    <li class="rv"><b>Sem bolhas nem falhas</b><span>Superfície lisa e inteira, sem buracos ou rebarbas.</span></li>
    <li class="rv"><b>Os dois ouvidos</b><span>Esquerdo e direito, cada um com o seu molde.</span></li>
    <li class="rv"><b>Aprovado na hora</b><span>Foto, vídeo ou videochamada com a Xtreme Ears antes de embalar.</span></li>
    <li class="rv"><b>Identificado</b><span>Nome e número do pedido no pacote. Envio com rastreio.</span></li>
  </ul>
</section>

<section class="sec wrap prazo">
  <div class="sec-head rv"><p class="kicker">Linha do tempo</p><h2 class="h2">Do molde ao palco.</h2></div>
  <ol class="tl rv">
    <li><b>Dia 0</b><span>Conversa com o especialista e indicação do fonoaudiólogo</span></li>
    <li><b>Consulta</b><span>Molde feito e aprovado por vídeo</span></li>
    <li><b>Correio</b><span>Envio com rastreio até a Xtreme Ears</span></li>
    <li><b>~4 semanas</b><span>Produção artesanal do seu fone</span></li>
    <li><b>Entrega</b><span>Frete grátis, 1 ano de garantia e 60 dias pra ajuste</span></li>
  </ol>
</section>

<section class="sec wrap faq">
  <div class="sec-head rv"><p class="kicker">Dúvidas sobre o molde</p><h2 class="h2">O que todo mundo pergunta.</h2></div>
  <div class="faq-list">
{faq_html(faq)}
  </div>
</section>

<section class="sec cta-final">
  <div class="wrap cta-mini rv">
    <h2 class="h2">Quer saber onde fazer<br><span class="dim">o seu molde?</span></h2>
    <p class="lede">Manda a sua cidade. O especialista indica o fonoaudiólogo parceiro mais perto e já te ajuda a escolher o modelo.</p>
    <a class="btn btn-zap btn-lg" href="{zap(msg)}" target="_blank" rel="noopener" data-cta="molde">{ICON["zap"]}Onde faço o meu molde?</a>
  </div>
</section>
</main>
{footer(pre)}
<a class="fab" href="{zap(msg)}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp" data-cta="fab">{ICON["zap"]}</a>
{scripts(pre)}'''
    d = RAIZ / "molde"
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(corpo)


def main():
    home()
    molde()
    for m in D.MODELOS:
        pagina(m)
    print("ok:", 2 + len(D.MODELOS), "páginas")


if __name__ == "__main__":
    main()
