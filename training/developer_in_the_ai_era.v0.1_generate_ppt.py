# -*- coding: utf-8 -*-
"""
AI 시대의 소프트웨어 개발자의 새로운 역할 - PPT 생성 스크립트
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── 색상 팔레트 ──
NAVY_DARK  = RGBColor(0x0F, 0x17, 0x2A)   # #0f172a
NAVY_MID   = RGBColor(0x1E, 0x3A, 0x5F)   # #1e3a5f
BLUE       = RGBColor(0x25, 0x63, 0xEB)    # #2563eb
SKY        = RGBColor(0x38, 0xBD, 0xF8)    # #38bdf8
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF1, 0xF5, 0xF9)
SLATE      = RGBColor(0x64, 0x74, 0x8B)
DARK_TEXT  = RGBColor(0x1E, 0x29, 0x3B)
RED        = RGBColor(0xDC, 0x26, 0x26)
GREEN      = RGBColor(0x05, 0x96, 0x69)
AMBER      = RGBColor(0xF5, 0x9E, 0x0B)
GREEN_BG   = RGBColor(0xEC, 0xFD, 0xF5)
AMBER_BG   = RGBColor(0xFF, 0xFB, 0xEB)
TABLE_HDR  = RGBColor(0x1E, 0x3A, 0x5F)
TABLE_BODY = RGBColor(0xFA, 0xFB, 0xFC)
TABLE_ALT  = RGBColor(0xF1, 0xF5, 0xF9)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

# ── Helper Functions ──

def add_gradient_bg(slide, c1, c2):
    """Add a gradient background to a slide"""
    bg = slide.background
    fill = bg.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = c1
    fill.gradient_stops[0].position = 0.0
    fill.gradient_stops[1].color.rgb = c2
    fill.gradient_stops[1].position = 1.0

def add_solid_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height, text, font_size=18,
                color=DARK_TEXT, bold=False, alignment=PP_ALIGN.LEFT,
                font_name='맑은 고딕', anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf.paragraphs[0].alignment = alignment
    except:
        pass
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    return txBox

def add_rich_textbox(slide, left, top, width, height, runs_data,
                     alignment=PP_ALIGN.LEFT, line_spacing=1.3):
    """Add textbox with multiple styled runs.
    runs_data = list of (text, font_size, color, bold, font_name)
    Use \\n in text for new paragraphs.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None

    first_para = True
    for text, font_size, color, bold, font_name in runs_data:
        parts = text.split('\n')
        for i, part in enumerate(parts):
            if first_para:
                p = tf.paragraphs[0]
                first_para = False
            elif i > 0 or text.startswith('\n'):
                p = tf.add_paragraph()
            else:
                p = tf.paragraphs[-1]
            p.alignment = alignment
            p.space_after = Pt(4)
            run = p.add_run()
            run.text = part
            run.font.size = Pt(font_size)
            run.font.color.rgb = color
            run.font.bold = bold
            run.font.name = font_name or '맑은 고딕'
    return txBox

def add_table(slide, left, top, width, height, rows, cols, data,
              header_color=TABLE_HDR, body_color=TABLE_BODY, 
              alt_color=TABLE_ALT, font_size=13, header_font_size=14):
    """Add a styled table. data = list of lists including header row."""
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    for col_idx in range(cols):
        for row_idx in range(rows):
            cell = table.cell(row_idx, col_idx)
            if row_idx < len(data) and col_idx < len(data[row_idx]):
                cell.text = str(data[row_idx][col_idx])
            
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.name = '맑은 고딕'
                if row_idx == 0:
                    paragraph.font.size = Pt(header_font_size)
                    paragraph.font.color.rgb = WHITE
                    paragraph.font.bold = True
                else:
                    paragraph.font.size = Pt(font_size)
                    paragraph.font.color.rgb = DARK_TEXT
            
            fill = cell.fill
            fill.solid()
            if row_idx == 0:
                fill.fore_color.rgb = header_color
            elif row_idx % 2 == 0:
                fill.fore_color.rgb = alt_color
            else:
                fill.fore_color.rgb = body_color
    return table_shape

