"""
Seção de modelos da home.

Sai daqui e não escrita à mão no index.html, para não divergir das páginas de
cada fone — as duas leem a mesma lista `MODELOS`. O gerador injeta o resultado
entre os marcadores <!-- MODELOS:INICIO --> e <!-- MODELOS:FIM -->.

Cada fone ganha uma linha inteira, alternando o lado da foto, em vez de três
cards espremidos lado a lado.
"""

import html

# ---------------------------------------------------------------- artistas
#
# SÓ entra aqui o que a Xtreme Ears declara publicamente. Afirmar que um
# artista usa um modelo sem fonte é forjar endosso — não preencha de ouvido.
#
# Fontes:
#   banner da home de xtremeears.com.br ... Lauana Prado, Felipe Amorim,
#                                           Marcelo Falcão
#   produto signature no catálogo ......... Aquiles Priester
#
# Os modelos que não aparecem aqui ficam sem a faixa, de propósito. Quando a
# Xtreme Ears passar a lista de quem usa o quê, é só completar.
ARTISTAS_POR_MODELO = {
    "xe4-pro":         [("Lauana Prado",     "lauana-prado.jpg")],
    "xe12-pro":        [("Marcelo Falcão",   "marcelo-falcao.jpg")],
    "xe14-pro":        [("Felipe Amorim",    None)],
    "xe3-pro":         [("Aquiles Priester", "aquiles-priester.jpg")],
    "xtreme-stage":    [("Aquiles Priester", "aquiles-priester.jpg")],
    "xtreme-one-plus": [("Aquiles Priester", "aquiles-priester.jpg")],
}


# ---------------------------------------------------------------- cores
#
# UMA foto serve de base pra todos os modelos; o que muda e a cor do faceplate,
# por filtro CSS. Isso e mais honesto que fingir foto propria por modelo: o
# faceplate e ESCOLHA DO CLIENTE, nao caracteristica do fone. Antes, cada card
# tinha uma foto diferente do catalogo, o que dava a entender que o XE6 "e"
# bege e o XE4 "e" vermelho — e nenhum dos dois e.
#
# A base (assets/fone-base.webp) e rosa saturado, matiz ~325 graus. As cores
# abaixo sao as MESMAS do personalizador da loja.
CORES = {
    "vermelho":          "hue-rotate(38deg) saturate(1.15)",
    "rosa":              "none",
    "rosa-claro":        "hue-rotate(6deg) saturate(.62) brightness(1.12)",
    "azul":              "hue-rotate(-108deg) saturate(1.05)",
    "azul-claro":        "hue-rotate(-96deg) saturate(.7) brightness(1.12)",
    "verde":             "hue-rotate(168deg) saturate(.95)",
    # preto puro sobre fundo preto desaparece: fica mais claro do que o
    # produto real, pra sobrar silhueta. O mesmo motivo separa translucido
    # de transparente, que senao viram o mesmo cinza.
    "preto":             "saturate(.05) brightness(.78) contrast(1.35)",
    "preto-translucido": "saturate(.3) brightness(.56) contrast(1.2)",
    "transparente":      "saturate(.07) brightness(1.35) contrast(.9)",
}

# Os UNIVERSAIS nao entram aqui: eles tem aparencia propria de fabrica, e a
# foto deles e a foto do produto mesmo. Faceplate escolhido pelo cliente so
# existe no moldado — e so por isso a base unica recolorida faz sentido.
SEM_PRE_MOLDE = {"xtreme-stage", "xtreme-one-plus", "xtreme-onemax"}

# uma cor por modelo, so pra linha nao ficar monocromatica
COR_DO_MODELO = {
    "one-plus-pro":    "azul",
    "xe3-pro":         "vermelho",
    "xe6-pro":         "preto-translucido",
    "xe4-pro":         "transparente",
    "xe5-pro":         "rosa",
    "xe8-pro":         "azul-claro",
    "onemax-pro":      "verde",
    "xe12-pro":        "preto",
    "xe14-pro":        "rosa-claro",
}


def tint(slug):
    """Filtro de cor do faceplate. Vazio para quem usa foto propria."""
    if slug in SEM_PRE_MOLDE:
        return "none"
    return CORES.get(COR_DO_MODELO.get(slug, "rosa"), "none")


def foto(slug):
    """Universal mostra o proprio produto; moldado usa a base recolorida."""
    return f"{slug}.webp" if slug in SEM_PRE_MOLDE else "fone-base.webp"

AREA_ORDEM = ["grave", "medio", "agudo", "universal"]

AREA_TEXTO = {
    "grave": ("Bateristas, baixistas, percussionistas e DJs.",
              "Se o bumbo some no meio da banda e você acaba tocando pelo que "
              "sente no chão em vez do que ouve, é aqui que começa."),
    "medio": ("Vocalistas, guitarristas e tecladistas.",
              "O médio é onde mora a sua voz e o seu instrumento — e é a "
              "primeira coisa que o palco engole."),
    "agudo": ("Técnicos de som, produtores e audiófilos.",
              "Quando a sua função é decidir o que vai pro PA ou o que fica na "
              "mixagem, descobrir o problema no vídeo do show depois não serve."),
    "universal": ("Sem pré-molde, pronta entrega.",
                  "Ponteira de silicone ou espuma, sai em até 2 dias úteis. "
                  "Resolve a turnê que começa semana que vem."),
}


