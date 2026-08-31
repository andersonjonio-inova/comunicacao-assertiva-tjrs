from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium


BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent
FONT_DIR = Path('/data/.openclaw/workspace/skills/design/canvas-design/canvas-fonts')
LOGO = PROJECT / 'assets' / 'logo-cjud.jpg'

NAVY = HexColor('#0E2F66')
BLUE = HexColor('#17488F')
GREEN = HexColor('#76B82A')
ORANGE = HexColor('#F39A24')
YELLOW = HexColor('#FFD21D')
INK = HexColor('#15243A')
MUTED = HexColor('#617087')
LINE = HexColor('#DCE5EF')
WHITE = HexColor('#FFFFFF')
WASH = HexColor('#F4F8FC')


def register_fonts():
    pdfmetrics.registerFont(TTFont('Instrument', str(FONT_DIR / 'InstrumentSans-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('InstrumentBold', str(FONT_DIR / 'InstrumentSans-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('GeistMono', str(FONT_DIR / 'GeistMono-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('GeistMonoBold', str(FONT_DIR / 'GeistMono-Bold.ttf')))


def txt(c, value, x, y, size, color=INK, font='Instrument', align='left'):
    c.setFillColor(color)
    c.setFont(font, size)
    if align == 'right':
        c.drawRightString(x, y, value)
    elif align == 'center':
        c.drawCentredString(x, y, value)
    else:
        c.drawString(x, y, value)


def header(c, title, subtitle, accent):
    width, height = landscape(A4)
    c.setFillColor(WHITE)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, height-6, width*.47, 6, fill=1, stroke=0)
    c.setFillColor(GREEN); c.rect(width*.47, height-6, width*.26, 6, fill=1, stroke=0)
    c.setFillColor(ORANGE); c.rect(width*.73, height-6, width*.19, 6, fill=1, stroke=0)
    c.setFillColor(YELLOW); c.rect(width*.92, height-6, width*.08, 6, fill=1, stroke=0)
    if LOGO.exists():
        c.drawImage(ImageReader(str(LOGO)), 28, height-66, width=42, height=42, preserveAspectRatio=True, mask='auto')
    txt(c, 'TJRS · FORMAÇÃO DE GESTORES', 80, height-31, 7.5, BLUE, 'GeistMonoBold')
    txt(c, title, 80, height-53, 20, NAVY, 'InstrumentBold')
    txt(c, subtitle, 80, height-68, 8.7, MUTED)
    txt(c, 'COMUNICAÇÃO ASSERTIVA', width-28, height-34, 8.5, accent, 'GeistMonoBold', 'right')
    txt(c, 'Inteligência Emocional e Comunicação Não Violenta', width-28, height-50, 7.7, MUTED, 'Instrument', 'right')
    txt(c, 'Ânderson Porto · Fernando de Assis Alves', width-28, height-65, 7.7, INK, 'InstrumentBold', 'right')


def panel(c, x, y, w, h, title, words, accent, fill):
    c.setFillColor(fill); c.setStrokeColor(LINE); c.setLineWidth(.7)
    c.roundRect(x, y, w, h, 11, fill=1, stroke=1)
    c.setFillColor(accent); c.roundRect(x, y+h-29, w, 29, 11, fill=1, stroke=0)
    c.rect(x, y+h-29, w, 12, fill=1, stroke=0)
    txt(c, title.upper(), x+12, y+h-19, 8.2, WHITE, 'GeistMonoBold')
    inner_w = w-24
    cols = 2 if len(words) > 10 else 1
    rows = (len(words)+cols-1)//cols
    col_w = inner_w/cols
    line_h = min(15.2, (h-43)/max(rows, 1))
    for i, word in enumerate(words):
        col = i//rows
        row = i%rows
        tx = x+12+col*col_w
        ty = y+h-43-row*line_h
        c.setFillColor(accent); c.circle(tx+2.5, ty+2.4, 1.7, fill=1, stroke=0)
        txt(c, word, tx+9, ty, 8.35, INK)


def footer(c, note):
    width, _ = landscape(A4)
    txt(c, note, 28, 17, 7.2, MUTED)
    txt(c, 'Mapa de consulta, não diagnóstico ou lista fechada.', width-28, 17, 7.2, MUTED, 'InstrumentBold', 'right')


FEELINGS = [
    ('AFEIÇÃO E CONEXÃO', ['afetuoso', 'acolhido', 'amistoso', 'amoroso', 'compassivo', 'conectado', 'grato', 'terno']),
    ('ALEGRIA E SATISFAÇÃO', ['alegre', 'animado', 'contente', 'encantado', 'entusiasmado', 'esperançoso', 'feliz', 'inspirado', 'orgulhoso', 'satisfeito']),
    ('CALMA E ALÍVIO', ['aliviado', 'calmo', 'centrado', 'confortável', 'descansado', 'relaxado', 'seguro', 'sereno', 'tranquilo']),
    ('INTERESSE E ENERGIA', ['alerta', 'curioso', 'energizado', 'estimulado', 'interessado', 'motivado', 'surpreso', 'vibrante']),
    ('MEDO E INSEGURANÇA', ['alarmado', 'ansioso', 'apreensivo', 'assustado', 'inseguro', 'nervoso', 'preocupado', 'receoso', 'tenso', 'vulnerável']),
    ('RAIVA E FRUSTRAÇÃO', ['agitado', 'contrariado', 'exasperado', 'frustrado', 'furioso', 'impaciente', 'incomodado', 'indignado', 'irritado', 'ressentido']),
    ('TRISTEZA E DOR', ['abatido', 'decepcionado', 'desanimado', 'desolado', 'magoado', 'melancólico', 'saudoso', 'solitário', 'triste']),
    ('CANSAÇO E CONFUSÃO', ['cansado', 'confuso', 'desconcertado', 'esgotado', 'hesitante', 'perplexo', 'sobrecarregado', 'sonolento']),
]

NEEDS = [
    ('SUSTENTO E BEM-ESTAR', ['abrigo', 'água', 'alimentação', 'descanso', 'espaço', 'movimento', 'proteção', 'saúde', 'segurança física']),
    ('AUTONOMIA', ['escolha', 'independência', 'liberdade', 'participação', 'privacidade', 'ritmo próprio']),
    ('INTEGRIDADE', ['autenticidade', 'coerência', 'dignidade', 'honestidade', 'respeito próprio', 'expressão pessoal']),
    ('CONEXÃO', ['aceitação', 'afeto', 'apoio', 'consideração', 'empatia', 'pertencimento', 'proximidade', 'respeito', 'ser compreendido', 'ser ouvido']),
    ('COOPERAÇÃO E CONFIANÇA', ['colaboração', 'comunicação', 'confiança', 'equidade', 'inclusão', 'reciprocidade', 'transparência']),
    ('CLAREZA E ORDEM', ['clareza', 'estrutura', 'informação', 'organização', 'previsibilidade', 'simplicidade', 'estabilidade']),
    ('COMPETÊNCIA E CONTRIBUIÇÃO', ['aprendizado', 'contribuição', 'efetividade', 'progresso', 'qualidade', 'realização', 'reconhecimento']),
    ('SENTIDO E JUSTIÇA', ['esperança', 'inspiração', 'justiça', 'propósito', 'significado', 'transcendência']),
    ('RENOVAÇÃO E CELEBRAÇÃO', ['beleza', 'celebração', 'criatividade', 'diversão', 'espontaneidade', 'harmonia', 'lazer']),
]


def feelings_page(out):
    width, height = landscape(A4)
    c = canvas.Canvas(str(out), pagesize=(width, height))
    c.setTitle('Folha de sentimentos da CNV')
    c.setAuthor('Ânderson Porto e Fernando de Assis Alves')
    header(c, 'SENTIMENTOS', 'Palavras para nomear estados afetivos com mais precisão', ORANGE)
    margin, gap = 28, 10
    top, bottom = height-92, 54
    cols, rows = 4, 2
    w = (width-2*margin-(cols-1)*gap)/cols
    h = (top-bottom-gap)/rows
    accents = [ORANGE, GREEN, BLUE, HexColor('#8C67B3'), HexColor('#C64D5C'), HexColor('#D56B32'), HexColor('#6C7F9D'), HexColor('#667788')]
    fills = [HexColor('#FFF7EB'), HexColor('#F2F8E9'), HexColor('#EEF4FA'), HexColor('#F5F0FA'), HexColor('#FCEFF1'), HexColor('#FFF2EA'), HexColor('#F1F4F8'), HexColor('#F2F4F6')]
    for i, (title, words) in enumerate(FEELINGS):
        row, col = divmod(i, cols)
        x = margin+col*(w+gap); y = top-(row+1)*h-row*gap
        panel(c, x, y, w, h, title, words, accents[i], fills[i])
    footer(c, 'Na CNV, sentimentos são estados afetivos. “Ignorado”, “pressionado” e “desrespeitado” costumam incluir interpretações sobre o outro.')
    c.showPage(); c.save()


def needs_page(out):
    width, height = landscape(A4)
    c = canvas.Canvas(str(out), pagesize=(width, height))
    c.setTitle('Folha de necessidades da CNV')
    c.setAuthor('Ânderson Porto e Fernando de Assis Alves')
    header(c, 'NECESSIDADES', 'Qualidades e condições humanas amplas, distintas das estratégias', GREEN)
    margin, gap = 28, 9
    top, bottom = height-92, 54
    cols, rows = 3, 3
    w = (width-2*margin-(cols-1)*gap)/cols
    h = (top-bottom-2*gap)/rows
    accents = [GREEN, BLUE, NAVY, HexColor('#8C67B3'), HexColor('#3E8A7A'), HexColor('#5576A4'), ORANGE, HexColor('#C35F54'), HexColor('#8A7B35')]
    fills = [HexColor('#F2F8E9'), HexColor('#EEF4FA'), HexColor('#EDF1F7'), HexColor('#F5F0FA'), HexColor('#EDF7F4'), HexColor('#F0F4F9'), HexColor('#FFF7EB'), HexColor('#FBF0EE'), HexColor('#F8F5E9')]
    for i, (title, words) in enumerate(NEEDS):
        row, col = divmod(i, cols)
        x = margin+col*(w+gap); y = top-(row+1)*h-row*gap
        panel(c, x, y, w, h, title, words, accents[i], fills[i])
    footer(c, 'Teste útil: uma necessidade não depende de uma pessoa ou ação específica. “Entregar hoje” é estratégia; previsibilidade e segurança podem ser necessidades.')
    c.showPage(); c.save()


def render_png(pdf_path):
    doc = pdfium.PdfDocument(str(pdf_path)); page = doc[0]
    bitmap = page.render(scale=180/72)
    png = pdf_path.with_suffix('.png')
    bitmap.to_pil().save(png, 'PNG', optimize=True)
    page.close(); doc.close()
    return png


if __name__ == '__main__':
    register_fonts()
    BASE.mkdir(parents=True, exist_ok=True)
    outputs = [BASE/'Folha_de_Sentimentos_CNV_A4.pdf', BASE/'Folha_de_Necessidades_CNV_A4.pdf']
    feelings_page(outputs[0]); needs_page(outputs[1])
    for output in outputs:
        print(output)
        print(render_png(output))
