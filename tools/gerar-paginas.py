#!/usr/bin/env python3
"""
Gera uma pagina por modelo de fone, a partir dos dados do catalogo da Xtreme Ears.

Rodar da raiz do projeto:   python3 tools/gerar-paginas.py

Cada modelo vira <slug>/index.html, entao a URL fica /xe3-pro/ — o vendedor manda
esse link no WhatsApp e o musico abre a apresentacao daquele fone.

Por que gerador e nao 12 arquivos na mao: as paginas compartilham nav, rodape,
processo, garantia e CTA. Escritas separadamente, divergem na primeira correcao.
Specs, configuracao de drivers e "indicado para" vem do catalogo e das tarjas das
fotos oficiais — nao invente numero aqui.
"""

import html
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import home_modelos
from home_modelos import tint, foto

WHATS = "5511950295494"

# Muda a cada deploy que mexa em site.css ou site.js: sem isso o navegador
# serve a versao em cache e o site quebra em pedacos dificeis de diagnosticar.
VERSAO_ASSETS = "202610032105"

CAIXA_MOLDADO = [
    "Fone de ouvido in ear moldado",
    "Ferramenta de limpeza para o duto de saída",
    "Desumidificador de sílica gel",
    "Plug adaptador estéreo",
    "Cordão Xtreme Ears",
    "Manual do usuário",
]

AREAS = {
    "grave": ("Grave", "Pra quem segura o tempo", [14, 9, 5]),
    "medio": ("Médio", "Pra quem canta e pra quem faz a melodia", [6, 14, 7]),
    "agudo": ("Agudo e detalhe", "Pra quem precisa ouvir tudo", [5, 9, 14]),
    "universal": ("Universal", "Sem pré-molde, sai em 2 dias úteis", [9, 9, 9]),
}

# ---------------------------------------------------------------- modelos

