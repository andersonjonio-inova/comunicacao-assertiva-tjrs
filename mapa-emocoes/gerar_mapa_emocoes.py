from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import pypdfium2 as pdfium


BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent
OUT = BASE / "Mapa_das_Emocoes_Valencia_Ativacao_Interocepcao_A3.pdf"
PNG_OUT = BASE / "Mapa_das_Emocoes_Valencia_Ativacao_Interocepcao_A3.png"
FONT_DIR = Path("/data/.openclaw/workspace/skills/design/canvas-design/canvas-fonts")
LOGO = PROJECT / "assets" / "logo-cjud.jpg"

NAVY = HexColor("#0E2F66")
BLUE = HexColor("#17488F")
GREEN = HexColor("#76B82A")
ORANGE = HexColor("#F39A24")
YELLOW = HexColor("#FFD21D")
INK = HexColor("#15243A")
MUTED = HexColor("#617087")
LINE = HexColor("#DCE5EF")
WHITE = HexColor("#FFFFFF")
WASH = HexColor("#F4F8FC")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Instrument", str(FONT_DIR / "InstrumentSans-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("InstrumentBold", str(FONT_DIR / "InstrumentSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("GeistMono", str(FONT_DIR / "GeistMono-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("GeistMonoBold", str(FONT_DIR / "GeistMono-Bold.ttf")))


def round_rect(c, x, y, w, h, radius, fill, stroke=None, width=1):
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.setLineWidth(width)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)


