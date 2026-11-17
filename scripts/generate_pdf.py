from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / 'dist' / 'carnet-francais.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu', FONT))
pdfmetrics.registerFont(TTFont('DejaVuBold', FONT_BOLD))

INK = HexColor('#17313B')
MUTED = HexColor('#587078')
PAPER = HexColor('#FFFDF8')
CARD = HexColor('#FFFFFF')
BORDER = HexColor('#DCE6E3')
MINT = HexColor('#BFE8D2')
MINT_DARK = HexColor('#2A8F67')
CORAL = HexColor('#F07C6A')
YELLOW = HexColor('#F6C85F')
BLUE = HexColor('#6FC2E8')
LAVENDER = HexColor('#C9B6FF')

W, H = A4


def line(c, x1, y1, x2, y2, color=INK, width=2):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)


def text(c, value, x, y, size=12, color=INK, bold=False):
    c.setFont('DejaVuBold' if bold else 'DejaVu', size)
    c.setFillColor(color)
    c.drawString(x, y, value)


def centered(c, value, x, y, size=12, color=INK, bold=False):
    c.setFont('DejaVuBold' if bold else 'DejaVu', size)
    c.setFillColor(color)
    c.drawCentredString(x, y, value)


def pill(c, label, x, y, fill, width=None):
    c.setFont('DejaVuBold', 9)
    width = width or stringWidth(label, 'DejaVuBold', 9) + 22
    c.setFillColor(fill)
    c.roundRect(x, y, width, 22, 11, stroke=0, fill=1)
    centered(c, label, x + width/2, y + 7, 9, white, True)
    return width


def rounded_card(c, x, y, w, h):
    c.setFillColor(CARD)
    c.setStrokeColor(BORDER)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 18, stroke=1, fill=1)



SKIN = HexColor('#D7A07B')
HAIR = HexColor('#3A2A2A')
DARK_BLUE = HexColor('#456D8B')
GROUND = HexColor('#D8E2DA')