def e(t):
    return html.escape(str(t), quote=True)


def _barras(valores):
    return "".join(f'<b style="height:{h}px"></b>' for h in valores)


def _artistas(slug):
    lista = ARTISTAS_POR_MODELO.get(slug)
    if not lista:
        return ""
    caras = ""
    for nome, arq in lista:
        if arq:
            caras += (f'<img src="assets/artistas/{arq}" alt="{e(nome)}" '
                      f'loading="lazy" width="360" height="360">')
        else:
            iniciais = "".join(w[0] for w in nome.split()[:2]).upper()
            caras += f'<span class="sem-foto">{e(iniciais)}</span>'
    nomes = " · ".join(e(n) for n, _ in lista)
    return (f'          <div class="usa-quem">\n'
            f'            <div class="usa-caras">{caras}</div>\n'
            f'            <p><span>Quem usa</span><strong>{nomes}</strong></p>\n'
            f'          </div>\n')


def _linha(m, areas):
    area_nome, _, barras = areas[m["area"]]
    # tres informacoes bastam no card: a configuracao e dois numeros.
    # a ficha completa fica na pagina do modelo.
    chips = [m["drivers"][0]] + [v for _, v in m["specs"][:2]]
    chips_html = "".join(f"<b>{e(c)}</b>" for c in chips)
    return (
        f'      <article class="modelo-linha rv" id="{e(m["slug"])}">\n'
        f'        <a class="modelo-img" href="{e(m["slug"])}/" tabindex="-1" aria-hidden="true">\n'
        f'          <img src="assets/{foto(m["slug"])}" alt="" loading="lazy" width="1200" height="900"\n'
        f'               style="filter:{tint(m["slug"])}">\n'
        f'        </a>\n'
        f'        <div class="modelo-txt">\n'
        f'          <span class="area-tag mini"><i aria-hidden="true">{_barras(barras)}</i>{e(area_nome)}</span>\n'
        f'          <h3><a href="{e(m["slug"])}/">{e(m["nome"])}</a></h3>\n'
        f'          <p class="modelo-assinatura">{e(m["assinatura"])}</p>\n'
        f'          <p class="modelo-para">{e(m["indicado"])}</p>\n'
        f'          <p class="body">{e(m["chamada"])}</p>\n'
        f'          <div class="spec">{chips_html}</div>\n'
        f'{_artistas(m["slug"])}'
        f'          <div class="modelo-pe">\n'
        f'            <span class="card-price">A partir de<b>R$ {e(m["preco"])}</b></span>\n'
        f'            <a class="btn btn-outline btn-sm" href="{e(m["slug"])}/">Ver o {e(m["nome"])}</a>\n'
        f'          </div>\n'
        f'        </div>\n'
        f'      </article>\n')


def secao(todos, areas):
    blocos = []
    for area in AREA_ORDEM:
        da_area = [m for m in todos if m["area"] == area]
        if not da_area:
            continue
        quem, frase = AREA_TEXTO[area]
        nome, titulo, barras = areas[area]
        linhas = "".join(_linha(m, areas) for m in da_area)
        blocos.append(
            f'    <div class="area">\n'
            f'      <header class="area-head rv">\n'
            f'        <div>\n'
            f'          <span class="area-tag"><i aria-hidden="true">{_barras(barras)}</i>{e(nome)}</span>\n'
            f'          <h3>{e(titulo)}.</h3>\n'
            f'        </div>\n'
            f'        <p class="area-who"><b>{e(quem)}</b> {e(frase)}</p>\n'
            f'      </header>\n'
            f'{linhas}    </div>\n')

    return (
        '<!-- ====================== MODELOS POR AREA SONORA ====================== -->\n'
        '<section class="section wrap" id="modelos">\n'
        '  <div class="section-head rv">\n'
        '    <span class="kicker">A linha</span>\n'
        '    <h2 class="h2">Não é sobre quantos drivers.<br>É sobre o que você precisa ouvir.</h2>\n'
        '    <p class="lede">Baterista não ouve o show do mesmo jeito que o cantor, '
        'e o técnico não ouve como nenhum dos dois. Escolha pela sua função no palco.</p>\n'
        '  </div>\n\n'
        f'{"".join(blocos)}'
        '  <p class="tiny" style="margin-top:34px">Valores a partir de, para a configuração '
        'base. Cor da cápsula, faceplate, cabo e logo são orçados junto com o especialista.</p>\n'
        '</section>\n\n')


def injetar(raiz, todos, areas):
    f = raiz / "index.html"
    t = f.read_text(encoding="utf-8")
    ini = t.index("<!-- MODELOS:INICIO -->") + len("<!-- MODELOS:INICIO -->")
    fim = t.index("<!-- MODELOS:FIM -->")
    f.write_text(t[:ini] + "\n" + secao(todos, areas) + t[fim:], encoding="utf-8")