MODELOS = [
    {
        "slug": "one-plus-pro", "nome": "XE ONE+/PRO", "area": "grave",
        "preco": "2.690", "flag": "Primeiro moldado",
        "indicado": "Bateristas, baixistas e guitarristas",
        "assinatura": "Separação instrumental e som limpo",
        "chamada": "O primeiro moldado. Três drivers, e cada faixa no seu lugar.",
        "pitch": "É o fone de quem está saindo do universal e descobrindo o que estava "
                 "perdendo. Com três microdrivers e crossover de três vias, o bumbo para "
                 "de embolar com o baixo e a guitarra para de brigar com o vocal — cada "
                 "faixa de frequência tem um transdutor só dela. A separação instrumental "
                 "é a primeira coisa que você nota, e é a que mais muda o jeito de tocar.",
        "ouvir": [
            ("Separação instrumental", "Cada instrumento ocupa um espaço próprio. Você para de adivinhar o que é seu no meio da banda."),
            ("Som limpo em qualquer volume", "Baixa distorção mesmo quando o palco sobe, porque nenhum driver está fazendo trabalho de dois."),
            ("Resposta coerente", "Transição suave entre grave, médio e agudo — nada salta, nada some."),
        ],
        "drivers": ["3 microdrivers de armadura balanceada", "1 driver para graves",
                    "1 driver para médias", "1 driver para altas frequências",
                    "1 crossover integrado de três vias"],
        "specs": [],
    },
    {
        "slug": "xe3-pro", "nome": "XE3/PRO", "area": "grave",
        "preco": "4.280", "flag": "O rei do punch",
        "indicado": "Bateristas e baixistas",
        "assinatura": "O rei do punch",
        "chamada": "O grave bate no peito. E ainda sobra fôlego quando a banda sobe.",
        "pitch": "Se o seu problema é sentir o tempo, é esse. Dois dos três microdrivers "
                 "cuidam de graves e médias, e o resultado é o modelo com maior "
                 "sensibilidade e headroom dinâmico da linha — o técnico não precisa "
                 "forçar o seu canal pra você se achar. É o fone de quem toca atrás do kit "
                 "ou segura o baixo e precisa do ataque, não só da nota.",
        "ouvir": [
            ("Punch com ataque", "O bumbo chega com corpo e com a batida definida, não como um borrão grave."),
            ("Headroom de sobra", "123 dB/mW de sensibilidade: sobra volume quando o refrão inteiro entra."),
            ("Grave que não embola", "O crossover de duas vias deixa o grave largo sem invadir o médio."),
        ],
        "drivers": ["3 microdrivers de armadura balanceada",
                    "2 drivers para graves e médias frequências",
                    "1 driver para altas frequências",
                    "1 crossover integrado de duas vias"],
        "specs": [("Impedância (1 kHz)", "35 Ω"), ("Sensibilidade", "123 dB/mW"),
                  ("Resposta de frequência", "20 Hz – 16 kHz")],
    },
    {
        "slug": "xe6-pro", "nome": "XE6/PRO", "area": "grave",
        "preco": "5.890", "flag": None,
        "indicado": "Bateristas, baixistas e percussionistas",
        "assinatura": "Peso com leitura fina",
        "chamada": "O peso do XE3, com detalhe pra ouvir a mão e a baqueta.",
        "pitch": "Seis microdrivers com drivers duplos para graves e médias, mais dois "
                 "dedicados às altas. Dá o mesmo corpo embaixo e devolve o que falta num "
                 "fone só de punch: a diferença entre o tom e o surdo, entre o prato e o "
                 "chimbal, entre a mão e a baqueta. É pra quem já sabe o que quer do kit e "
                 "precisa de leitura fina pra chegar lá.",
        "ouvir": [
            ("Detalhe dentro do grave", "Você ouve a textura da pele e do corpo do tambor, não só o impacto."),
            ("Agudo aberto", "Dois drivers só pras altas: pratos com brilho e sem aspereza."),
            ("Resposta estendida", "De 10 Hz a 20 kHz, com crossover passivo de três vias."),
        ],
        "drivers": ["6 microdrivers de armadura balanceada", "1 driver duplo para graves",
                    "1 driver duplo para médias", "2 drivers para altas frequências",
                    "1 crossover passivo de três vias"],
        "specs": [("Impedância (1 kHz)", "30 Ω"), ("Sensibilidade", "122 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 20 kHz")],
    },
    {
        "slug": "xe4-pro", "nome": "XE4/PRO", "area": "medio",
        "preco": "4.680", "flag": "Flat",
        "indicado": "Vocalistas, técnicos de som e guitarristas",
        "assinatura": "A definição de flat",
        "chamada": "Sua voz sai do retorno do mesmo jeito que entrou no microfone.",
        "pitch": "Resposta plana de verdade: nada empurrado, nada escondido. O agudo "
                 "aparece sem acentuação, o médio fica equilibrado e o grave se soma ao "
                 "sub de forma homogênea. É por isso que técnico de som pede esse modelo — "
                 "o que ele ouve no fone é o que está indo pro PA. E é por isso que "
                 "cantor confia: a afinação não vem maquiada.",
        "ouvir": [
            ("Nada maquiado", "Sem realce em nenhuma região. O que você ouve é o que foi captado."),
            ("Voz na frente", "O médio não é engolido pelo grave, então você se acha na afinação sem pedir volume."),
            ("Referência confiável", "Mesma leitura no palco à noite e na mixagem no dia seguinte."),
        ],
        "drivers": ["4 microdrivers de armadura balanceada", "1 driver duplo para graves",
                    "1 driver para médias", "1 driver para altas frequências",
                    "1 crossover passivo de três vias"],
        "specs": [("Impedância (1 kHz)", "25 Ω"), ("Sensibilidade", "118 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 17 kHz")],
    },
    {
        "slug": "xe5-pro", "nome": "XE5/PRO", "area": "medio",
        "preco": "5.290", "flag": None,
        "indicado": "Vocalistas, técnicos de som e guitarristas",
        "assinatura": "Transparente e cirúrgico",
        "chamada": "Guitarra com corpo sem comer o vocal.",
        "pitch": "O XE4 com mais resolução. Drivers duplos para graves e médias, mais um "
                 "de precisão nas altas, entregam uma assinatura transparente e cirúrgica. "
                 "A guitarra ganha corpo sem invadir o espaço da voz, e a voz não "
                 "desaparece quando a banda inteira sobe. Serve o palco à noite e a "
                 "referência de estúdio no dia seguinte sem trocar de fone.",
        "ouvir": [
            ("Alta resolução", "Camadas que somem em fones mais simples continuam audíveis aqui."),
            ("Médio protegido", "Drivers duplos nas médias seguram a voz no lugar mesmo com a banda cheia."),
            ("Versátil", "Transparente o suficiente pra mixar, encorpado o suficiente pro palco."),
        ],
        "drivers": ["5 microdrivers de armadura balanceada", "1 driver duplo para graves",
                    "1 driver duplo para médias", "1 driver para altas frequências",
                    "1 crossover passivo de três vias"],
        "specs": [("Impedância (1 kHz)", "25 Ω"), ("Sensibilidade", "118 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 17 kHz")],
    },
    {
        "slug": "xe8-pro", "nome": "XE8/PRO", "area": "medio",
        "preco": "7.890", "flag": None,
        "indicado": "Vocalistas, tecladistas e guitarristas",
        "assinatura": "Grave articulado, médio na frente",
        "chamada": "Quatro drivers só pro grave — e o médio ainda na frente.",
        "pitch": "Oito microdrivers, com quatro dedicados exclusivamente aos graves, e "
                 "mesmo assim a voz continua na frente. É o equilíbrio entre a energia que "
                 "o palco grande exige e a naturalidade que o cantor precisa. Feito pra "
                 "show com naipe de sopro, teclado em camada sobre camada e banda cheia, "
                 "onde grave demais costuma custar a própria voz.",
        "ouvir": [
            ("Grave texturizado", "Quatro drivers embaixo entregam presença articulada, não um borrão."),
            ("Voz preservada", "O driver duplo de médias segura o vocal mesmo com todo esse grave."),
            ("Naturalidade", "Equilíbrio e sofisticação pra qualquer estilo, do gospel ao rock."),
        ],
        "drivers": ["8 microdrivers de armadura balanceada", "4 drivers para graves",
                    "1 driver duplo para médias", "2 drivers para altas frequências",
                    "1 crossover passivo de três vias"],
        "specs": [("Impedância (1 kHz)", "22 Ω"), ("Sensibilidade", "118 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 20 kHz")],
    },
    {
        "slug": "onemax-pro", "nome": "XE ONEMAX/PRO", "area": "agudo",
        "preco": "3.990", "flag": "Mais musical",
        "indicado": "Técnicos de som, vocalistas e tecladistas",
        "assinatura": "Musical, aveludado e equilibrado",
        "chamada": "Agudo cristalino sem o brilho que cansa.",
        "pitch": "Quatro microdrivers — dois para graves, um para médias e um para altas — "
                 "com crossover integrado de três vias. Grave aveludado por baixo e agudo "
                 "cristalino em cima, sem a aspereza que faz o ouvido pedir pausa. É o "
                 "mais musical da faixa de entrada, e quem ensaia de fone todo dia sente a "
                 "diferença no fim do dia, não nos primeiros dez minutos.",
        "ouvir": [
            ("Agudo sem fadiga", "Cristalino sem o pico agressivo que cansa em ensaio longo."),
            ("Grave aveludado", "Dois drivers embaixo dão corpo sem endurecer o som."),
            ("Equilíbrio musical", "Favorito de cantor e audiófilo justamente por não cansar."),
        ],
        "drivers": ["4 microdrivers de armadura balanceada", "2 drivers para graves",
                    "1 driver para médias", "1 driver para altas frequências",
                    "1 crossover integrado de três vias"],
        "specs": [("Impedância (1 kHz)", "28 Ω"), ("Sensibilidade", "117 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 20 kHz")],
    },
    {
        "slug": "xe12-pro", "nome": "XE12/PRO", "area": "agudo",
        "preco": "11.890", "flag": "Padrão ouro",
        "indicado": "Vocalistas, audiófilos, técnicos e produtores",
        "assinatura": "Resolução máxima e palco sonoro",
        "chamada": "O problema aparece na hora. Não no vídeo do show depois.",
        "pitch": "Doze microdrivers em quatro vias de verdade: quatro só para subgraves, "
                 "quatro para graves, dois para médias e dois para altas. A separação de "
                 "frequências e o palco sonoro colocam cada instrumento num lugar próprio, "
                 "e é isso que permite achar o problema enquanto ele acontece. É o padrão "
                 "ouro da indústria pra quem decide o que vai pro PA ou pra mixagem.",
        "ouvir": [
            ("Subgrave separado do grave", "Quatro drivers só pro sub: você ouve a extensão sem perder a definição do grave."),
            ("Palco sonoro", "Cada instrumento com posição própria — dá pra apontar de onde vem cada coisa."),
            ("Resolução cirúrgica", "Detalhe suficiente pra decidir em tempo real, não depois."),
        ],
        "drivers": ["12 microdrivers de armadura balanceada", "4 drivers para subgraves",
                    "4 drivers para graves", "2 drivers para médias",
                    "2 drivers para altas frequências",
                    "1 crossover integrado de quatro vias"],
        "specs": [("Impedância (1 kHz)", "15 Ω"), ("Sensibilidade", "118 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 20 kHz")],
    },
    {
        "slug": "xe14-pro", "nome": "XE14/PRO", "area": "agudo",
        "preco": "18.990", "flag": "Topo da linha",
        "indicado": "Audiófilos — o som mais puro",
        "assinatura": "O topo absoluto da linha",
        "chamada": "O que você escuta aqui é o que está na gravação. Ponto.",
        "pitch": "O flagship. Catorze microdrivers num crossover de quatro vias, com o "
                 "HexaDrive Array™ — seis drivers em formação hexagonal dedicados só às "
                 "médias, a faixa mais crítica do espectro — e o driver E50D de alta "
                 "frequência, com resposta estendida até 50 kHz. Tecnologia de cancelamento "
                 "de distorção harmônica mantém a pureza dos médios mesmo em volume alto.",
        "ouvir": [
            ("HexaDrive Array™", "Seis drivers só pros médios: clareza vocal e instrumental sem precedente na faixa mais crítica."),
            ("Driver E50D", "Agudo cristalino com extensão até 50 kHz — além do audível, mas o harmônico se sente."),
            ("Distorção ultrabaixa", "Pureza mantida no volume de palco, não só no volume de teste."),
        ],
        "drivers": ["14 microdrivers de armadura balanceada",
                    "6 drivers para médias — HexaDrive Array™",
                    "Driver E50D para altas frequências",
                    "1 crossover integrado de quatro vias"],
        "specs": [("Resposta de frequência", "estendida até 50 kHz"),
                  ("Crossover", "4 vias")],
    },
    # ------------------------------------------------------------ universais
    {
        "slug": "xtreme-stage", "nome": "Xtreme Stage", "area": "universal",
        "preco": "890", "flag": "Primeiro in-ear", "universal": True,
        "indicado": "Quem curte um verdadeiro som",
        "assinatura": "O primeiro in-ear",
        "chamada": "Pra começar a ouvir direito sem esperar quatro semanas.",
        "pitch": "Driver dinâmico de neodímio numa cápsula ergonômica e resistente, com "
                 "acoplador acústico de tecnologia 3D que elimina vazamento e protege o "
                 "driver. Som detalhado e grave profundo pra ensaio, estudo e dia a dia. "
                 "Sai em até 2 dias úteis, sem pré-molde.",
        "ouvir": [
            ("Grave profundo", "O ímã de neodímio entrega corpo que surpreende pro tamanho."),
            ("Conforto prolongado", "Design anatômico pensado pra uso intensivo."),
            ("Pronta entrega", "Sem pré-molde, sem espera de produção."),
        ],
        "drivers": ["1 driver dinâmico de neodímio", "1 crossover integrado",
                    "Acoplador acústico de tecnologia 3D"],
        "specs": [("Impedância (1 kHz)", "16 Ω"), ("Sensibilidade", "117 dB/mW"),
                  ("Resposta de frequência", "20 Hz – 17 kHz")],
    },
    {
        "slug": "xtreme-one-plus", "nome": "Xtreme One Plus", "area": "universal",
        "preco": "2.200", "flag": "Topo do universal", "universal": True,
        "indicado": "Músicos e audiófilos",
        "assinatura": "Topo da linha universal",
        "chamada": "O universal que chega mais perto de um moldado.",
        "pitch": "Três microdrivers de armadura balanceada com tecnologia Knowles e "
                 "crossover integrado de três vias, que minimiza a interferência entre as "
                 "faixas e resulta em baixa distorção e melhor clareza. Cabo trançado "
                 "removível, então manutenção e troca não aposentam o fone. Ponteiras de "
                 "espuma e silicone acompanham.",
        "ouvir": [
            ("Três drivers dedicados", "Grave, médio e agudo cada um no seu transdutor, como na linha PRO."),
            ("Alta resolução", "Graves profundos, médios transparentes e agudos ricos em detalhe."),
            ("Cabo removível", "Troca sem perder o fone — o cabo é a peça que mais sofre."),
        ],
        "drivers": ["3 microdrivers de armadura balanceada com tecnologia Knowles",
                    "1 crossover integrado de três vias", "Cabo trançado removível",
                    "Ponteiras de espuma e silicone"],
        "specs": [("Impedância (1 kHz)", "26 Ω"), ("Sensibilidade", "121 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 17 kHz")],
    },
    {
        "slug": "xtreme-onemax", "nome": "Xtreme ONEMAX", "area": "universal",
        "preco": "2.890", "flag": None, "universal": True,
        "indicado": "Cantores, tecladistas e audiófilos",
        "assinatura": "Quatro drivers sem pré-molde",
        "chamada": "A assinatura da linha PRO, em formato universal.",
        "pitch": "Quatro drivers de armadura balanceada — dois para graves, um para médias "
                 "e um para altas — com crossover integrado de três vias. É a forma de "
                 "ouvir o que você vai encontrar no moldado antes de encomendar o seu. "
                 "Cabo trançado removível e acoplador acústico 3D.",
        "ouvir": [
            ("Quatro drivers", "Mesma lógica do ONEMAX/PRO: dois no grave, um no médio, um no agudo."),
            ("Equilíbrio musical", "Clareza e alta definição sem a aspereza que cansa."),
            ("Caminho pro moldado", "Serve de reserva depois que o seu moldado chegar."),
        ],
        "drivers": ["4 microdrivers de armadura balanceada", "2 drivers para graves",
                    "1 driver para médias", "1 driver para altas frequências",
                    "1 crossover integrado de três vias"],
        "specs": [("Impedância (1 kHz)", "28 Ω"), ("Sensibilidade", "117 dB/mW"),
                  ("Resposta de frequência", "10 Hz – 20 kHz")],
    },
]