def text(c, value, x, y, size, color=INK, font="Instrument", align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    if align == "center":
        c.drawCentredString(x, y, value)
    elif align == "right":
        c.drawRightString(x, y, value)
    else:
        c.drawString(x, y, value)


def wrap(c, value, x, y, max_width, size, leading, color=MUTED, font="Instrument"):
    words = value.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_emotion(c, px, py, label, fill, radius=14, label_dx=0, label_dy=-3):
    c.setFillColor(fill)
    c.setStrokeColor(Color(1, 1, 1, alpha=0.92))
    c.setLineWidth(1.4)
    c.circle(px, py, radius, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont("InstrumentBold", 8.4)
    c.drawCentredString(px + label_dx, py + label_dy, label)


def build():
    register_fonts()
    width, height = landscape(A3)
    c = canvas.Canvas(str(OUT), pagesize=(width, height))
    c.setTitle("Mapa das Emoções: valência, ativação e interocepção")
    c.setAuthor("Ânderson Porto e Fernando de Assis Alves")

    margin = 34
    header_h = 92
    footer_h = 48
    panel_w = 238
    gap = 20
    chart_x = margin
    chart_y = footer_h + 28
    chart_w = width - 2 * margin - panel_w - gap
    chart_h = height - header_h - footer_h - 48
    panel_x = chart_x + chart_w + gap

    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, height - 7, width * 0.45, 7, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(width * 0.45, height - 7, width * 0.28, 7, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(width * 0.73, height - 7, width * 0.19, 7, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(width * 0.92, height - 7, width * 0.08, 7, fill=1, stroke=0)

    if LOGO.exists():
        c.drawImage(str(LOGO), margin, height - 78, width=48, height=48, preserveAspectRatio=True, mask="auto")
    text(c, "TJRS · FORMAÇÃO DE GESTORES", margin + 60, height - 38, 8.5, BLUE, "GeistMonoBold")
    text(c, "MAPA DAS EMOÇÕES", margin + 60, height - 61, 21, NAVY, "InstrumentBold")
    text(c, "valência · ativação · interocepção", margin + 60, height - 78, 10.5, MUTED, "Instrument")
    text(c, "COMUNICAÇÃO ASSERTIVA", width - margin, height - 40, 10, BLUE, "GeistMonoBold", "right")
    text(c, "Inteligência Emocional e Comunicação Não Violenta", width - margin, height - 59, 9, MUTED, "Instrument", "right")
    text(c, "Ânderson Porto · Fernando de Assis Alves", width - margin, height - 76, 8.5, INK, "InstrumentBold", "right")

    # Quadrantes: campos cromáticos suaves, fronteiras permeáveis.
    half_w, half_h = chart_w / 2, chart_h / 2
    quadrants = [
        (chart_x, chart_y + half_h, half_w, half_h, HexColor("#FDEBEC")),
        (chart_x + half_w, chart_y + half_h, half_w, half_h, HexColor("#FFF2C9")),
        (chart_x, chart_y, half_w, half_h, HexColor("#EAF0F7")),
        (chart_x + half_w, chart_y, half_w, half_h, HexColor("#EAF5DE")),
    ]
    for x, y, w, h, fill in quadrants:
        c.setFillColor(fill)
        c.rect(x, y, w, h, fill=1, stroke=0)

    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    for i in range(1, 10):
        x = chart_x + chart_w * i / 10
        y = chart_y + chart_h * i / 10
        c.line(x, chart_y, x, chart_y + chart_h)
        c.line(chart_x, y, chart_x + chart_w, y)
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.6)
    c.line(chart_x + half_w, chart_y, chart_x + half_w, chart_y + chart_h)
    c.line(chart_x, chart_y + half_h, chart_x + chart_w, chart_y + half_h)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.2)
    c.rect(chart_x, chart_y, chart_w, chart_h, fill=0, stroke=1)

    text(c, "ALTA ATIVAÇÃO", chart_x + 8, chart_y + chart_h - 16, 8.5, NAVY, "GeistMonoBold")
    text(c, "BAIXA ATIVAÇÃO", chart_x + 8, chart_y + 8, 8.5, NAVY, "GeistMonoBold")
    text(c, "VALÊNCIA DESAGRADÁVEL", chart_x + 8, chart_y + half_h + 8, 8.2, BLUE, "GeistMonoBold")
    text(c, "VALÊNCIA AGRADÁVEL", chart_x + chart_w - 8, chart_y + half_h + 8, 8.2, BLUE, "GeistMonoBold", "right")

    def pos(v, a):
        return chart_x + (v + 1) * chart_w / 2, chart_y + (a + 1) * chart_h / 2

    emotions = [
        ("pânico", -.84, .89, "neg"), ("terror", -.68, .79, "neg"),
        ("fúria", -.88, .65, "neg"), ("raiva", -.64, .63, "neg"),
        ("ansiedade", -.49, .52, "neg"), ("indignação", -.34, .68, "neg"),
        ("nojo", -.70, .37, "neg"), ("irritação", -.29, .35, "neg"),
        ("tensão", -.12, .58, "neg"), ("vergonha", -.47, .18, "neg"),
        ("inveja", -.24, .13, "neg"), ("culpa", -.38, -.23, "neg_low"),
        ("solidão", -.78, -.34, "neg_low"), ("tristeza", -.61, -.49, "neg_low"),
        ("melancolia", -.78, -.66, "neg_low"), ("desânimo", -.49, -.72, "neg_low"),
        ("tédio", -.19, -.61, "neg_low"), ("exaustão", -.39, -.89, "neg_low"),
        ("impotência", -.68, -.84, "neg_low"),
        ("surpresa", .02, .87, "amb"), ("excitação", .77, .91, "pos"),
        ("entusiasmo", .45, .78, "pos"), ("alegria", .69, .67, "pos"),
        ("interesse", .24, .51, "pos"), ("esperança", .42, .38, "pos"),
        ("curiosidade", .12, .22, "pos"), ("orgulho", .70, .31, "pos"),
        ("gratidão", .43, -.10, "pos_low"), ("satisfação", .22, -.25, "pos_low"),
        ("alívio", .39, -.36, "pos_low"), ("afeto", .72, -.20, "pos_low"),
        ("contentamento", .61, -.48, "pos_low"), ("segurança", .79, -.61, "pos_low"),
        ("calma", .28, -.72, "pos_low"), ("serenidade", .60, -.82, "pos_low"),
        ("confusão", -.08, .08, "amb"), ("ambivalência", .02, -.05, "amb"),
    ]
    fills = {
        "neg": HexColor("#E55A67"), "neg_low": HexColor("#8FA6C2"),
        "pos": HexColor("#F4B62C"), "pos_low": HexColor("#8BC34A"),
        "amb": HexColor("#B8A4D9"),
    }
    for label, v, a, group in emotions:
        x, y = pos(v, a)
        radius = 13.5 if len(label) < 9 else 16
        draw_emotion(c, x, y, label, fills[group], radius=radius)

    # Painel interoceptivo: camada corporal transversal.
    round_rect(c, panel_x, chart_y, panel_w, chart_h, 18, WASH, LINE, .8)
    text(c, "INTEROCEPÇÃO", panel_x + 18, chart_y + chart_h - 28, 12, NAVY, "GeistMonoBold")
    text(c, "o corpo oferece pistas", panel_x + 18, chart_y + chart_h - 45, 9.5, BLUE, "InstrumentBold")
    y = chart_y + chart_h - 74
    blocks = [
        ("ALTA ATIVAÇÃO", ORANGE, ["coração acelerado", "respiração curta ou rápida", "calor, tensão, tremor", "energia para aproximar ou afastar"]),
        ("ATIVAÇÃO VARIÁVEL", BLUE, ["aperto ou expansão no peito", "nó na garganta", "desconforto abdominal", "atenção estreita ou dispersa"]),
        ("BAIXA ATIVAÇÃO", GREEN, ["peso e lentidão", "queda de energia", "respiração mais lenta", "retraimento ou imobilidade"]),
    ]
    for heading, color, items in blocks:
        c.setFillColor(color)
        c.circle(panel_x + 22, y + 2, 4.2, fill=1, stroke=0)
        text(c, heading, panel_x + 34, y - 2, 8.5, color, "GeistMonoBold")
        y -= 20
        for item in items:
            text(c, "•", panel_x + 22, y, 9, MUTED, "InstrumentBold")
            text(c, item, panel_x + 34, y, 8.5, INK, "Instrument")
            y -= 15
        y -= 9

    c.setStrokeColor(LINE)
    c.line(panel_x + 18, y + 4, panel_x + panel_w - 18, y + 4)
    y -= 18
    text(c, "INVESTIGUE EM CAMADAS", panel_x + 18, y, 8.5, NAVY, "GeistMonoBold")
    y -= 20
    for index, item in enumerate(("1  notar o corpo", "2  localizar valência e ativação", "3  testar palavras emocionais", "4  considerar contexto e pensamento", "5  escolher a resposta")):
        text(c, item, panel_x + 18, y, 8.5, INK, "InstrumentBold" if index == 4 else "Instrument")
        y -= 17

    round_rect(c, panel_x + 14, chart_y + 15, panel_w - 28, 61, 10, HexColor("#FFF8ED"), HexColor("#F7D7A7"), .8)
    text(c, "LEITURA RESPONSÁVEL", panel_x + 26, chart_y + 57, 8, ORANGE, "GeistMonoBold")
    wrap(c, "A posição das emoções é aproximada. Um sinal corporal isolado não identifica uma emoção.", panel_x + 26, chart_y + 43, panel_w - 52, 7.8, 10, MUTED)

    text(c, "DESAGRADÁVEL", chart_x, chart_y - 18, 8.5, MUTED, "GeistMonoBold")
    text(c, "AGRADÁVEL", chart_x + chart_w, chart_y - 18, 8.5, MUTED, "GeistMonoBold", "right")
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.line(chart_x + 85, chart_y - 15, chart_x + chart_w - 74, chart_y - 15)
    c.setFillColor(BLUE)
    c.line(chart_x + chart_w - 74, chart_y - 15, chart_x + chart_w - 82, chart_y - 11)
    c.line(chart_x + chart_w - 74, chart_y - 15, chart_x + chart_w - 82, chart_y - 19)

    text(c, "Mapa didático dimensional. Emoções podem coexistir e mudar de posição conforme pessoa, intensidade e contexto.", margin, 18, 7.8, MUTED, "Instrument")
    text(c, "Base conceitual: teorias dimensionais das emoções + interocepção como fonte de pistas corporais.", width - margin, 18, 7.8, MUTED, "Instrument", "right")
    c.showPage()
    c.save()
    pdf = pdfium.PdfDocument(str(OUT))
    page = pdf[0]
    bitmap = page.render(scale=200 / 72)
    bitmap.to_pil().save(PNG_OUT, "PNG", optimize=True)
    page.close()
    pdf.close()
    print(OUT)
    print(PNG_OUT)


if __name__ == "__main__":
    build()
