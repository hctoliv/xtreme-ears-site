"""
Dados do site. Os textos e specs de cada fone vêm de gerar-paginas.py (catálogo oficial);
aqui entram só o que o 3D precisa e os fatos da empresa levantados em 06/11/2026.

Fontes dos fatos (não invente nada aqui):
- xtremeears.com.br: /pages/fale-conosco, /pages/perguntas-frequentes, /pages/como-comprar-1,
  /pages/manutencao-e-garantia, /pages/por-que-os-pre-moldes-do-seu-ouvido-sao-importantes,
  /pages/artistas, /policies/refund-policy, /policies/shipping-policy
- Canaltech, 29/01/2020: especial Xtreme Ears (André Goldstein, XE2/PRO em 2010)
"""
import importlib.util
import os

_aqui = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("catalogo", os.path.join(_aqui, "gerar-paginas.py"))
catalogo = importlib.util.module_from_spec(_spec)
import sys
sys.path.insert(0, _aqui)
_spec.loader.exec_module(catalogo)

MODELOS = catalogo.MODELOS
CAIXA_MOLDADO = catalogo.CAIXA_MOLDADO
REEL_POR_AREA = catalogo.REEL_POR_AREA

WHATS = "5511950295494"
TELEFONE = "(11) 3256-2692"
EMAIL = "contato@xtremeears.com.br"
ENDERECO = "Rua Dom José de Barros, 152, conj. 95/96, Centro, São Paulo/SP"
HORARIO = "Segunda a sexta, das 9h às 17h"
INSTAGRAM = "https://www.instagram.com/xtremeears/"
YOUTUBE = "https://www.youtube.com/user/XtremeEars"
LOJA = "https://www.xtremeears.com.br"

# Drivers por faixa, como o 3D desenha. Sai da "Configuração dos drivers" do catálogo:
# "driver duplo" = 2 drivers. "nd" = drivers cuja faixa a marca não divulga (XE14).
BANDAS = {
    "one-plus-pro": ({"bass": 1, "mid": 1, "high": 1}, 3),
    "onemax-pro":   ({"bass": 2, "mid": 1, "high": 1}, 3),
    "xe3-pro":      ({"bass": 2, "high": 1}, 2),
    "xe4-pro":      ({"bass": 2, "mid": 1, "high": 1}, 3),
    "xe5-pro":      ({"bass": 2, "mid": 2, "high": 1}, 3),
    "xe6-pro":      ({"bass": 2, "mid": 2, "high": 2}, 3),
    "xe8-pro":      ({"bass": 4, "mid": 2, "high": 2}, 3),
    "xe12-pro":     ({"sub": 4, "bass": 4, "mid": 2, "high": 2}, 4),
    "xe14-pro":     ({"nd": 7, "mid": 6, "high": 1}, 4),
}

NOTA_BANDAS = {
    "xe3-pro": "No XE3 os dois drivers de baixo cuidam juntos de grave e médio: o crossover é de duas vias.",
    "xe12-pro": "Dos oito drivers de baixo, quatro são só de subgrave. Por isso o crossover é de quatro vias.",
    "xe14-pro": "A Xtreme Ears publica os seis médios do HexaDrive Array™ e o driver E50D de agudo. "
                "A divisão dos outros sete não é divulgada, e no 3D eles aparecem em cinza.",
}

# visual de cada fone no 3D e nos cards. Faceplate e casco são escolha do cliente:
# isso aqui é só a combinação de vitrine.
VISUAL = {
    "one-plus-pro": ("transparente", "glitter", "azul", "prata"),
    "onemax-pro":   ("preto-translucido", "perola", "roxo", "prata"),
    "xe3-pro":      ("preto", "carbono", "preto", "prata"),
    "xe4-pro":      ("vermelho", "glitter", "vermelho", "prata"),
    "xe5-pro":      ("azul", "solido", "azul", "prata"),
    "xe6-pro":      ("verde", "glitter", "verde", "prata"),
    "xe8-pro":      ("transparente", "perola", "dourado", "ouro"),
    "xe12-pro":     ("preto-translucido", "glitter", "vermelho", "prata"),
    "xe14-pro":     ("preto", "glitter", "dourado", "ouro"),
}

# quem usa qual modelo: só o que a marca declara publicamente (banners da home e produtos signature)
ARTISTAS_POR_MODELO = {
    "xe4-pro": [("Lauana Prado", "lauana-prado.jpg")],
    "xe12-pro": [("Marcelo Falcão", "marcelo-falcao.jpg")],
    "xe14-pro": [("Felipe Amorim", None)],
    "xe3-pro": [("Aquiles Priester", "aquiles-priester.jpg")],
    "xtreme-stage": [("Aquiles Priester", "aquiles-priester.jpg")],
    "xtreme-one-plus": [("Aquiles Priester", "aquiles-priester.jpg")],
}

AREAS = {
    "grave": ("Grave", "Pra quem segura o tempo", "Bateria, baixo, percussão, DJ"),
    "medio": ("Médio", "Pra quem canta e faz a melodia", "Voz, guitarra, teclado"),
    "agudo": ("Agudo e detalhe", "Pra quem precisa ouvir tudo", "Técnico de som, produtor, audiófilo"),
    "universal": ("Universal", "Sem pré-molde, sai em até 2 dias úteis", "Primeiro in-ear, reserva"),
}

FAQ = [
    ("Por que não dá pra comprar direto no carrinho?",
     "Dá, mas o moldado só começa a ser feito depois do pré-molde do seu ouvido. Falar antes com o "
     "especialista evita escolher o modelo errado pro que você toca e já sai com a indicação de onde fazer o molde."),
    ("Quanto tempo leva?",
     "Cerca de 4 semanas depois que o pré-molde aprovado chega na Xtreme Ears. Se tiver faceplate com arte, "
     "o prazo conta a partir da arte aprovada também. Universais e acessórios saem em até 2 dias úteis."),
    ("E se o fone não encaixar direito?",
     "As conchas de acrílico têm 60 dias pra ajuste do molde, o que pode incluir refazer a concha. "
     "O fone tem 1 ano de garantia contra defeito de fabricação e entupimento."),
    ("Posso devolver um moldado?",
     "Não, porque ele é feito pro seu ouvido e não serve em mais ninguém. Dá pra trocar por outro modelo "
     "pagando a diferença. Universais podem ser trocados em até 7 dias, sem uso e na embalagem original."),
    ("Mais drivers é sempre melhor?",
     "Não. Mais drivers dão mais resolução e separação, mas o certo é o que combina com o seu instrumento. "
     "Baterista costuma render mais com punch no grave do que com 12 drivers. É isso que a conversa resolve."),
    ("Dá pra ouvir o ambiente e a plateia?",
     "Existe a opção Ambient: ventilação com 4 plugues que deixam entrar o som de fora e 1 plugue fechado que "
     "devolve o isolamento total. O preço é um pouco de grave a menos com a ventilação aberta."),
    ("Posso colocar a minha logo?",
     "Pode. A logo vai gravada no faceplate. Precisa de arquivo vetorial (CorelDraw ou Illustrator). "
     "Também tem madeira, aço escovado, fibra de carbono, cristais e glitter, em mais de 20 cores."),
    ("O frete é grátis?",
     "A Xtreme Ears anuncia frete grátis e entrega em todo o Brasil. Na garantia, se o defeito for avisado em "
     "até 7 dias da entrega, ela paga ida e volta."),
]