# prova social por area — reels reais do @xtremeears
REEL_POR_AREA = {
    "grave":     ("DdpiEGPMb8i", "Heitor Gomes", "Baixista — rock brasileiro"),
    "medio":     ("Dd2HSHGSWDA", "Lucas Lima", "Cantor — Pagode dos Ex"),
    "agudo":     ("DdkE-7uSR2n", "Paulo Farat", "Engenheiro de som"),
    "universal": ("Dd91oj4yZCL", "Xtreme Ears", "Do retorno de chão ao in-ear"),
}


def e(t):
    return html.escape(str(t), quote=True)


def zap(modelo):
    msg = (f"Olá! Vim pela página do {modelo} no site da Xtreme Ears "
           f"e queria falar com um especialista sobre esse modelo.")
    from urllib.parse import quote
    return f"https://wa.me/{WHATS}?text={quote(msg)}"


def pagina(m, todos):
    area_nome, area_frase, barras = AREAS[m["area"]]
    universal = m.get("universal", False)
    reel, reel_nome, reel_papel = REEL_POR_AREA[m["area"]]

    irmaos = [o for o in todos if o["area"] == m["area"] and o["slug"] != m["slug"]][:3]
    if len(irmaos) < 2:
        irmaos += [o for o in todos if o["slug"] != m["slug"]
                   and o not in irmaos][:2 - len(irmaos)]

    barras_html = "".join(f'<b style="height:{h}px"></b>' for h in barras)

    ouvir_html = "\n".join(
        f'''      <article class="ouvir-item rv">
        <h3>{e(t)}</h3>
        <p>{e(d)}</p>
      </article>''' for t, d in m["ouvir"])

    drivers_html = "\n".join(f"        <li>{e(d)}</li>" for d in m["drivers"])

    specs_html = "\n".join(
        f'        <div class="spec-linha"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>'
        for k, v in m["specs"]) or \
        '        <div class="spec-linha"><dt>Configuração</dt><dd>sob consulta</dd></div>'

    caixa_html = "\n".join(f"        <li>{e(i)}</li>" for i in CAIXA_MOLDADO) \
        if not universal else \
        "\n".join(f"        <li>{e(i)}</li>" for i in
                  ["Fone de ouvido in ear universal", "Kit de ponteiras de silicone e espuma",
                   "Estojo", "Manual do usuário"])

    irmaos_html = "\n".join(f'''      <a class="irmao rv" href="../{o["slug"]}/">
        <img src="../assets/{foto(o["slug"])}" alt="{e(o["nome"])}" loading="lazy" width="1200" height="900" style="filter:{tint(o["slug"])}">
        <div><strong>{e(o["nome"])}</strong><span>{e(o["assinatura"])}</span>
        <em>A partir de R$ {e(o["preco"])}</em></div>
      </a>''' for o in irmaos)

    processo = "" if universal else f'''
<!-- ============================ PROCESSO ============================ -->
<section class="section wrap">
  <div class="section-head rv">
    <span class="kicker">Como você recebe o seu</span>
    <h2 class="h2">Do primeiro contato<br>ao {e(m["nome"])} no palco.</h2>
  </div>
  <div class="steps">
    <article class="step rv"><h4>Conversa com o especialista</h4><p>Você conta o que toca e onde toca. Confirmamos se o {e(m["nome"])} é mesmo o certo — ou se outro modelo serve melhor.</p></article>
    <article class="step rv"><h4>Pré-molde com fonoaudiólogo</h4><p>Indicamos um profissional perto de você. O molde é do tipo concha completa e inclui a segunda curva do canal.</p></article>
    <article class="step rv"><h4>Aprovação antes de produzir</h4><p>Você manda fotos, vídeo ou faz videochamada com o time. Só seguimos com o pré-molde aprovado.</p></article>
    <article class="step rv"><h4>Personalização</h4><p>Cores da cápsula, faceplate, cabo e a sua logomarca gravada, se quiser.</p></article>
    <article class="step rv"><h4>Produção e entrega</h4><p>Cerca de 4 semanas após o pré-molde chegar, com frete grátis e garantia de 1 ano.</p></article>
  </div>
</section>'''

    prazo = ("Pronta entrega — sai em até 2 dias úteis"
             if universal else "Produção em ~4 semanas após o pré-molde")

    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(m["nome"])} — {e(m["assinatura"])} | Xtreme Ears</title>
