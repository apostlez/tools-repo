"""
AI 시대의 소프트웨어 개발자의 새로운 역할
고등학생 대상 특강 PPT 생성 스크립트
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy
from lxml import etree

# ── 색상 팔레트 ──────────────────────────────────────────────────────────────
C_PRIMARY   = RGBColor(0x1A, 0x1A, 0x2E)   # 네이비 (배경 / 마스터 헤더)
C_ACCENT    = RGBColor(0x16, 0x21, 0x3E)   # 다크 블루
C_HIGHLIGHT = RGBColor(0x0F, 0x3C, 0x88)   # 블루 (제목 바)
C_NEON      = RGBColor(0x00, 0xD4, 0xFF)   # 사이언 (포인트)
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_LIGHT     = RGBColor(0xE0, 0xF0, 0xFF)   # 연한 파랑 (본문 배경)
C_GRAY      = RGBColor(0xB0, 0xBE, 0xC5)
C_YELLOW    = RGBColor(0xFF, 0xD7, 0x00)   # 강조 포인트

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

W = prs.slide_width
H = prs.slide_height

# ── 헬퍼 함수 ────────────────────────────────────────────────────────────────
def solid_fill(shape, color: RGBColor):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color

def add_rect(slide, l, t, w, h, color: RGBColor, alpha=None):
    shape = slide.shapes.add_shape(1, l, t, w, h)   # MSO_SHAPE_TYPE.RECTANGLE = 1
    solid_fill(shape, color)
    shape.line.fill.background()
    return shape

def add_textbox(slide, l, t, w, h, text, font_size, color: RGBColor,
                bold=False, align=PP_ALIGN.LEFT, wrap=True, italic=False):
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    return txb

def add_bullet_box(slide, l, t, w, h, items, font_size=18,
                   text_color=C_PRIMARY, bullet_color=C_NEON,
                   bold_first=False, line_spacing=1.2):
    txb = slide.shapes.add_textbox(l, t, w, h)
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        # 들여쓰기 레벨 처리
        if item.startswith("    ") or item.startswith("　"):
            text = "    • " + item.strip()
            run.font.size = Pt(font_size - 2)
        else:
            text = "▸ " + item.strip()
            run.font.size = Pt(font_size)
        run.text = text
        run.font.color.rgb = text_color
        run.font.bold = (bold_first and i == 0)
    return txb

def draw_header(slide, title_text, subtitle_text="", section_num=""):
    """공통 헤더: 상단 컬러 바 + 섹션 번호 + 제목"""
    # 배경
    bg = add_rect(slide, 0, 0, W, H, C_PRIMARY)
    # 상단 강조 바
    add_rect(slide, 0, 0, W, Inches(0.08), C_NEON)
    # 헤더 영역
    add_rect(slide, 0, 0, W, Inches(1.4), C_HIGHLIGHT)
    # 섹션 번호 원
    if section_num:
        circ = slide.shapes.add_shape(9, Inches(0.3), Inches(0.18), Inches(1.0), Inches(1.0))
        solid_fill(circ, C_NEON)
        circ.line.fill.background()
        tf = circ.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run()
        run.text = section_num
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = C_PRIMARY
        # 수직 가운데 정렬
        from pptx.enum.text import MSO_ANCHOR
        tf.auto_size = None
        tf.word_wrap = False
        circ.text_frame.paragraphs[0].runs[0].font.size = Pt(22)
    # 제목
    title_l = Inches(1.5) if section_num else Inches(0.5)
    add_textbox(slide, title_l, Inches(0.2), W - title_l - Inches(0.3), Inches(1.0),
                title_text, 32, C_WHITE, bold=True)
    # 부제목
    if subtitle_text:
        add_textbox(slide, title_l, Inches(0.9), W - title_l - Inches(0.3), Inches(0.5),
                    subtitle_text, 14, C_NEON, bold=False)
    # 하단 라인
    add_rect(slide, 0, H - Inches(0.25), W, Inches(0.25), C_HIGHLIGHT)
    add_textbox(slide, Inches(0.2), H - Inches(0.25), W - Inches(0.4), Inches(0.25),
                "AI 시대의 소프트웨어 개발자의 새로운 역할  |  고등학생 특강",
                9, C_GRAY, align=PP_ALIGN.RIGHT)
    return Inches(1.5)   # content_top 반환

def content_area(l=Inches(0.5), t=Inches(1.55), w=None, h=None):
    if w is None: w = W - Inches(1.0)
    if h is None: h = H - Inches(1.9)
    return l, t, w, h

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 1 : 표지
# ════════════════════════════════════════════════════════════════════════════
def slide_cover():
    sl = prs.slides.add_slide(prs.slide_layouts[6])   # blank
    # 배경
    add_rect(sl, 0, 0, W, H, C_PRIMARY)
    add_rect(sl, 0, 0, W, Inches(0.08), C_NEON)
    # 대각선 장식 사각형
    add_rect(sl, W - Inches(4), 0, Inches(4), H, C_ACCENT)
    add_rect(sl, W - Inches(4), 0, Inches(0.06), H, C_NEON)
    # 메인 타이틀
    add_textbox(sl, Inches(0.7), Inches(1.5), Inches(8.5), Inches(1.2),
                "AI 시대의", 52, C_NEON, bold=True)
    add_textbox(sl, Inches(0.7), Inches(2.5), Inches(8.5), Inches(1.4),
                "소프트웨어 개발자의", 46, C_WHITE, bold=True)
    add_textbox(sl, Inches(0.7), Inches(3.5), Inches(8.5), Inches(1.2),
                "새로운 역할", 46, C_WHITE, bold=True)
    # 구분선
    add_rect(sl, Inches(0.7), Inches(4.85), Inches(5.0), Inches(0.05), C_NEON)
    # 부제목
    add_textbox(sl, Inches(0.7), Inches(5.0), Inches(8.0), Inches(0.5),
                "고등학생 특강  |  2026", 18, C_GRAY)
    # 우측 장식 텍스트
    add_textbox(sl, W - Inches(3.8), Inches(2.0), Inches(3.3), Inches(4.0),
                "DEVELOPER\nIN THE\nAI ERA", 28, C_HIGHLIGHT, bold=True, align=PP_ALIGN.CENTER)
    # 하단
    add_rect(sl, 0, H - Inches(0.25), W, Inches(0.25), C_HIGHLIGHT)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 2 : 목차
# ════════════════════════════════════════════════════════════════════════════
def slide_toc():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "목차", "오늘 강의에서 다룰 내용")
    l, t, w, h = content_area()
    sections = [
        ("01", "강사 소개"),
        ("02", "문제 제기 — 개발자, 사라지는 걸까?"),
        ("03", "현상 분석 — 실제로 무슨 일이 일어나고 있나"),
        ("04", "사례 제시 — AI가 못하는 영역"),
        ("05", "업무의 변화 — 내 일상이 달라졌다"),
        ("06", "앞으로의 전망 — 그래서 어떻게 살아야 할까"),
    ]
    item_h = Inches(0.78)
    for i, (num, title) in enumerate(sections):
        ty = t + i * item_h
        # 번호 박스
        num_box = add_rect(sl, l, ty, Inches(0.65), Inches(0.62), C_NEON)
        add_textbox(sl, l, ty + Inches(0.06), Inches(0.65), Inches(0.5),
                    num, 18, C_PRIMARY, bold=True, align=PP_ALIGN.CENTER)
        # 제목
        add_textbox(sl, l + Inches(0.8), ty + Inches(0.1), w - Inches(0.9), Inches(0.5),
                    title, 20, C_WHITE, bold=False)
        # 밑줄
        add_rect(sl, l + Inches(0.8), ty + Inches(0.62), w - Inches(0.9), Inches(0.015), C_HIGHLIGHT)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 3 : 강사 소개
# ════════════════════════════════════════════════════════════════════════════
def slide_intro():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "강사 소개", section_num="01")
    l, t, w, h = content_area()
    # 좌측 프로필 카드
    card_w = Inches(4.5)
    add_rect(sl, l, t, card_w, h, C_ACCENT)
    add_rect(sl, l, t, card_w, Inches(0.06), C_NEON)
    # 프로필 아이콘 (원)
    circ = sl.shapes.add_shape(9, l + Inches(1.5), t + Inches(0.4), Inches(1.5), Inches(1.5))
    solid_fill(circ, C_NEON)
    circ.line.fill.background()
    add_textbox(sl, l + Inches(1.5), t + Inches(0.5), Inches(1.5), Inches(1.2),
                "👤", 36, C_PRIMARY, align=PP_ALIGN.CENTER)
    add_textbox(sl, l + Inches(0.2), t + Inches(2.1), card_w - Inches(0.4), Inches(0.5),
                "임베디드 소프트웨어 개발자", 14, C_NEON, bold=True, align=PP_ALIGN.CENTER)
    add_textbox(sl, l + Inches(0.2), t + Inches(2.6), card_w - Inches(0.4), Inches(1.5),
                "LG전자 임베디드 개발팀\n소프트웨어 경력 10년 이상\nAI 도구 도입·활용 경험 보유", 14, C_LIGHT, align=PP_ALIGN.CENTER)
    # 우측 소개 내용
    rx = l + card_w + Inches(0.4)
    rw = W - rx - Inches(0.3)
    add_textbox(sl, rx, t, rw, Inches(0.5), "오늘 이 자리에 온 이유", 18, C_NEON, bold=True)
    bullets = [
        "AI가 개발자를 대체한다는 뉴스, 여러분도 들어봤나요?",
        "현직 개발자로서 실제 변화를 직접 겪고 있습니다",
        "과장된 공포 vs 진짜 기회 — 함께 생각해 봐요",
        "여러분이 미래를 선택하는 데 도움이 되길 바랍니다",
    ]
    add_bullet_box(sl, rx, t + Inches(0.6), rw, h - Inches(0.6),
                   bullets, font_size=17, text_color=C_WHITE)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 4 : 문제 제기 — 뉴스 헤드라인
# ════════════════════════════════════════════════════════════════════════════
def slide_problem_news():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "뉴스로 본 현실", "AI 도입 이후 일어나고 있는 일들", section_num="02")
    l, t, w, h = content_area()
    news = [
        ("💼", "대규모 해고", "구글·메타 등 빅테크, AI 도입 이후 수만 명 SW 개발자 정리해고"),
        ("📱", "앱 생태계 혼란", "AI 바이브 코딩으로 앱 스토어에 저품질 앱이 폭발적으로 증가"),
        ("🤖", "AI가 코드 작성", "GitHub Copilot 등 AI 코딩 도우미, 생산성 55% 향상 보고"),
    ]
    card_w = (w - Inches(0.4)) / 3
    for i, (icon, title, desc) in enumerate(news):
        cx = l + i * (card_w + Inches(0.2))
        add_rect(sl, cx, t, card_w, h, C_ACCENT)
        add_rect(sl, cx, t, card_w, Inches(0.06), C_NEON if i != 1 else C_YELLOW)
        add_textbox(sl, cx, t + Inches(0.3), card_w, Inches(0.8),
                    icon, 40, C_WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.15), t + Inches(1.2), card_w - Inches(0.3), Inches(0.5),
                    title, 18, C_NEON if i != 1 else C_YELLOW, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.15), t + Inches(1.8), card_w - Inches(0.3), h - Inches(2.0),
                    desc, 14, C_LIGHT, align=PP_ALIGN.CENTER, wrap=True)
    # 하단 질문
    add_rect(sl, l, H - Inches(1.0), w, Inches(0.65), C_HIGHLIGHT)
    add_textbox(sl, l + Inches(0.2), H - Inches(0.95), w - Inches(0.4), Inches(0.55),
                "❓  그렇다면 앞으로 SW 개발자라는 직업은 사라질까요?",
                18, C_YELLOW, bold=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 5 : 현상 분석 — 개발자 직군 분류
# ════════════════════════════════════════════════════════════════════════════
def slide_analysis_types():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "SW 개발자의 세계 — 얼마나 다양한가?", section_num="03")
    l, t, w, h = content_area()
    # 좌측 설명
    lw = Inches(5.5)
    rows = [
        ("웹/앱 개발", "60%", C_NEON),
        ("서버/백엔드", "20%", C_LIGHT),
        ("시스템 소프트웨어", "10%", C_YELLOW),
        ("임베디드", "7%",  RGBColor(0xFF, 0x80, 0x00)),
        ("기타(AI·보안 등)", "3%",  RGBColor(0xFF, 0x40, 0x80)),
    ]
    add_textbox(sl, l, t, lw, Inches(0.4),
                "전 세계 SW 개발자 직군 비율 (추정)", 14, C_GRAY)
    bar_t = t + Inches(0.5)
    for i, (label, pct, color) in enumerate(rows):
        by = bar_t + i * Inches(0.72)
        add_textbox(sl, l, by, Inches(2.0), Inches(0.45), label, 14, C_WHITE, bold=True)
        bar_full_w = lw - Inches(2.3)
        pct_val = int(pct.replace('%', ''))
        bar_fill_w = bar_full_w * pct_val / 100
        add_rect(sl, l + Inches(2.2), by + Inches(0.08), bar_fill_w, Inches(0.32), color)
        add_textbox(sl, l + Inches(2.2) + bar_fill_w + Inches(0.1), by, Inches(0.8), Inches(0.45),
                    pct, 14, color, bold=True)
    # 우측 핵심 메시지
    rx = l + lw + Inches(0.4)
    rw = W - rx - Inches(0.3)
    add_rect(sl, rx, t, rw, h, C_ACCENT)
    add_rect(sl, rx, t, rw, Inches(0.06), C_NEON)
    add_textbox(sl, rx + Inches(0.2), t + Inches(0.2), rw - Inches(0.4), Inches(0.5),
                "핵심 인사이트", 16, C_NEON, bold=True)
    insights = [
        "AI 코딩이 가장 큰 영향을 주는 분야는\n'웹·앱' 개발 영역",
        "시스템·임베디드·보안은\nAI가 쉽게 대체하기 어렵다",
        "AI 발전 → 새로운 AI 관련\n직군이 새로 생겨나는 중",
    ]
    for i, ins in enumerate(insights):
        iy = t + Inches(0.9) + i * Inches(1.3)
        add_rect(sl, rx + Inches(0.15), iy, rw - Inches(0.3), Inches(1.1), C_HIGHLIGHT)
        add_textbox(sl, rx + Inches(0.25), iy + Inches(0.1), rw - Inches(0.5), Inches(0.9),
                    ins, 14, C_WHITE, wrap=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 6 : 현상 분석 — AI 코딩 언어 & 시장
# ════════════════════════════════════════════════════════════════════════════
def slide_analysis_market():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "AI가 잘하는 것 vs 시장이 원하는 것", section_num="03")
    l, t, w, h = content_area()
    # 좌측 — AI 코딩 언어
    lw = (w - Inches(0.3)) / 2
    add_rect(sl, l, t, lw, h, C_ACCENT)
    add_rect(sl, l, t, lw, Inches(0.06), C_NEON)
    add_textbox(sl, l + Inches(0.2), t + Inches(0.1), lw - Inches(0.4), Inches(0.45),
                "AI 코딩 도구 사용 언어 TOP 5", 15, C_NEON, bold=True)
    langs = [("Python", 35), ("JavaScript", 28), ("TypeScript", 15), ("Java", 12), ("기타", 10)]
    for i, (lang, pct) in enumerate(langs):
        ly = t + Inches(0.7) + i * Inches(0.6)
        add_textbox(sl, l + Inches(0.2), ly, Inches(1.6), Inches(0.45), lang, 14, C_WHITE, bold=True)
        bar_w = (lw - Inches(2.2)) * pct / 35
        add_rect(sl, l + Inches(2.0), ly + Inches(0.08), bar_w, Inches(0.3), C_NEON)
        add_textbox(sl, l + Inches(2.0) + bar_w + Inches(0.1), ly, Inches(0.6), Inches(0.45),
                    f"{pct}%", 13, C_NEON, bold=True)
    add_textbox(sl, l + Inches(0.2), t + Inches(3.8), lw - Inches(0.4), Inches(0.5),
                "→ 주로 웹·데이터·스크립트 영역에 집중", 13, C_GRAY, italic=True)
    # 우측 — SW 시장 규모
    rx = l + lw + Inches(0.3)
    rw = lw
    add_rect(sl, rx, t, rw, h, C_ACCENT)
    add_rect(sl, rx, t, rw, Inches(0.06), C_YELLOW)
    add_textbox(sl, rx + Inches(0.2), t + Inches(0.1), rw - Inches(0.4), Inches(0.45),
                "글로벌 SW 시장 규모 (2025 추정)", 15, C_YELLOW, bold=True)
    markets = [
        ("엔터프라이즈 SW", "$650B"),
        ("임베디드·IoT", "$300B"),
        ("클라우드 서비스", "$800B"),
        ("AI/ML 플랫폼", "$200B"),
        ("보안 SW", "$180B"),
    ]
    for i, (name, size) in enumerate(markets):
        my = t + Inches(0.7) + i * Inches(0.65)
        add_rect(sl, rx + Inches(0.2), my + Inches(0.08), Inches(0.3), Inches(0.3), C_YELLOW)
        add_textbox(sl, rx + Inches(0.65), my, rw - Inches(1.5), Inches(0.45),
                    name, 13, C_WHITE)
        add_textbox(sl, rx + rw - Inches(1.3), my, Inches(1.2), Inches(0.45),
                    size, 13, C_YELLOW, bold=True, align=PP_ALIGN.RIGHT)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 7 : 사례 — 임베디드
# ════════════════════════════════════════════════════════════════════════════
def slide_case_embedded():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "사례 ① 임베디드 소프트웨어", "AI가 쉽게 들어오지 못하는 이유", section_num="04")
    l, t, w, h = content_area()
    # 좌측 설명 카드
    lw = Inches(6.0)
    add_rect(sl, l, t, lw, h, C_ACCENT)
    add_rect(sl, l, t, lw, Inches(0.06), RGBColor(0xFF, 0x80, 0x00))
    add_textbox(sl, l + Inches(0.2), t + Inches(0.15), lw - Inches(0.4), Inches(0.45),
                "임베디드란? — 세탁기·TV·자동차 안에 들어가는 소프트웨어", 13, RGBColor(0xFF, 0x80, 0x00), bold=True)
    bullets_emb = [
        "외부에 공개되지 않는 독점 코드 → AI 학습 데이터 없음",
        "하드웨어와 밀접 → 물리적 테스트 없이 검증 불가",
        "AI 할루시네이션(엉뚱한 코드)이 하드웨어 고장으로 이어짐",
        '현장에서 통하는 농담: "우리는 AI의 인간 하네스가 됐다"',
        "그러나 문서 작성·패턴 분석에는 AI가 크게 도움됨",
    ]
    add_bullet_box(sl, l + Inches(0.2), t + Inches(0.75), lw - Inches(0.4), h - Inches(0.9),
                   bullets_emb, font_size=16, text_color=C_WHITE)
    # 우측 — 핵심 메시지 박스
    rx = l + lw + Inches(0.3)
    rw = W - rx - Inches(0.3)
    add_rect(sl, rx, t, rw, h * 0.55, RGBColor(0xFF, 0x80, 0x00))
    add_textbox(sl, rx + Inches(0.15), t + Inches(0.2), rw - Inches(0.3), Inches(0.5),
                "개발자 반응", 16, C_PRIMARY, bold=True)
    add_textbox(sl, rx + Inches(0.15), t + Inches(0.8), rw - Inches(0.3), h * 0.4,
                "AI 도입을 환영하지만\n생각만큼 활용하지\n못하고 있다", 16, C_PRIMARY, bold=False, wrap=True)
    add_rect(sl, rx, t + h * 0.58, rw, h * 0.42, C_HIGHLIGHT)
    add_textbox(sl, rx + Inches(0.15), t + h * 0.60, rw - Inches(0.3), h * 0.38,
                "전문 도메인 지식 +\n하드웨어 이해는\n여전히 인간의 영역", 15, C_NEON, bold=True, wrap=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 8 : 사례 — 보안·금융·방위산업
# ════════════════════════════════════════════════════════════════════════════
def slide_case_security():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "사례 ② 보안 · 금융 · 방위산업", "신뢰성과 검증이 최우선인 분야", section_num="04")
    l, t, w, h = content_area()
    cards = [
        ("🔐", "보안 분야", C_NEON,
         ["AI 생성 코드에서 보안 취약점 발견 사례 증가",
          "OWASP Top 10 — AI도 이 실수를 반복함",
          "오히려 보안 검증 전문가 수요 증가"]),
        ("🏦", "금융 분야", C_YELLOW,
         ["금융 사고 예방 = 수천억 원 손실 방지",
          "규제·컴플라이언스 코드는 AI가 임의 생성 불가",
          "AI 코드 감사(audit) 전문가가 새 직군으로 등장"]),
        ("🛡️", "방위산업", RGBColor(0xFF, 0x80, 0x00),
         ["이중·삼중 안전장치 의무화",
          "AI 생성 코드는 보안 인증 통과 불가",
          "전문 인력의 역할이 오히려 더 중요해짐"]),
    ]
    card_w = (w - Inches(0.4)) / 3
    for i, (icon, title, color, items) in enumerate(cards):
        cx = l + i * (card_w + Inches(0.2))
        add_rect(sl, cx, t, card_w, h, C_ACCENT)
        add_rect(sl, cx, t, card_w, Inches(0.06), color)
        add_textbox(sl, cx, t + Inches(0.2), card_w, Inches(0.7),
                    icon, 36, C_WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.1), t + Inches(1.0), card_w - Inches(0.2), Inches(0.5),
                    title, 17, color, bold=True, align=PP_ALIGN.CENTER)
        add_rect(sl, cx + Inches(0.2), t + Inches(1.55), card_w - Inches(0.4), Inches(0.04), color)
        add_bullet_box(sl, cx + Inches(0.1), t + Inches(1.7), card_w - Inches(0.2), h - Inches(2.0),
                       items, font_size=13, text_color=C_LIGHT)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 9 : 업무의 변화
# ════════════════════════════════════════════════════════════════════════════
def slide_work_change():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "내 일상이 달라졌다", "현직 개발자가 경험한 AI 도입 전·후", section_num="05")
    l, t, w, h = content_area()
    changes = [
        ("📝", "문서 작성", "줄었다",
         "가장 힘든 업무였던\n코드 설명 문서를\nAI가 초안 작성", C_NEON, True),
        ("🔬", "데이터 분석", "빨라졌다",
         "실험 결과 정리·\n통계 분석을\nAI로 대체", C_YELLOW, True),
        ("▶️", "유튜브 시청", "줄었다",
         "AI로 영상 요약·\n공식 문서 설명을\n즉시 받음", RGBColor(0xFF, 0x80, 0x00), True),
        ("📈", "할 일의 양", "늘었다!",
         "1년치 계획이\n3개월 만에 완료 →\n더 많은 목표 설정", RGBColor(0xFF, 0x40, 0x80), False),
    ]
    card_w = (w - Inches(0.6)) / 4
    for i, (icon, cat, result, desc, color, positive) in enumerate(changes):
        cx = l + i * (card_w + Inches(0.2))
        add_rect(sl, cx, t, card_w, h, C_ACCENT)
        add_rect(sl, cx, t, card_w, Inches(0.06), color)
        add_textbox(sl, cx, t + Inches(0.2), card_w, Inches(0.65),
                    icon, 32, C_WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.1), t + Inches(0.95), card_w - Inches(0.2), Inches(0.4),
                    cat, 14, C_GRAY, bold=False, align=PP_ALIGN.CENTER)
        add_rect(sl, cx + Inches(0.1), t + Inches(1.45), card_w - Inches(0.2), Inches(0.42), color)
        add_textbox(sl, cx + Inches(0.1), t + Inches(1.5), card_w - Inches(0.2), Inches(0.35),
                    result, 15, C_PRIMARY if positive else C_WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.1), t + Inches(2.05), card_w - Inches(0.2), h - Inches(2.2),
                    desc, 13, C_LIGHT, align=PP_ALIGN.CENTER, wrap=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 10 : 앞으로의 전망 — 개발자의 삶
# ════════════════════════════════════════════════════════════════════════════
def slide_future_dev():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "앞으로의 전망 ① — 개발자의 삶", section_num="06")
    l, t, w, h = content_area()
    # 좌측 메시지
    lw = Inches(6.2)
    add_rect(sl, l, t, lw, h, C_ACCENT)
    add_rect(sl, l, t, lw, Inches(0.06), C_NEON)
    add_textbox(sl, l + Inches(0.2), t + Inches(0.15), lw - Inches(0.4), Inches(0.5),
                "10년 전에 10년·20년 후를 상상했을 때와", 16, C_GRAY)
    add_textbox(sl, l + Inches(0.2), t + Inches(0.65), lw - Inches(0.4), Inches(0.7),
                "크게 다르지 않다 — 끊임없는 학습", 24, C_NEON, bold=True)
    add_rect(sl, l + Inches(0.2), t + Inches(1.45), lw - Inches(0.4), Inches(0.04), C_HIGHLIGHT)
    items = [
        "새 언어·프레임워크가 나올 때마다 배워왔다 → AI 도구도 같다",
        "전문성(도메인 지식)의 가치는 오히려 더 높아진다",
        "AI를 '도구'로 잘 다루는 개발자가 경쟁력을 가진다",
        "확실한 것: 전문가의 역할은 줄어들지 않는다",
    ]
    add_bullet_box(sl, l + Inches(0.2), t + Inches(1.6), lw - Inches(0.4), h - Inches(1.8),
                   items, font_size=16, text_color=C_WHITE)
    # 우측 인용
    rx = l + lw + Inches(0.3)
    rw = W - rx - Inches(0.3)
    add_rect(sl, rx, t, rw, h, C_HIGHLIGHT)
    add_textbox(sl, rx + Inches(0.2), t + Inches(0.3), rw - Inches(0.4), Inches(0.4),
                "\" \"", 60, C_NEON, bold=True)
    add_textbox(sl, rx + Inches(0.2), t + Inches(1.1), rw - Inches(0.4), Inches(2.5),
                "AI는 주니어 개발자를 대체하는 것이 아니라,\nAI를 쓰는 개발자가\nAI를 안 쓰는 개발자를 대체한다",
                15, C_WHITE, wrap=True)
    add_textbox(sl, rx + Inches(0.2), t + Inches(3.7), rw - Inches(0.4), Inches(0.4),
                "— 실리콘밸리 엔지니어링 리더", 12, C_GRAY, italic=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 11 : 앞으로의 전망 — 불확실성과 나의 선택
# ════════════════════════════════════════════════════════════════════════════
def slide_future_choice():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    draw_header(sl, "앞으로의 전망 ② — 불확실성과 나의 선택", section_num="06")
    l, t, w, h = content_area()
    # 비트코인 비유
    add_rect(sl, l, t, W - Inches(1.0), Inches(1.5), C_ACCENT)
    add_rect(sl, l, t, Inches(0.06), Inches(1.5), C_YELLOW)
    add_textbox(sl, l + Inches(0.3), t + Inches(0.1), W - Inches(1.5), Inches(0.5),
                "비트코인 비유 — 미래는 항상 불확실하다", 16, C_YELLOW, bold=True)
    add_textbox(sl, l + Inches(0.3), t + Inches(0.65), W - Inches(1.5), Inches(0.75),
                '처음 봤을 때: "암호키를 사고파는 다단계 아냐?"  →  지금은 디지털 금\n'
                "양자 컴퓨터가 개발되면 비트코인 가격은?  →  아무도 모른다",
                14, C_LIGHT)
    # 3개 카드
    cards2 = [
        ("🧭", "내가 원하는 것\n먼저 정하기",
         "무엇을 공부할지는\n내가 결정한다\n남의 말에 흔들리지 말자", C_NEON),
        ("📚", "부지런한\n정보 수집",
         "AI 뉴스는 빠르다\n공식 문서 + AI 요약\n조합이 최강", C_YELLOW),
        ("🔁", "학습과\n실험 반복",
         "써보기 전엔 모른다\n작은 프로젝트로\n직접 느껴라", RGBColor(0xFF, 0x80, 0x00)),
    ]
    card_w2 = (W - Inches(1.0) - Inches(0.4)) / 3
    ct = t + Inches(1.65)
    ch = h - Inches(1.65)
    for i, (icon, title, desc, color) in enumerate(cards2):
        cx = l + i * (card_w2 + Inches(0.2))
        add_rect(sl, cx, ct, card_w2, ch, C_ACCENT)
        add_rect(sl, cx, ct, card_w2, Inches(0.06), color)
        add_textbox(sl, cx, ct + Inches(0.2), card_w2, Inches(0.7),
                    icon, 32, C_WHITE, align=PP_ALIGN.CENTER)
        add_textbox(sl, cx + Inches(0.1), ct + Inches(1.0), card_w2 - Inches(0.2), Inches(0.8),
                    title, 15, color, bold=True, align=PP_ALIGN.CENTER, wrap=True)
        add_textbox(sl, cx + Inches(0.1), ct + Inches(1.9), card_w2 - Inches(0.2), ch - Inches(2.1),
                    desc, 13, C_LIGHT, align=PP_ALIGN.CENTER, wrap=True)

# ════════════════════════════════════════════════════════════════════════════
# 슬라이드 12 : 마무리
# ════════════════════════════════════════════════════════════════════════════
def slide_closing():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    # 배경
    add_rect(sl, 0, 0, W, H, C_PRIMARY)
    add_rect(sl, 0, 0, W, Inches(0.08), C_NEON)
    add_rect(sl, 0, H - Inches(0.08), W, Inches(0.08), C_NEON)
    # 장식
    add_rect(sl, 0, 0, Inches(4), H, C_ACCENT)
    add_rect(sl, Inches(4), 0, Inches(0.06), H, C_NEON)
    # 좌측 요약
    add_textbox(sl, Inches(0.3), Inches(0.8), Inches(3.4), Inches(0.5),
                "오늘의 핵심", 16, C_NEON, bold=True)
    summaries = [
        "AI가 모든 개발자를 대체하진 않는다",
        "전문성 있는 개발자는 더 강해진다",
        "AI는 도구 — 잘 쓰는 자가 이긴다",
        "불확실성 속에서 내 결정이 중요하다",
    ]
    for i, s in enumerate(summaries):
        sy = Inches(1.5) + i * Inches(0.95)
        add_rect(sl, Inches(0.3), sy, Inches(0.35), Inches(0.35), C_NEON)
        add_textbox(sl, Inches(0.8), sy - Inches(0.05), Inches(3.0), Inches(0.5),
                    s, 14, C_WHITE, wrap=True)
    # 우측 마무리 메시지
    add_textbox(sl, Inches(4.5), Inches(1.0), Inches(8.3), Inches(1.0),
                "여러분에게 전하고 싶은 말", 22, C_NEON, bold=True)
    add_rect(sl, Inches(4.5), Inches(2.0), Inches(8.0), Inches(0.04), C_HIGHLIGHT)
    add_textbox(sl, Inches(4.5), Inches(2.2), Inches(8.0), Inches(3.5),
                "AI 시대에도 결국 중요한 건\n'사람'과 '전문성'입니다.\n\n"
                "여러분이 무엇을 좋아하고\n무엇을 잘하고 싶은지\n그것부터 찾으세요.",
                20, C_WHITE, wrap=True)
    add_rect(sl, Inches(4.5), H - Inches(1.3), Inches(8.0), Inches(0.65), C_HIGHLIGHT)
    add_textbox(sl, Inches(4.7), H - Inches(1.25), Inches(7.6), Inches(0.55),
                "Q & A  |  궁금한 것은 무엇이든 물어보세요!", 18, C_NEON, bold=True)

# ── 슬라이드 생성 실행 ──────────────────────────────────────────────────────
slide_cover()
slide_toc()
slide_intro()
slide_problem_news()
slide_analysis_types()
slide_analysis_market()
slide_case_embedded()
slide_case_security()
slide_work_change()
slide_future_dev()
slide_future_choice()
slide_closing()

# ── 저장 ───────────────────────────────────────────────────────────────────
import os
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI시대_SW개발자의새로운역할_특강.pptx")
prs.save(out_path)
print(f"저장 완료: {out_path}")