def add_accent_line(slide, left, top, width, color=BLUE):
    """Add a thin accent line/rectangle"""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, Pt(4)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_quote_box(slide, left, top, width, height, text, font_size=16):
    """Add a styled quote box with left border"""
    # Background rect
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    rect.fill.solid()
    rect.fill.fore_color.rgb = RGBColor(0xF8, 0xFA, 0xFC)
    rect.line.fill.background()
    # Left border
    border = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, Pt(4), height
    )
    border.fill.solid()
    border.fill.fore_color.rgb = BLUE
    border.line.fill.background()
    # Text
    tb = add_textbox(slide, left + Inches(0.3), top + Inches(0.1),
                     width - Inches(0.4), height - Inches(0.2),
                     text, font_size=font_size, color=SLATE)
    return tb

def make_chapter_slide(title, subtitle, note=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    add_gradient_bg(slide, NAVY_DARK, NAVY_MID)
    add_textbox(slide, Inches(0), Inches(2.2), W, Inches(1.2),
                title, font_size=52, color=SKY, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(0), Inches(3.5), W, Inches(0.8),
                subtitle, font_size=28, color=WHITE, bold=False,
                alignment=PP_ALIGN.CENTER)
    if note:
        add_textbox(slide, Inches(0), Inches(4.5), W, Inches(0.5),
                    note, font_size=18, color=SLATE, bold=False,
                    alignment=PP_ALIGN.CENTER)
    return slide

def make_content_slide(title, emoji=""):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_solid_bg(slide, RGBColor(0xFA, 0xFB, 0xFC))
    display_title = f"{emoji} {title}" if emoji else title
    add_textbox(slide, Inches(0.7), Inches(0.3), Inches(11), Inches(0.7),
                display_title, font_size=30, color=NAVY_DARK, bold=True)
    add_accent_line(slide, Inches(0.7), Inches(1.0), Inches(2), BLUE)
    return slide


# ═══════════════════════════════════════════════════════════
# SLIDE 1: Title
# ═══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient_bg(slide, NAVY_DARK, BLUE)
add_textbox(slide, Inches(0), Inches(1.5), W, Inches(1),
            "AI 시대의", font_size=44, color=SKY, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(2.3), W, Inches(1),
            "소프트웨어 개발자의", font_size=44, color=SKY, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(3.1), W, Inches(1),
            "새로운 역할", font_size=44, color=SKY, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(4.5), W, Inches(0.6),
            "고등학생을 위한 AI 특강", font_size=26, color=SLATE,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(5.3), W, Inches(0.5),
            "2026년 5월", font_size=20, color=RGBColor(0xCB, 0xD5, 0xE1),
            alignment=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════
# SLIDE 2: TOC
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("강의 순서 (90분)")
add_table(slide,
    Inches(1.5), Inches(1.4), Inches(10), Inches(4.5),
    rows=8, cols=3,
    data=[
        ["시간", "파트", "내용"],
        ["00–05", "인사", "강사 소개"],
        ["05–20", "1부", "문제 제기 — AI가 개발자를 대체하나?"],
        ["20–45", "2부", "현상 분석 — 데이터로 보는 진실"],
        ["45–55", "휴식", "쉬는 시간"],
        ["55–75", "3부", "사례 — AI가 잘 못하는 영역"],
        ["75–85", "4부", "업무 변화와 미래 전망"],
        ["85–90", "Q&A", "질의응답"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 3: Instructor
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("강사 소개")
add_quote_box(slide, Inches(1), Inches(1.5), Inches(5), Inches(1),
              "건국대학교 컴퓨터공학과 공학박사", font_size=20)
add_quote_box(slide, Inches(1), Inches(2.8), Inches(5), Inches(1),
              "2012년 ~ 현재 · LG전자 CTO Software Platform Lab", font_size=20)
add_table(slide,
    Inches(7), Inches(1.5), Inches(5), Inches(3),
    rows=5, cols=2,
    data=[
        ["프로젝트", "역할"],
        ["webOS Platform", "개발"],
        ["webOS SDK", "개발"],
        ["LUPA Platform", "개발"],
        ["LUPA SDK", "개발"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 4: Chapter 1
# ═══════════════════════════════════════════════════════════
make_chapter_slide("1부", "AI가 개발자를 대체하는가?", "문제 제기")

# ═══════════════════════════════════════════════════════════
# SLIDE 5: Big Tech CEOs
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("빅테크 CEO들의 선언 (2025)")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(3.6),
    rows=6, cols=4,
    data=[
        ["기업", "누가", "무슨 말을?", "시기"],
        ["Google", "CEO Sundar Pichai", "신규 코드의 25~30% 이상이 AI 작성", "01월"],
        ["Meta", "CEO Zuckerberg", "AI가 중간급 엔지니어 대체할 것", "01월"],
        ["Shopify", "CEO Tobi Lütke", "AI가 못하는 걸 증명해야 채용 가능", "04월"],
        ["Anthropic", "CEO Dario Amodei", "기업 3/4이 AI에 전체 업무 위임", "09월"],
        ["Gartner", "리서치 보고서", "2030년까지 개발자 3명 중 1명 실직 전망", "09월"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.2), Inches(11.5), Inches(0.9),
              "Amazon은 2025~2026년 사이 AI·자동화를 이유로 약 30,000명 감원", font_size=18)

# ═══════════════════════════════════════════════════════════
# SLIDE 7: Vibe Coding
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("바이브 코딩(Vibe Coding)의 등장")
add_quote_box(slide, Inches(0.7), Inches(1.4), Inches(11.5), Inches(1),
              'OpenAI 공동창립자 Andrej Karpathy가 2025년 2월 제안\n"코드를 읽지 않고, 자연어로 지시만 하면 AI가 코드를 생성"',
              font_size=16)
add_table(slide,
    Inches(0.7), Inches(2.8), Inches(11.5), Inches(3.2),
    rows=5, cols=2,
    data=[
        ["지표", "내용"],
        ["Collins Dictionary", "2025 올해의 단어 선정"],
        ["Y Combinator", "2025 Winter 스타트업 25%가 코드의 95%를 AI로 생성"],
        ["Cursor (Anysphere)", "기업가치 $293억 → xAI $600억 인수 논의 (2026.04)"],
        ["OpenAI", "바이브 코딩 스타트업 Windsurf $30억 인수 (2025.05)"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 8: Vibe Coding Dark Side
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("바이브 코딩의 어두운 면")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(3.8),
    rows=6, cols=3,
    data=[
        ["사건", "내용", "시기"],
        ["Replit DB 삭제", "AI 에이전트가 프로덕션 DB 삭제 후 거짓 보고", "2025.07"],
        ["METR 연구", "AI 사용 시 오히려 19% 느려짐 (본인은 빨라졌다고 착각)", "2025.07"],
        ["GitClear", "코드 리팩토링 25%→10% 미만, 코드 중복 4배 증가", "2025"],
        ["바이브 코딩 숙취", '"개발 지옥" — 시니어 엔지니어들의 고통', "2025.09"],
        ["오픈소스 위협", "LLM이 대형 라이브러리에만 편향 → 신규 도구 발견 감소", "2026.01"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.5), Inches(11.5), Inches(0.8),
              "Linus Torvalds: 바이브 코딩 사용하지만, 핵심 커널 코드가 아닌 부수적 도구에만 활용 (2026.01)",
              font_size=15)

# ═══════════════════════════════════════════════════════════
# SLIDE 9: AI Slop
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("AI 슬롭(AI Slop) — 저품질 콘텐츠의 범람")
add_quote_box(slide, Inches(0.7), Inches(1.4), Inches(11.5), Inches(0.8),
              '"Slop" = Merriam-Webster & 미국 방언학회 2025 올해의 단어 동시 선정',
              font_size=18)
add_table(slide,
    Inches(0.7), Inches(2.6), Inches(11.5), Inches(3.2),
    rows=5, cols=3,
    data=[
        ["플랫폼", "문제", "시기"],
        ["Steam", '출시 게임의 20%가 AI 공시 포함 — "AI 쇼블웨어"', "2025.07"],
        ["Google Play", "Angry Birds AI 이미지 비판 → 삭제", "2025"],
        ["Lovable", "1,645개 앱 중 170개에서 개인정보 노출", "2025.05"],
        ["한국", "AI 슬롭 콘텐츠 소비 세계 1위", "2025.12"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 10: Key Question (Alert)
# ═══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, AMBER_BG)
# Left accent
border = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, 0, 0, Pt(8), H
)
border.fill.solid()
border.fill.fore_color.rgb = AMBER
border.line.fill.background()
add_textbox(slide, Inches(0), Inches(1.5), W, Inches(0.8),
            "핵심 질문", font_size=28, color=RGBColor(0x92, 0x40, 0x0E),
            bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(2.8), W, Inches(1.2),
            "앞으로 SW 개발자의 수가 줄어들고\n일자리도 없어지지 않을까?",
            font_size=40, color=NAVY_DARK, bold=True, alignment=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════
# SLIDE 11: Chapter 2
# ═══════════════════════════════════════════════════════════
make_chapter_slide("2부", "데이터로 보는 진실", "현상 분석")

# ═══════════════════════════════════════════════════════════
# SLIDE 12: US Employment
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("미국 SW 개발자 고용 현황")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(11), Inches(0.5),
            "미국 노동통계국 (BLS, 2024년 기준)", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(1.5), Inches(1.9), Inches(10), Inches(3.5),
    rows=6, cols=2,
    data=[
        ["지표", "수치"],
        ["총 종사자 수", "1,895,500명"],
        ["중위 연봉", "$133,080 / 년"],
        ["고용 전망 (2024–2034)", "+15% 성장"],
        ["10년 신규 고용", "+287,900명"],
        ["연간 채용 예상", "~129,200건 / 년"],
    ])
add_quote_box(slide, Inches(1.5), Inches(5.7), Inches(10), Inches(0.7),
              "전체 직종 평균 대비 훨씬 빠른 성장 전망", font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 13: Global Developers
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("전 세계 SW 개발자 규모")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(11), Inches(0.5),
            "GitHub Octoverse 2025 (2025.10 발표)", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(1.5), Inches(1.9), Inches(10), Inches(3.5),
    rows=6, cols=3,
    data=[
        ["지표", "수치", "변화"],
        ["GitHub 전체 개발자", "1.5억 명 이상", "—"],
        ["2025년 신규 가입", "3,600만 명", "매 초 1명!"],
        ["AI 관련 저장소", "430만 개", "2년 새 2배"],
        ["LLM SDK 사용 저장소", "113만 개", "+178% YoY"],
        ["신규 개발자 Copilot 사용", "~80%", "첫 주 내"],
    ])
add_quote_box(slide, Inches(1.5), Inches(5.7), Inches(10), Inches(0.7),
              "개발자 수는 감소하지 않고 오히려 폭증 중", font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 14: Korea Developers
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("한국 SW 개발자 현황")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(5), Inches(0.5),
            "국내 ICT 인력 (ITSTAT, 2024 잠정치)", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(5.5), Inches(2.8),
    rows=5, cols=2,
    data=[
        ["지표", "수치"],
        ["ICT 산업 전체 인력", "220만 811명"],
        ["SW 산업 종사자 (추정)", "약 100만 명 이상"],
        ["연평균 성장률", "4~5% (최근 5년)"],
        ["GitHub 기여자 순위", "7위 (기여량 6위)"],
    ])
# Right side: bullet points
add_textbox(slide, Inches(7), Inches(1.9), Inches(5.5), Inches(0.5),
            "주요 특징", font_size=20, color=NAVY_MID, bold=True)
bullets = [
    "• 삼성·LG·카카오·네이버 등 대기업 중심 SW 인력 집중",
    "• AI·클라우드·임베디드 분야 신규 수요 지속 증가",
    "• 2025년 이후 AI 관련 채용 공고 전년 대비 급증세",
]
add_textbox(slide, Inches(7), Inches(2.6), Inches(5.5), Inches(2.5),
            '\n'.join(bullets), font_size=16, color=DARK_TEXT)

# ═══════════════════════════════════════════════════════════
# SLIDE 15: AI Coding Languages
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("AI 코딩에서 많이 쓰는 언어")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(5), Inches(0.5),
            "GitHub Octoverse 2025", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(5.5), Inches(2.4),
    rows=4, cols=4,
    data=[
        ["순위", "언어", "성장률 (YoY)", "특징"],
        ["1위", "TypeScript", "+66%", "AI 타입 안전성"],
        ["2위", "Python", "+48%", "AI/ML 표준 언어"],
        ["3위", "JavaScript", "+24%", "TS로 전환 가속"],
    ])
add_textbox(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(0.5),
            "AI 관련 저장소 언어별", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(7), Inches(1.9), Inches(5.5), Inches(2.4),
    rows=4, cols=3,
    data=[
        ["언어", "저장소 수", "증가율"],
        ["Python", "582,000개", "+50.7%"],
        ["TypeScript", "86,000개", "+77.9%"],
        ["JavaScript", "88,000개", "+24.8%"],
    ])

# Visual bar chart for language growth
for i, (lang, pct, w, clr) in enumerate([
    ("TypeScript +66%", 66, 6.6, RGBColor(0x31, 0x78, 0xC6)),
    ("Python +48%", 48, 4.8, RGBColor(0x30, 0x6D, 0x98)),
    ("JavaScript +24%", 24, 2.4, RGBColor(0xF0, 0xDB, 0x4F)),
]):
    y = 4.7 + i * 0.7
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(2), Inches(y), Inches(w), Inches(0.5))
    bar.fill.solid()
    bar.fill.fore_color.rgb = clr
    bar.line.fill.background()
    add_textbox(slide, Inches(2.1), Inches(y + 0.05), Inches(4), Inches(0.4),
                lang, font_size=13, color=WHITE, bold=True)

# ═══════════════════════════════════════════════════════════
# SLIDE 16: AI Productivity
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("AI가 높이는 개발자 생산성")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(5.5), Inches(0.5),
            "GitHub Copilot × Accenture 연구 (2024)", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(5.5), Inches(3.5),
    rows=6, cols=2,
    data=[
        ["지표", "변화"],
        ["Pull Request 수", "+8.69%"],
        ["PR 병합률 (코드 품질)", "+15%"],
        ["빌드 성공률", "+84%"],
        ["업무 만족도 향상", "90% 응답"],
        ["코딩이 즐거워짐", "95% 응답"],
    ])
add_textbox(slide, Inches(7), Inches(1.9), Inches(5.5), Inches(0.5),
            "GitHub 개발자 설문 (2024)", font_size=18, color=SLATE, bold=True)
bullets = [
    "• 97% 이상이 AI 코딩 도구 사용 경험",
    "",
    "• 절약된 시간 → 설계·협업·학습에 재투자",
    "",
    "• 90% 코드 품질 향상 체감 (미국 응답자)",
    "",
    "• 60~71%가 새 언어 습득 용이해짐",
]
add_textbox(slide, Inches(7), Inches(2.6), Inches(5.5), Inches(3),
            '\n'.join(bullets), font_size=16, color=DARK_TEXT)

# ═══════════════════════════════════════════════════════════
# SLIDE 17: Part 2 Summary (Insight)
# ═══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, GREEN_BG)
border = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Pt(8), H)
border.fill.solid()
border.fill.fore_color.rgb = GREEN
border.line.fill.background()
add_textbox(slide, Inches(0), Inches(0.5), W, Inches(0.7),
            "2부 핵심 정리", font_size=30, color=RGBColor(0x06, 0x5F, 0x46),
            bold=True, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(1.5), Inches(1.5), Inches(5), Inches(0.5),
            "일자리가 사라지는가?", font_size=24, color=NAVY_DARK, bold=True)
add_quote_box(slide, Inches(1.5), Inches(2.1), Inches(5), Inches(1.5),
              "미국 BLS: 2034년까지 +15% 성장 전망\nGitHub: 매 초 1명씩 신규 개발자 가입",
              font_size=18)
add_textbox(slide, Inches(7), Inches(1.5), Inches(5), Inches(0.5),
            "AI가 바꾸는 것은?", font_size=24, color=NAVY_DARK, bold=True)
add_quote_box(slide, Inches(7), Inches(2.1), Inches(5), Inches(1.5),
              "단순 코딩 → AI 도구 활용 + 전문적 설계·검증 중심\n새 시장: AI 에이전트 · LLM 인프라 · Edge AI · SDV",
              font_size=18)

# ═══════════════════════════════════════════════════════════
# SLIDE 18: Chapter 3
# ═══════════════════════════════════════════════════════════
make_chapter_slide("3부", "AI가 잘 못하는 영역", "사례 제시")

# ═══════════════════════════════════════════════════════════
# SLIDE 19: Embedded SW - AI Limits
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("임베디드 소프트웨어 — AI의 한계")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(11), Inches(0.5),
            "LG전자 임베디드 개발 현장의 이야기", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(11.5), Inches(3.5),
    rows=6, cols=2,
    data=[
        ["한계 요인", "설명"],
        ["비공개 코드", "외부에 없는 사내 코드 → AI 학습 불가"],
        ["하드웨어 의존", "물리적 개입 없이 테스트 불가"],
        ["할루시네이션", "존재하지 않는 API를 생성"],
        ["실시간성", "타이밍이 중요한 RTOS 환경"],
        ["안전 규격", "AUTOSAR, DO-178C 등 인증 부담"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.7), Inches(11.5), Inches(0.8),
              '"우리가 AI의 인간 하네스(harness)가 될 수도 있다" — 현장 개발자',
              font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 20: Embedded × AI
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("하지만 임베디드 × AI는 가장 뜨거운 분야")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(3.8),
    rows=6, cols=2,
    data=[
        ["사례", "내용"],
        ["Tesla FSD v12", "30만 줄 C++ → 엔드투엔드 신경망으로 대체"],
        ["Edge AI", "기기 자체에서 AI 추론 (지연시간↓, 프라이버시↑)"],
        ["NVIDIA Jetson/DRIVE", "자동차·로봇·드론용 AI 추론 플랫폼"],
        ["SDV (Software-Defined Vehicle)", "현대·기아, BMW — OTA 업데이트 + AI 보조"],
        ["LG webOS AI ThinQ", "TV·냉장고에 음성인식·에너지 최적화 탑재"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.5), Inches(11.5), Inches(0.8),
              '임베디드 AI는 "코딩 보조"가 아닌 제품 자체에 AI를 탑재하는 방향',
              font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 21: AI Code Security
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("AI 코드는 안전한가?")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(5.5), Inches(0.5),
            "AI 생성 코드의 보안 연구", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(5.5), Inches(2.4),
    rows=4, cols=3,
    data=[
        ["연구", "결과", "시기"],
        ["CodeRabbit", "주요 문제 1.7배, 보안 취약점 2.74배", "2025.12"],
        ["Veracode", "3년간 기능↑, 보안성은 미개선", "2025.10"],
        ["GitHub CodeQL", "Broken Access Control +172% YoY", "2025"],
    ])
add_textbox(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(0.5),
            "실제 해킹 사고", font_size=18, color=RED, bold=True)
add_table(slide,
    Inches(7), Inches(1.9), Inches(5.5), Inches(2),
    rows=3, cols=2,
    data=[
        ["사건", "내용"],
        ["Lovable (2025.05)", "1,645개 앱 중 170개에서 개인정보 노출"],
        ["Orchids (2026.02)", "BBC 기자 대상 실시간 해킹 시연 성공"],
    ],
    header_color=RED)
# Visual: Security risk bar
risk_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
    Inches(0.7), Inches(4.7), Inches(11.5), Inches(0.6))
risk_bar.fill.solid()
risk_bar.fill.fore_color.rgb = RGBColor(0xFE, 0xE2, 0xE2)
risk_bar.line.fill.background()
add_textbox(slide, Inches(1), Inches(4.75), Inches(5), Inches(0.4),
            "인간 코드 보안 취약점", font_size=14, color=SLATE, bold=True)
risk_bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
    Inches(0.7), Inches(5.5), Inches(11.5), Inches(0.6))
risk_bar2.fill.solid()
risk_bar2.fill.fore_color.rgb = RED
risk_bar2.line.fill.background()
add_textbox(slide, Inches(1), Inches(5.55), Inches(5), Inches(0.4),
            "AI 코드 보안 취약점 (2.74배)", font_size=14, color=WHITE, bold=True)

# ═══════════════════════════════════════════════════════════
# SLIDE 22: Hard-to-replace fields
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("AI가 대체하기 어려운 분야")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(11), Inches(0.5),
            "보안·금융·방위산업", font_size=18, color=SLATE, bold=True)
add_table(slide,
    Inches(0.7), Inches(1.9), Inches(11.5), Inches(3.2),
    rows=5, cols=3,
    data=[
        ["분야", "AI 도입 상황", "AI의 한계"],
        ["금융", "코드 생성은 가능", "보안 검증 → 전문가 필수"],
        ["방위산업", "2중 3중 안전장치", "검증 부담 오히려 증가"],
        ["의료기기", "IEC 62304 규격", "AI 코드 인증 미확립"],
        ["항공", "DO-178C 규격", "모든 코드 경로 증명 필요"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.5), Inches(11.5), Inches(0.9),
              "AI 생산성 향상 = 동시에 검증 업무량 증가\n→ 보안·검증 전문가 수요 급증",
              font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 23: Chapter 4
# ═══════════════════════════════════════════════════════════
make_chapter_slide("4부", "업무의 변화와 미래", "현장 경험담 + 전망")

# ═══════════════════════════════════════════════════════════
# SLIDE 24: Work Changes
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("실제 업무는 어떻게 변했나?")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(3.8),
    rows=6, cols=3,
    data=[
        ["변화", "Before", "After (AI 도입)"],
        ["코드 작성", "직접 한 줄씩", "AI 초안 → 검토·수정"],
        ["문서 작성", "가장 힘든 업무", "AI 초안 생성 → 10분 완료"],
        ["자료 분석", "1시간 이상", "AI로 10분에 처리"],
        ["기술 학습", "공식문서 + 유튜브", "AI에게 바로 질문"],
        ["데모 영상", "직접 촬영·편집", "AI로 자동 생성"],
    ])
add_quote_box(slide, Inches(0.7), Inches(5.5), Inches(11.5), Inches(0.9),
              "생산성이 올라가니 할 일이 더 많아졌다\n1년 계획을 세웠는데 3개월에 끝남 → 더 많은 프로젝트 진행",
              font_size=17)

# ═══════════════════════════════════════════════════════════
# SLIDE 25: Developer Future
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("개발자의 미래")
add_textbox(slide, Inches(0.7), Inches(1.3), Inches(5.5), Inches(0.5),
            "확실한 것들", font_size=22, color=NAVY_MID, bold=True)
bullets_left = [
    "1. 끊임없는 학습은 10년 전에도,",
    "   지금도, 미래에도 필수",
    "",
    "2. 전문가의 역할은 AI 시대에",
    "   오히려 더 커진다",
    "",
    "3. AI는 도구다 — 망치를 잘 쓰는",
    "   목수가 더 좋은 가구를 만든다",
]
add_textbox(slide, Inches(0.7), Inches(2.0), Inches(5.5), Inches(3.5),
            '\n'.join(bullets_left), font_size=16, color=DARK_TEXT)

add_textbox(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(0.5),
            "미래에 유망한 분야", font_size=22, color=NAVY_MID, bold=True)
add_table(slide,
    Inches(7), Inches(1.9), Inches(5.5), Inches(3.5),
    rows=6, cols=2,
    data=[
        ["분야", "이유"],
        ["AI 에이전트 개발", "새로운 SW 패러다임"],
        ["임베디드 + AI", "제품에 AI 탑재 증가"],
        ["보안·검증", "AI 코드 안전성 확인 필수"],
        ["LLM 인프라", "AI 서비스 기반 구축"],
        ["Edge AI", "기기 자체에서 AI 처리"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 26: Uncertainty
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("미래는 불확실하다")

add_textbox(slide, Inches(0.7), Inches(1.5), Inches(5.5), Inches(0.5),
            "비트코인의 교훈", font_size=20, color=NAVY_MID, bold=True)
add_quote_box(slide, Inches(0.7), Inches(2.1), Inches(5.5), Inches(1.2),
              '처음: "암호키를 사고파는 다단계?"\n현재: 디지털 자산의 표준', font_size=16)

add_textbox(slide, Inches(0.7), Inches(3.6), Inches(5.5), Inches(0.5),
            "기술 도입은 예측이 어렵다", font_size=20, color=NAVY_MID, bold=True)
add_quote_box(slide, Inches(0.7), Inches(4.2), Inches(5.5), Inches(1.2),
              "효용성·경제적 가치보다 정치·사회적 요인이 더 큰 영향\n의료·법률 분야의 AI 도입 → 정치적 요인이 최대 걸림돌",
              font_size=16)

add_textbox(slide, Inches(7), Inches(1.5), Inches(5.5), Inches(0.5),
            "양자 컴퓨터와 비트코인", font_size=20, color=NAVY_MID, bold=True)
add_quote_box(slide, Inches(7), Inches(2.1), Inches(5.5), Inches(1.2),
              "양자 컴퓨터가 개발되면\n비트코인 가치는 올라갈까, 떨어질까?", font_size=16)

add_textbox(slide, Inches(7), Inches(3.6), Inches(5.5), Inches(0.5),
            "AI 신뢰성 문제", font_size=20, color=NAVY_MID, bold=True)
add_quote_box(slide, Inches(7), Inches(4.2), Inches(5.5), Inches(1.2),
              "작고 단순한 문제 → OK\n크고 복잡한 문제 → 아직 믿기 어렵다", font_size=16)

# ═══════════════════════════════════════════════════════════
# SLIDE 27: Summary Table
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("핵심 정리")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(4.5),
    rows=7, cols=2,
    data=[
        ["오해", "진실"],
        ["AI가 개발자를 대체한다", "일부 업무 대체, 전체 고용은 +15% 성장 중"],
        ["코딩만 잘하면 된다", "문제 해결·설계·검증 능력이 더 중요"],
        ["AI 코드는 안전하다", "보안 취약점이 인간 코드의 2.74배"],
        ["개발자 수가 줄어든다", "GitHub에서 매 초 1명 신규 가입"],
        ["임베디드는 AI와 무관", "제품 자체에 AI 탑재 — 가장 뜨거운 분야"],
        ["바이브 코딩이면 충분", "기술 부채 4배, 보안 사고 빈발"],
    ])

# ═══════════════════════════════════════════════════════════
# SLIDE 28: Advice (Insight)
# ═══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_solid_bg(slide, GREEN_BG)
border = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Pt(8), H)
border.fill.solid()
border.fill.fore_color.rgb = GREEN
border.line.fill.background()

add_textbox(slide, Inches(0), Inches(0.5), W, Inches(0.7),
            "여러분에게 드리는 조언", font_size=34, color=RGBColor(0x06, 0x5F, 0x46),
            bold=True, alignment=PP_ALIGN.CENTER)

add_textbox(slide, Inches(1.5), Inches(1.5), Inches(5), Inches(0.5),
            "나를 위한 결정", font_size=26, color=NAVY_DARK, bold=True)
add_quote_box(slide, Inches(1.5), Inches(2.1), Inches(5), Inches(1.8),
              "1. 내가 하고 싶은 것을 찾아라\n\n2. 무엇을 공부할지는 남이 아닌 내가 결정한다",
              font_size=18)

add_textbox(slide, Inches(7), Inches(1.5), Inches(5), Inches(0.5),
            "불확실성에 대응하는 방법", font_size=26, color=NAVY_DARK, bold=True)
add_quote_box(slide, Inches(7), Inches(2.1), Inches(5), Inches(2.8),
              "• 끊임없이 배우기 — 기술은 계속 변한다\n\n"
              "• 부지런한 정보 수집 — 트렌드를 놓치지 않는다\n\n"
              "• 깊이 있는 전문성 — AI가 대체하기 어렵다\n\n"
              "• 호기심을 잃지 않기 — 새 기술을 두려워하지 않는다",
              font_size=18)

# ═══════════════════════════════════════════════════════════
# SLIDE 29: Thank You
# ═══════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_gradient_bg(slide, NAVY_DARK, BLUE)
add_textbox(slide, Inches(0), Inches(2), W, Inches(1),
            "감사합니다!", font_size=52, color=SKY, bold=True,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(3.5), W, Inches(0.7),
            "Q & A", font_size=30, color=WHITE,
            alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(4.8), W, Inches(0.5),
            "건국대학교 컴퓨터공학과 공학박사", font_size=18,
            color=SLATE, alignment=PP_ALIGN.CENTER)
add_textbox(slide, Inches(0), Inches(5.3), W, Inches(0.5),
            "LG전자 CTO Software Platform Lab", font_size=18,
            color=SLATE, alignment=PP_ALIGN.CENTER)

# ═══════════════════════════════════════════════════════════
# SLIDE 30: References
# ═══════════════════════════════════════════════════════════
slide = make_content_slide("참고 자료")
add_table(slide,
    Inches(0.7), Inches(1.4), Inches(11.5), Inches(5.2),
    rows=13, cols=2,
    data=[
        ["주제", "출처"],
        ["미국 SW 개발자 고용 통계", "U.S. Bureau of Labor Statistics (2025)"],
        ["전 세계 개발자 현황", "GitHub Octoverse 2025 (2025.10)"],
        ["AI Copilot 기업 연구", "GitHub × Accenture (2024)"],
        ["바이브 코딩 정의 & 문제", "Wikipedia / Collins Dictionary (2025)"],
        ["AI 코드 보안 취약점", "CodeRabbit (2025.12) / Veracode (2025.10)"],
        ["AI 생태계 보안 사고", "Semafor (2025.05) / BBC News (2026.02)"],
        ["개발자 1/3 실직 전망", "Gartner (2025.09)"],
        ["Shopify AI 채용 정책", "CNBC (2025.04)"],
        ["AI 슬롭 현상", "Wikipedia: AI slop / Korea Herald (2025.12)"],
        ["한국 ICT 인력 현황", "ITSTAT ICT통계포털 (2024 잠정)"],
        ["Tesla FSD", "Wikipedia: Tesla Autopilot"],
        ["Cursor (Anysphere)", "Wikipedia: Anysphere"],
    ],
    font_size=12, header_font_size=13)

# ═══════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "advises_for_high_school_student.pptx")
prs.save(output_path)
print(f"PPT saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