<meta name="description" content="{e(m["nome"])}: {e(m["chamada"])} Indicado para {e(m["indicado"].lower())}. A partir de R$ {e(m["preco"])}.">
<meta name="theme-color" content="#000000">
<link rel="icon" href="../assets/logo-xtreme-branco.png" type="image/png">
<meta property="og:title" content="{e(m["nome"])} — Xtreme Ears">
<meta property="og:description" content="{e(m["chamada"])}">
<meta property="og:image" content="../assets/{foto(m["slug"])}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700;9..40,800;9..40,900&display=swap">
<link rel="stylesheet" href="../assets/site.css?v={VERSAO_ASSETS}">
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>

<header class="nav">
  <div class="nav-in">
    <a class="brand" href="../" aria-label="Xtreme Ears — início">
      <img src="../assets/logo-xtreme-branco.png" alt="" width="104" height="26">
    </a>
    <nav class="nav-links" aria-label="Principal">
      <a href="../#porque">Por que moldado</a>
      <a href="../#modelos">Modelos por área</a>
      <a href="../#processo">Como funciona</a>
      <a href="../#artistas">Quem usa</a>
      <a href="../#duvidas">Dúvidas</a>
    </nav>
    <div class="nav-right">
      <a class="btn btn-primary btn-sm" href="{zap(m["nome"])}" target="_blank" rel="noopener">Falar sobre o {e(m["nome"])}</a>
      <button class="burger" id="burger" aria-expanded="false" aria-controls="drawer" aria-label="Abrir menu"><span></span></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer">
  <a href="../#porque">Por que moldado</a>
  <a href="../#modelos">Modelos por área</a>
  <a href="../#processo">Como funciona</a>
  <a href="../#artistas">Quem usa</a>
  <a href="../#duvidas">Dúvidas</a>
  <a class="btn btn-primary" href="{zap(m["nome"])}" target="_blank" rel="noopener">Falar sobre o {e(m["nome"])}</a>