def scene_base(c, x, y, sky=MINT):
    c.setFillColor(sky)
    c.roundRect(x, y, 165, 150, 24, stroke=0, fill=1)
    c.setFillColor(GROUND)
    c.roundRect(x + 1, y + 1, 163, 39, 22, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFillAlpha(0.45)
    c.circle(x + 133, y + 118, 20, stroke=0, fill=1)
    c.setFillAlpha(1)


def draw_human(c, cx, cy, outfit, woman=False, wave=False, child=False):
    """Editorial semi-realistic figure: natural proportions, clothing and expression."""
    s = 0.68 if child else 1.0
    # legs and shoes
    c.setStrokeColor(INK)
    c.setLineWidth(2.5 * s)
    line(c, cx - 7*s, cy + 34*s, cx - 10*s, cy - 8*s, DARK_BLUE, 3*s)
    line(c, cx + 7*s, cy + 34*s, cx + 12*s, cy - 8*s, DARK_BLUE, 3*s)
    line(c, cx - 16*s, cy - 9*s, cx - 5*s, cy - 9*s, HAIR, 3*s)
    line(c, cx + 7*s, cy - 9*s, cx + 18*s, cy - 9*s, HAIR, 3*s)
    # torso and neck
    c.setFillColor(outfit)
    c.roundRect(cx - 20*s, cy + 29*s, 40*s, 50*s, 10*s, stroke=0, fill=1)
    c.setFillColor(SKIN)
    c.roundRect(cx - 5*s, cy + 73*s, 10*s, 11*s, 3*s, stroke=0, fill=1)
    # arms + hands
    if wave:
        line(c, cx + 18*s, cy + 67*s, cx + 40*s, cy + 98*s, SKIN, 5*s)
        c.setFillColor(SKIN)
        c.circle(cx + 42*s, cy + 101*s, 5*s, stroke=0, fill=1)
        for dx in (-4, 0, 4):
            line(c, cx + (42+dx)*s, cy + 103*s, cx + (42+dx)*s, cy + 110*s, SKIN, 1.3*s)
    else:
        line(c, cx - 18*s, cy + 67*s, cx - 33*s, cy + 42*s, SKIN, 5*s)
        line(c, cx + 18*s, cy + 67*s, cx + 34*s, cy + 45*s, SKIN, 5*s)
        c.setFillColor(SKIN)
        c.circle(cx - 34*s, cy + 41*s, 4*s, stroke=0, fill=1)
        c.circle(cx + 35*s, cy + 44*s, 4*s, stroke=0, fill=1)
    # head, ears, nose
    c.setFillColor(SKIN)
    c.ellipse(cx - 17*s, cy + 80*s, cx + 17*s, cy + 119*s, stroke=0, fill=1)
    c.circle(cx - 18*s, cy + 99*s, 3*s, stroke=0, fill=1)
    c.circle(cx + 18*s, cy + 99*s, 3*s, stroke=0, fill=1)
    # hair gives adult identity and texture
    c.setFillColor(HAIR)
    if woman:
        c.ellipse(cx - 20*s, cy + 97*s, cx + 20*s, cy + 124*s, stroke=0, fill=1)
        c.roundRect(cx - 21*s, cy + 88*s, 7*s, 24*s, 4*s, stroke=0, fill=1)
        c.roundRect(cx + 14*s, cy + 88*s, 7*s, 24*s, 4*s, stroke=0, fill=1)
    else:
        c.ellipse(cx - 18*s, cy + 105*s, cx + 18*s, cy + 124*s, stroke=0, fill=1)
    # facial area over hair
    c.setFillColor(SKIN)
    c.ellipse(cx - 13*s, cy + 86*s, cx + 13*s, cy + 113*s, stroke=0, fill=1)
    c.setFillColor(INK)
    c.circle(cx - 5*s, cy + 103*s, 1.45*s, stroke=0, fill=1)
    c.circle(cx + 5*s, cy + 103*s, 1.45*s, stroke=0, fill=1)
    c.setStrokeColor(CORAL)
    c.setLineWidth(1.5*s)
    c.arc(cx - 6*s, cy + 91*s, cx + 6*s, cy + 101*s, 205, 130)


def draw_family_scene(c, x, y, aunt=True):
    scene_base(c, x, y)
    # interior window and plant establish an everyday family scene
    c.setFillColor(white)
    c.roundRect(x + 12, y + 84, 39, 40, 5, stroke=0, fill=1)
    line(c, x + 31, y + 86, x + 31, y + 122, BLUE, 1)
    line(c, x + 14, y + 104, x + 49, y + 104, BLUE, 1)
    c.setFillColor(MINT_DARK)
    c.circle(x + 143, y + 49, 8, stroke=0, fill=1)
    c.circle(x + 151, y + 56, 7, stroke=0, fill=1)
    c.setFillColor(CORAL)
    c.roundRect(x + 142, y + 34, 15, 12, 3, stroke=0, fill=1)
    if aunt:
        draw_human(c, x + 77, y + 17, CORAL, woman=True)
    else:
        draw_human(c, x + 77, y + 17, DARK_BLUE)
    draw_human(c, x + 121, y + 26, YELLOW, child=True)


def draw_tea(c, x, y):
    scene_base(c, x, y, HexColor('#DCEBE4'))
    # table, shadow, porcelain cup and realistic tea colour
    c.setFillColor(HexColor('#B07B56'))
    c.roundRect(x + 15, y + 31, 135, 13, 6, stroke=0, fill=1)
    c.setFillColor(HexColor('#A86F4D'))
    c.ellipse(x + 37, y + 43, x + 128, y + 59, stroke=0, fill=1)
    c.setFillColor(white)
    c.roundRect(x + 54, y + 61, 61, 48, 8, stroke=0, fill=1)
    c.setStrokeColor(INK)
    c.setLineWidth(2)
    c.arc(x + 105, y + 68, x + 137, y + 101, 285, 155)
    c.setFillColor(HexColor('#B97D37'))
    c.ellipse(x + 59, y + 98, x + 110, y + 106, stroke=0, fill=1)
    c.setFillColor(HexColor('#FFE8A9'))
    c.ellipse(x + 64, y + 100, x + 105, y + 104, stroke=0, fill=1)
    c.setStrokeColor(HexColor('#C9876A'))
    c.setLineWidth(1.9)
    c.bezier(x + 74, y + 110, x + 66, y + 125, x + 88, y + 132, x + 78, y + 144)
    c.bezier(x + 96, y + 110, x + 88, y + 125, x + 110, y + 132, x + 100, y + 144)


def draw_hello(c, x, y):
    scene_base(c, x, y, HexColor('#DCEBE4'))
    # café facade and a natural greeting gesture
    c.setFillColor(white)
    c.roundRect(x + 103, y + 49, 46, 67, 6, stroke=0, fill=1)
    c.setFillColor(CORAL)
    c.rect(x + 100, y + 111, 52, 9, stroke=0, fill=1)
    c.setFillColor(YELLOW)
    c.circle(x + 132, y + 128, 15, stroke=0, fill=1)
    for dx, dy in [(0,23),(18,14),(23,0),(18,-14),(-18,14),(-23,0)]:
        line(c, x + 132, y + 128, x + 132 + dx, y + 128 + dy, YELLOW, 1.4)
    draw_human(c, x + 63, y + 27, LAVENDER, woman=True, wave=True)


def entry(c, y, number, word, article, ipa, sentence, hint, kind):
    x, card_w, card_h = 42, W - 84, 310
    rounded_card(c, x, y, card_w, card_h)
    pill(c, f'{number:02d}', x + 26, y + card_h - 46, MINT_DARK, 36)
    text(c, article.upper(), x + 75, y + card_h - 38, 10, MUTED, True)
    text(c, word, x + 75, y + card_h - 78, 31, INK, True)
    text(c, 'Prononciation', x + 75, y + card_h - 105, 10, MUTED, True)
    text(c, ipa, x + 75, y + card_h - 127, 15, MINT_DARK, True)

    text(c, 'Une phrase', x + 75, y + card_h - 158, 10, MUTED, True)
    text(c, sentence, x + 75, y + card_h - 186, 15, INK)
    text(c, 'À retenir', x + 75, y + card_h - 218, 10, MUTED, True)
    text(c, hint, x + 75, y + card_h - 244, 13, INK)
    text(c, 'J’écris', x + 75, y + 52, 10, MUTED, True)
    line(c, x + 75, y + 32, x + 324, y + 32, BORDER, 1)
    line(c, x + 75, y + 14, x + 324, y + 14, BORDER, 1)
    ix, iy = x + card_w - 194, y + 88
    if kind == 'aunt':
        draw_family_scene(c, ix, iy, aunt=True)
    elif kind == 'uncle':
        draw_family_scene(c, ix, iy, aunt=False)
    elif kind == 'tea':
        draw_tea(c, ix, iy)
    else:
        draw_hello(c, ix, iy)


def page_header(c, n, title, subtitle):
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    text(c, 'MON CARNET DE FRANÇAIS', 42, H - 48, 11, MUTED, True)
    text(c, title, 42, H - 88, 24, INK, True)
    text(c, subtitle, 42, H - 112, 12, MUTED)
    line(c, 42, H - 128, W - 42, H - 128, BORDER, 1)
    text(c, f'{n:02d}', W - 67, 32, 10, MUTED, True)


c = canvas.Canvas(str(OUT), pagesize=A4)
c.setTitle('Mon carnet de français')
c.setAuthor('Juan Carlos · Chati')

# Cover
c.setFillColor(PAPER)
c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(MINT)
c.circle(W - 72, H - 72, 114, stroke=0, fill=1)
c.setFillColor(LAVENDER)
c.circle(66, 125, 86, stroke=0, fill=1)
text(c, 'MON', 52, H - 162, 22, MINT_DARK, True)
text(c, 'CARNET', 52, H - 219, 47, INK, True)
text(c, 'DE FRANÇAIS', 52, H - 272, 31, INK, True)
text(c, 'Des mots, des images, des phrases.', 54, H - 309, 15, MUTED)
pill(c, 'VOLUME 01', 54, H - 356, CORAL, 100)
# cover illustration
for xx, yy, col, femme in [(95, 245, CORAL, True), (183, 210, BLUE, False), (275, 245, YELLOW, False)]:
    draw_human(c, xx, yy, col, woman=femme, wave=(col == BLUE), child=(col == YELLOW))
draw_tea(c, 340, 130)
centered(c, 'Je regarde. Je comprends. Je retiens.', W/2, 65, 13, INK, True)
text(c, 'FRANÇAIS SEULEMENT', 52, 38, 10, MUTED, True)
c.showPage()

page_header(c, 1, 'LES MOTS DU JOUR', 'Je regarde l’image, je lis, puis j’écris.')
entry(c, 414, 1, 'tante', 'LA', '/tɑ̃t/', 'Voici ma tante.', 'la → féminin', 'aunt')
entry(c, 72, 2, 'oncle', 'L’', '/ɔ̃kl/', 'Voici mon oncle.', 'mon → masculin', 'uncle')
c.showPage()

page_header(c, 2, 'SALUER ET BOIRE', 'Des mots simples pour commencer une conversation.')
entry(c, 414, 3, 'thé', 'LE', '/te/', 'Le thé est chaud.', 'le → masculin', 'tea')
entry(c, 72, 4, 'Bonjour !', '', '/bɔ̃.ʒuʁ/', 'Bonjour, tante !', 'Je salue une personne.', 'hello')
c.showPage()

c.save()
print(OUT)
