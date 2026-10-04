"""
Blocos das páginas de modelo que existem para o músico, não para o catálogo.

- `assinatura()` mostra onde o modelo gasta os drivers (grave/médio/agudo).
  É o dado que o músico realmente compara, e é mais útil que a tabela de
  impedância — que fica na ficha, mais abaixo.
- `personalizador()` deixa ele trocar a cor do faceplate ali mesmo, antes de
  falar com o vendedor. Só aparece no moldado: universal não tem faceplate
  escolhido pelo cliente.
"""

import html

from home_modelos import CORES, SEM_PRE_MOLDE, filtro, foto


def e(t):
    return html.escape(str(t), quote=True)


# Quantos drivers o modelo dedica a cada faixa, da "Configuração dos drivers"
# do catálogo. NÃO invente número aqui. (0,0,0) esconde o gráfico; a nota
# explica configuração compartilhada ou divisão não divulgada.
FAIXAS = {
    "one-plus-pro":    ((1, 1, 1), None),
    "onemax-pro":      ((2, 1, 1), None),
    "xe3-pro":         ((2, 2, 1), "Os dois drivers de grave e médio são os mesmos — "
                                   "o crossover é de duas vias, não de três."),
    "xe4-pro":         ((2, 1, 1), "O grave é um driver duplo."),
    "xe5-pro":         ((2, 2, 1), "Grave e médio são drivers duplos."),
    "xe6-pro":         ((2, 2, 2), "Grave e médio são drivers duplos."),
    "xe8-pro":         ((4, 2, 2), "Quatro drivers dedicados só ao grave, "
                                   "e o médio é um driver duplo."),
    "xe12-pro":        ((8, 2, 2), "Dos oito graves, quatro são de subgrave — "
                                   "por isso o crossover é de quatro vias."),
    "xe14-pro":        ((0, 6, 0), "A Xtreme Ears publica os seis médios do HexaDrive "
                                   "Array™ e o driver E50D de alta; a divisão completa "
                                   "dos catorze não é divulgada."),
    "xtreme-stage":    ((0, 0, 0), None),
    "xtreme-one-plus": ((1, 1, 1), None),
    "xtreme-onemax":   ((2, 1, 1), None),
}

BANDAS = (
    ("Grave", "o bumbo, o baixo, o peso"),
    ("Médio", "a sua voz, a guitarra, o teclado"),
    ("Agudo", "o prato, o brilho, o ar"),
)


def assinatura(slug):
    dados = FAIXAS.get(slug)
    if not dados or sum(dados[0]) == 0:
        return ""
    contagem, nota = dados
    pico = max(contagem) or 1

    linhas = ""
    for (rotulo, quem), n in zip(BANDAS, contagem):
        pct = round(n / pico * 100)
        plural = "driver" if n == 1 else "drivers"
        linhas += (
            '      <div class="faixa">\n'
            f'        <span class="faixa-nome">{rotulo}</span>\n'
            f'        <span class="faixa-barra"><i style="width:{pct}%"></i></span>\n'
            f'        <span class="faixa-n">{n} <small>{plural}</small></span>\n'
            f'        <span class="faixa-quem">{quem}</span>\n'
            '      </div>\n')

    rodape = f'    <p class="tiny" style="margin-top:20px">{e(nota)}</p>\n' if nota else ""

    return (
        '<!-- ====================== ASSINATURA SONORA ====================== -->\n'
        '<section class="section wrap">\n'
        '  <div class="section-head rv">\n'
        '    <span class="kicker">Assinatura sonora</span>\n'
        '    <h2 class="h2">Onde esse fone<br>gasta os drivers.</h2>\n'
        '    <p class="lede">Um in-ear não fica melhor por ter mais drivers. '
        'Fica melhor por colocar driver onde você precisa ouvir. Esta é a divisão '
        'deste modelo.</p>\n'
        '  </div>\n'
        '  <div class="faixas rv">\n'
        f'{linhas}'
        '  </div>\n'
        f'{rodape}'
        '</section>\n\n')


# as cores do personalizador da loja, na ordem em que aparecem lá
PALETA = [
    ("Transparente",      "transparente"),
    ("Preto",             "preto"),
    ("Preto translúcido", "preto-translucido"),
    ("Azul",              "azul"),
    ("Verde",             "verde"),
    ("Vermelho",          "vermelho"),
    ("Rosa",              "rosa"),
]


def personalizador(m, zap):
    if m["slug"] in SEM_PRE_MOLDE:
        return ""

    botoes = "".join(
        f'<button class="cor" type="button" data-filtro="{CORES[cod]}" '
        f'data-nome="{e(nome)}"><span class="pastilha pastilha-{cod}"></span>'
        f'<em>{e(nome)}</em></button>\n        '
        for nome, cod in PALETA)

    return (
        '<!-- ====================== PERSONALIZADOR ====================== -->\n'
        '<section class="section wrap" id="personalizar">\n'
        '  <div class="section-head rv">\n'
        '    <span class="kicker">Do seu jeito</span>\n'
        '    <h2 class="h2">O seu não precisa<br>ser igual ao de ninguém.</h2>\n'
        '    <p class="lede">A cápsula sai do molde do seu ouvido. O faceplate é '
        'escolha sua — toque numa cor pra ver como fica.</p>\n'
        '  </div>\n\n'
        '  <div class="perso rv">\n'
        '    <div class="perso-palco">\n'
        '      <div class="perso-circulo">\n'
        f'        <img id="fonePerso" src="../assets/{foto(m["slug"])}" '
        f'alt="{e(m["nome"])}" width="1000" height="1000" loading="lazy"\n'
        f'             style="filter:{filtro(m["slug"])}">\n'
        '      </div>\n'
        f'      <p class="perso-legenda">{e(m["nome"])} · <span id="corNome">como no catálogo</span></p>\n'
        '    </div>\n'
        '    <div class="perso-cores">\n'
        f'        {botoes}'
        '<p class="tiny">Essas são as cores do catálogo. Madeira, fibra de carbono, '
        'glitter e a sua logomarca gravada também são possíveis — o especialista '
        'mostra tudo na conversa.</p>\n'
        f'      <a class="btn btn-primary" href="{zap}" target="_blank" rel="noopener">'
        'Montar o meu com um especialista</a>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n\n')