</div>

<main id="conteudo">

<!-- ============================ HERO DO MODELO ============================ -->
<section class="modelo-hero">
  <div class="wrap modelo-hero-in">
    <div class="modelo-texto">
      <a class="voltar" href="../#modelos">← Todos os modelos</a>
      <span class="area-tag"><i aria-hidden="true">{barras_html}</i>Área {e(area_nome)}</span>
      <h1 class="h1">{e(m["nome"])}</h1>
      <p class="modelo-assinatura">{e(m["assinatura"])}</p>
      <p class="lede">{e(m["chamada"])}</p>
      <div class="modelo-meta">
        <div><span>Indicado para</span><strong>{e(m["indicado"])}</strong></div>
        <div><span>A partir de</span><strong>R$ {e(m["preco"])}</strong></div>
      </div>
      <div class="btn-row">
        <a class="btn btn-primary" href="{zap(m["nome"])}" target="_blank" rel="noopener">Falar com um especialista</a>
        <a class="btn btn-outline" href="#specs">Ver especificações</a>
      </div>
      <p class="tiny" style="margin-top:20px">{e(prazo)} · Garantia de 1 ano · Frete grátis</p>
    </div>
    <figure class="modelo-foto">
      <img src="../assets/{foto(m["slug"])}" alt="{e(m["nome"])}" width="1200" height="900" fetchpriority="high" style="filter:{tint(m["slug"])}">
      {f'<figcaption class="card-flag">{e(m["flag"])}</figcaption>' if m.get("flag") else ''}
    </figure>
  </div>
</section>

<!-- ============================ PITCH ============================ -->
<section class="section wrap">
  <div class="section-head rv">
    <span class="kicker">Pra quem é</span>
    <h2 class="h2">{e(area_frase)}.</h2>
    <p class="lede">{e(m["pitch"])}</p>
  </div>

  <div class="ouvir-grid">
{ouvir_html}
  </div>
</section>

<!-- ============================ PROVA SOCIAL ============================ -->
<section class="section band">
  <div class="wrap">
    <div class="section-head rv">
      <span class="kicker">Quem já usa</span>
      <h2 class="h2">{e(reel_nome)} explica.</h2>
      <p class="body">{e(reel_papel)}</p>
    </div>
    <div class="reel-um rv">
      <blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/reel/{reel}/" data-instgrm-version="14"></blockquote>
    </div>
  </div>
</section>

<!-- ============================ SPECS ============================ -->
<section class="section wrap" id="specs">
  <div class="section-head rv">
    <span class="kicker">Por dentro</span>
    <h2 class="h2">Como o {e(m["nome"])} é feito.</h2>
  </div>

  <div class="ficha">
    <div class="ficha-bloco rv">
      <h3 class="h3">Configuração dos drivers</h3>
      <ul class="lista">
{drivers_html}
      </ul>
    </div>
    <div class="ficha-bloco rv">
      <h3 class="h3">Especificações</h3>
      <dl class="specs-dl">
{specs_html}
      </dl>
    </div>
    <div class="ficha-bloco rv">
      <h3 class="h3">Na caixa</h3>
      <ul class="lista">
{caixa_html}
      </ul>
    </div>
  </div>
</section>
{processo}

<!-- ============================ IRMÃOS ============================ -->
<section class="section wrap">
  <div class="section-head rv">
    <span class="kicker neutral">Comparar</span>
    <h2 class="h2">Na dúvida entre esse e outro?</h2>
    <p class="body">É exatamente pra isso que o atendimento existe. Mas se quiser olhar antes:</p>
  </div>
  <div class="irmaos">
{irmaos_html}
  </div>
</section>

<!-- ============================ CTA ============================ -->
<section class="final">
  <div class="final-media">
    <img src="../assets/artista-felipe.jpg" alt="" loading="lazy" width="1920" height="1080" aria-hidden="true">
  </div>
  <div class="final-in wrap">
    <h2 class="h1 rv">O {e(m["nome"])} ainda não existe.<br>Vamos fazer o seu.</h2>
    <p class="lede rv">Um especialista com você do primeiro contato até a primeira música.</p>
    <div class="btn-row rv">
      <a class="btn btn-primary" href="{zap(m["nome"])}" target="_blank" rel="noopener">Falar sobre o {e(m["nome"])}</a>
      <a class="btn btn-outline" href="tel:+551132562692">Ligar: (11) 3256-2692</a>
    </div>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="../" aria-label="Xtreme Ears"><img src="../assets/logo-xtreme-branco.png" alt="Xtreme Ears" width="120" height="30"></a>
        <p class="body" style="margin-top:20px;max-width:34ch">In-ear moldados sob medida, fabricados no Brasil. Pioneira no país, mais de 15 anos acompanhando músicos do primeiro contato ao palco.</p>
      </div>
      <div>
        <h5>Navegue</h5>
        <ul>
          <li><a href="../#porque">Por que moldado</a></li>
          <li><a href="../#encontre">Encontre seu fone</a></li>
          <li><a href="../#modelos">Modelos por área</a></li>
          <li><a href="../#processo">Como funciona</a></li>
          <li><a href="../#duvidas">Dúvidas</a></li>
        </ul>
      </div>
      <div>
        <h5>Atendimento</h5>
        <ul>
          <li><a href="{zap(m["nome"])}" target="_blank" rel="noopener">WhatsApp: (11) 95029-5494</a></li>
          <li><a href="tel:+551132562692">Telefone: (11) 3256-2692</a></li>
          <li><a href="mailto:contato@xtremeears.com.br">contato@xtremeears.com.br</a></li>
          <li>Segunda a sexta, 9h às 17h</li>
        </ul>
      </div>
      <div>
        <h5>Onde estamos</h5>
        <ul><li>Rua Dom José de Barros, 152<br>conj. 95/96 — Centro<br>São Paulo / SP</li></ul>
      </div>
    </div>
    <div class="foot-bottom">
      <p>© <span id="ano">2026</span> Xtreme Ears. Todos os direitos reservados.</p>
      <p>Sinta o verdadeiro som.</p>
    </div>
  </div>
</footer>

<a class="float show" href="{zap(m["nome"])}" target="_blank" rel="noopener">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21h.01c5.46 0 9.91-4.45 9.91-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14.1c-.24.68-1.4 1.3-1.95 1.38-.5.07-1.13.1-1.82-.11-.42-.13-.96-.31-1.65-.61-2.9-1.25-4.8-4.17-4.94-4.37-.15-.2-1.19-1.58-1.19-3.02 0-1.43.75-2.14 1.02-2.43.27-.29.58-.36.78-.36l.56.01c.18.01.42-.07.66.5.24.59.83 2.02.9 2.17.07.15.12.32.02.51-.1.2-.15.32-.29.49-.15.17-.31.38-.44.51-.15.15-.3.31-.13.6.17.29.76 1.25 1.63 2.03 1.12 1 2.06 1.31 2.35 1.46.29.15.46.12.63-.07.17-.2.73-.85.92-1.14.2-.29.39-.24.66-.15.27.1 1.7.8 1.99.95.29.15.49.22.56.34.07.12.07.69-.17 1.37z"/></svg>
  Falar agora
</a>

<script async src="https://www.instagram.com/embed.js"></script>
<script src="../assets/site.js?v={VERSAO_ASSETS}"></script>
</body>
</html>
'''


def main():
    raiz = pathlib.Path(__file__).resolve().parent.parent
    for m in MODELOS:
        destino = raiz / m["slug"]
        destino.mkdir(exist_ok=True)
        (destino / "index.html").write_text(pagina(m, MODELOS), encoding="utf-8")
        print(f"  {m['slug']}/index.html")
    home_modelos.injetar(raiz, MODELOS, AREAS)
    print(f"\n{len(MODELOS)} páginas + seção de modelos da home.")


if __name__ == "__main__":
    main()
