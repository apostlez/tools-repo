"""
AI 시대의 소프트웨어 개발자의 새로운 역할 — v0.4
Marp 디자인(developer_in_the_ai_era.v0.2.marp.md)을 그대로 재현한 python-pptx 스크립트
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.oxml.ns import qn
from copy import deepcopy
from lxml import etree

# ── Marp 색상 팔레트 ────────────────────────────────────────────────────────
NAVY        = RGBColor(0x1A, 0x1A, 0x2E)   # body bg
NAVY_DARK   = RGBColor(0x16, 0x21, 0x3E)   # card / panel bg
BLUE        = RGBColor(0x0F, 0x3C, 0x88)   # H1 underline / question bg
CYAN        = RGBColor(0x00, 0xD4, 0xFF)   # h2/h3 / accent border
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT       = RGBColor(0xE0, 0xF0, 0xFF)   # td text
GRAY        = RGBColor(0xB0, 0xBE, 0xC5)   # em / footer
YELLOW      = RGBColor(0xFF, 0xD7, 0x00)   # strong / yellow border
ORANGE      = RGBColor(0xFF, 0x80, 0x00)
PINK        = RGBColor(0xFF, 0x40, 0x80)

# ── 슬라이드 기본 ────────────────────────────────────────────────────────────
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
W, H = prs.slide_width, prs.slide_height

# 페이지 여백 (Marp 50px 60px 와 유사)
PAD_X = Inches(0.6)
PAD_Y = Inches(0.5)

# ── 헬퍼 ────────────────────────────────────────────────────────────────────
def _solid(shape, color: RGBColor):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()

def add_rect(slide, l, t, w, h, color: RGBColor):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    _solid(sh, color)
    return sh

def _set_run(run, text, *, size, color, bold=False, italic=False, name="Malgun Gothic"):
    run.text = text
    run.font.name = name
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic

def add_text(slide, l, t, w, h, segments, *, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.15):
    """
    segments: 리스트의 리스트. 각 원소는 한 문단.
              문단은 (text, options) 튜플 리스트.
              options keys: size, color, bold, italic.
    또는 단순 string 한 줄도 허용.
    """
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.03); tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = anchor

    if isinstance(segments, str):
        segments = [[(segments, {})]]
    if segments and isinstance(segments[0], tuple):  # single paragraph
        segments = [segments]

    for i, para_runs in enumerate(segments):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        # clear default run
        if i == 0:
            for r in list(p.runs):
                r.text = ""
        for j, item in enumerate(para_runs):
            text, opts = item
            opts = opts or {}
            run = p.add_run()
            _set_run(run, text,
                     size=opts.get("size", 14),
                     color=opts.get("color", WHITE),
                     bold=opts.get("bold", False),
                     italic=opts.get("italic", False))
    return tb

def add_simple_text(slide, l, t, w, h, text, size, color, *, bold=False,
                    italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    return add_text(slide, l, t, w, h,
                    [(text, {"size": size, "color": color,
                             "bold": bold, "italic": italic})],
                    align=align, anchor=anchor)

def add_bullets(slide, l, t, w, h, items, *, size=14, color=WHITE, bullet="•",
                line_spacing=1.35):
    """
    items: list of either:
        - str (plain bullet, 'strong:' for yellow bold inline not supported here;
               use rich variant below)
        - list[(text, opts), ...] for rich runs (without bullet — bullet auto added)
    """
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.03); tf.margin_bottom = Inches(0.03)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        if i == 0:
            for r in list(p.runs):
                r.text = ""
        # bullet
        run = p.add_run()
        _set_run(run, f"{bullet}  ", size=size, color=CYAN, bold=True)
        if isinstance(item, str):
            run = p.add_run()
            _set_run(run, item, size=size, color=color)
        else:
            for text, opts in item:
                opts = opts or {}
                run = p.add_run()
                _set_run(run, text,
                         size=opts.get("size", size),
                         color=opts.get("color", color),
                         bold=opts.get("bold", False),
                         italic=opts.get("italic", False))
    return tb

# ── 페이지 공통: 배경, 상단 액센트 바, 페이지번호, footer ────────────────────
def base_slide(*, page_no=None, footer=True, bg=NAVY, accent=True):
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    add_rect(sl, 0, 0, W, H, bg)
    if accent:
        add_rect(sl, 0, 0, W, Inches(0.08), CYAN)   # border-top: 6px solid #00D4FF
    if footer:
        add_simple_text(sl, Inches(0.4), H - Inches(0.4), W - Inches(0.8), Inches(0.3),
                        "AI 시대의 소프트웨어 개발자의 새로운 역할",
                        9, GRAY, align=PP_ALIGN.LEFT)
    if page_no is not None:
        add_simple_text(sl, W - Inches(1.0), H - Inches(0.4), Inches(0.6), Inches(0.3),
                        str(page_no), 10, GRAY, align=PP_ALIGN.RIGHT)
    return sl

# ── H1 / H2 ─────────────────────────────────────────────────────────────────
def draw_h1(slide, title, subtitle=None, *, top=None):
    """Marp H1: white 38pt + bottom-border 3px BLUE. Optional H2 (cyan 22pt)."""
    if top is None:
        top = Inches(0.55)
    add_simple_text(slide, PAD_X, top, W - 2 * PAD_X, Inches(0.7),
                    title, 30, WHITE, bold=True, align=PP_ALIGN.LEFT)
    # bottom border (3px blue line). Inches(0.04) ~3px
    add_rect(slide, PAD_X, top + Inches(0.75), W - 2 * PAD_X, Inches(0.04), BLUE)
    if subtitle:
        add_simple_text(slide, PAD_X, top + Inches(0.85), W - 2 * PAD_X, Inches(0.45),
                        subtitle, 18, CYAN, align=PP_ALIGN.LEFT)
        return top + Inches(1.4)
    return top + Inches(1.0)

# ── 카드 / 패널 ─────────────────────────────────────────────────────────────
def draw_card(slide, l, t, w, h, *, top_color=CYAN):
    """배경 #16213E, 상단 4px 컬러 보더, padding 16px"""
    add_rect(slide, l, t, w, h, NAVY_DARK)
    add_rect(slide, l, t, w, Inches(0.06), top_color)
    return (l + Inches(0.18), t + Inches(0.16),
            w - Inches(0.36), h - Inches(0.32))

def card_h3(slide, l, t, w, text, *, color=CYAN, size=15):
    """카드 안 H3 — Marp는 center, 18px cyan"""
    return add_simple_text(slide, l, t, w, Inches(0.4), text, size, color,
                           bold=True, align=PP_ALIGN.CENTER)

def card_body(slide, l, t, w, h, lines, *, size=11, color=LIGHT, align=PP_ALIGN.LEFT):
    """리스트 또는 일반 텍스트(rich segments)"""
    if all(isinstance(x, str) and not x.startswith("•") for x in lines) and len(lines) <= 3 and not any('\n' in s for s in lines):
        # treat as paragraphs (not bullets) — used for short descriptions
        segs = []
        for ln in lines:
            segs.append([(ln, {"size": size, "color": color})])
        return add_text(slide, l, t, w, h, segs, align=align, line_spacing=1.3)
    # bullet list
    return add_bullets(slide, l, t, w, h, lines, size=size, color=color)

# ── Question 박스 ───────────────────────────────────────────────────────────
def draw_question(slide, l, t, w, text, *, size=18, height=Inches(0.6)):
    add_rect(slide, l, t, w, height, BLUE)
    add_simple_text(slide, l + Inches(0.2), t, w - Inches(0.4), height,
                    text, size, YELLOW, bold=True,
                    align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 1 : 표지 (Marp section.cover — gradient + huge cyan H1)
# ────────────────────────────────────────────────────────────────────────────
def slide_cover():
    sl = prs.slides.add_slide(prs.slide_layouts[6])
    # gradient 흉내: 좌→우로 NAVY → NAVY_DARK → BLUE 3단
    add_rect(sl, 0, 0, W, H, NAVY)
    add_rect(sl, Inches(6.5), 0, Inches(3.5), H, NAVY_DARK)
    add_rect(sl, Inches(10.0), 0, W - Inches(10.0), H, BLUE)
    add_rect(sl, 0, 0, W, Inches(0.08), CYAN)

    # Big "AI 시대의" — cyan 64pt
    add_simple_text(sl, Inches(0.9), Inches(1.2), Inches(11), Inches(1.4),
                    "AI 시대의", 56, CYAN, bold=True)
    # "소프트웨어 개발자의" — white 48pt
    add_simple_text(sl, Inches(0.9), Inches(2.4), Inches(11), Inches(1.2),
                    "소프트웨어 개발자의", 44, WHITE, bold=True)
    add_simple_text(sl, Inches(0.9), Inches(3.4), Inches(11), Inches(1.2),
                    "새로운 역할", 44, WHITE, bold=True)
    # hr — 4px cyan, 320px ≒ 3.3 inch
    add_rect(sl, Inches(0.9), Inches(4.9), Inches(3.3), Inches(0.05), CYAN)
    # subtitle
    add_simple_text(sl, Inches(0.9), Inches(5.1), Inches(11), Inches(0.5),
                    "건국대학교사범대학부속고등학교  |  2026", 18, GRAY)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 2 : 목차 (테이블)
# ────────────────────────────────────────────────────────────────────────────
def slide_toc():
    sl = base_slide(page_no=2)
    body_top = draw_h1(sl, "목차", "오늘 강의에서 다룰 내용")
    rows = [
        ("01", "강사 소개"),
        ("02", "문제 제기 — 개발자, 사라지는 걸까?"),
        ("03", "현상 분석 — 실제로 무슨 일이 일어나고 있나"),
        ("04", "사례 제시 — AI가 못하는 영역"),
        ("05", "업무의 변화 — 내 일상이 달라졌다"),
        ("06", "앞으로의 전망 — 개발자의 삶, 불확실성, 나의 결정과 준비"),
    ]
    # Marp 스타일 테이블 흉내
    tbl_l, tbl_t = PAD_X, body_top + Inches(0.1)
    tbl_w = W - 2 * PAD_X
    header_h = Inches(0.55)
    row_h = Inches(0.65)

    # Header
    col1_w = Inches(1.4)
    add_rect(sl, tbl_l, tbl_t, col1_w, header_h, BLUE)
    add_rect(sl, tbl_l + col1_w, tbl_t, tbl_w - col1_w, header_h, BLUE)
    add_rect(sl, tbl_l, tbl_t + header_h - Inches(0.04), tbl_w, Inches(0.04), CYAN)
    add_simple_text(sl, tbl_l, tbl_t, col1_w, header_h, "  #", 16, CYAN, bold=True,
                    anchor=MSO_ANCHOR.MIDDLE)
    add_simple_text(sl, tbl_l + col1_w, tbl_t, tbl_w - col1_w, header_h, "  주제",
                    16, CYAN, bold=True, anchor=MSO_ANCHOR.MIDDLE)

    # Rows
    for i, (num, title) in enumerate(rows):
        ry = tbl_t + header_h + i * row_h
        add_rect(sl, tbl_l, ry, col1_w, row_h, NAVY_DARK)
        add_rect(sl, tbl_l + col1_w, ry, tbl_w - col1_w, row_h, NAVY_DARK)
        # 하단 1px 라인
        add_rect(sl, tbl_l, ry + row_h - Inches(0.015), tbl_w, Inches(0.015), BLUE)
        add_simple_text(sl, tbl_l + Inches(0.2), ry, col1_w, row_h, num,
                        15, YELLOW, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        add_simple_text(sl, tbl_l + col1_w + Inches(0.2), ry, tbl_w - col1_w, row_h,
                        title, 15, LIGHT, anchor=MSO_ANCHOR.MIDDLE)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 3 : 01. 강사 소개
# ────────────────────────────────────────────────────────────────────────────
def slide_intro():
    sl = base_slide(page_no=3)
    body_top = draw_h1(sl, "01. 강사 소개")
    # twocol wide-left (3fr : 2fr)
    gap = Inches(0.3)
    total_w = W - 2 * PAD_X
    left_w = (total_w - gap) * 3 / 5
    right_w = total_w - gap - left_w
    panel_h = H - body_top - Inches(0.85)

    # Left panel
    cl, ct, cw, ch = draw_card(sl, PAD_X, body_top, left_w, panel_h, top_color=CYAN)
    card_h3(sl, cl, ct, cw, "오늘 이 자리에 온 이유", size=18)
    add_bullets(sl, cl, ct + Inches(0.55), cw, ch - Inches(0.55), [
        [("AI가 개발자를 대체한다는 뉴스, 여러분도 들어봤나요?", {})],
        [("현직 개발자로서 ", {}), ("실제 변화를 직접 겪고 있습니다", {"bold": True, "color": YELLOW})],
        [("매체로 접하는 이야기 vs 현업의 목소리", {})],
        [("여러분이 미래를 선택하는 데 도움이 되길 바랍니다", {})],
    ], size=16, color=WHITE)

    # Right panel
    rl, rt, rw, rh = draw_card(sl, PAD_X + left_w + gap, body_top, right_w, panel_h, top_color=CYAN)
    card_h3(sl, rl, rt, rw, "프로필", size=18)
    add_simple_text(sl, rl, rt + Inches(0.55), rw, Inches(0.45),
                    "플랫폼 소프트웨어 개발자", 17, YELLOW, bold=True)
    add_bullets(sl, rl, rt + Inches(1.05), rw, rh - Inches(1.1), [
        "LG전자 CTO Software Platform Lab",
        "2012 ~",
        "webOS, ThinQ, UP가전",
        "AI 도구 도입·활용",
    ], size=15, color=WHITE)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 4 : 02. 뉴스로 본 현실 (3 cards + question)
# ────────────────────────────────────────────────────────────────────────────
def slide_news():
    sl = base_slide(page_no=4)
    body_top = draw_h1(sl, "02. 뉴스로 본 현실", "AI 도입 이후 일어나고 있는 일들")
    # 3 cards
    cards = [
        ("대규모 해고", CYAN, "구글·메타 등 빅테크, ", "AI 도입 이후", " 수만 명 SW 개발자 정리해고"),
        ("앱 생태계 혼란", YELLOW, "AI ", "바이브 코딩", "으로 앱 스토어에 저품질 앱이 폭발적으로 증가"),
        ("AI가 코드 작성", CYAN, "GitHub Copilot 등 AI 코딩 도우미, ", "생산성 55% 향상", " 보고"),
    ]
    gap = Inches(0.25)
    total_w = W - 2 * PAD_X
    cw = (total_w - gap * 2) / 3
    ch = Inches(3.0)
    for i, (title, top_c, pre, strong, post) in enumerate(cards):
        cx = PAD_X + i * (cw + gap)
        il, it, iw, ih = draw_card(sl, cx, body_top, cw, ch, top_color=top_c)
        card_h3(sl, il, it, iw, title, size=18, color=top_c)
        add_text(sl, il, it + Inches(0.7), iw, ih - Inches(0.7),
                 [[(pre, {"size": 15, "color": LIGHT}),
                   (strong, {"size": 15, "color": YELLOW, "bold": True}),
                   (post, {"size": 15, "color": LIGHT})]],
                 align=PP_ALIGN.LEFT, line_spacing=1.4)
    # question box
    qy = body_top + ch + Inches(0.3)
    draw_question(sl, PAD_X, qy, total_w, "그렇다면 앞으로 SW 개발자의 전망은?", size=20, height=Inches(0.7))

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 5 : 03. SW 개발자의 세계 (table + insight panel)
# ────────────────────────────────────────────────────────────────────────────
def slide_role_diversity():
    sl = base_slide(page_no=5)
    body_top = draw_h1(sl, "03. SW 개발자의 세계 — 얼마나 다양한가?")
    gap = Inches(0.4)
    total_w = W - 2 * PAD_X
    left_w = (total_w - gap) / 2
    right_w = left_w
    body_h = H - body_top - Inches(0.85)

    # Left — title + 도형 막대그래프 + small question
    add_simple_text(sl, PAD_X, body_top, left_w, Inches(0.4),
                    "전 세계 SW 개발자 직군 비율 (추정)", 16, WHITE, bold=True)

    # 도형으로 직접 그리는 수평 막대그래프 (Office 호환성 100%)
    rows = [
        ("웹/앱 개발", 60, True),
        ("서버/백엔드", 20, False),
        ("시스템 SW", 10, False),
        ("임베디드", 7, False),
        ("기타(AI·보안 등)", 3, False),
    ]
    chart_top = body_top + Inches(0.55)
    chart_h = Inches(3.4)
    label_w = Inches(1.7)        # 좌측 카테고리 라벨 폭
    bar_area_l = PAD_X + label_w
    bar_area_w = left_w - label_w - Inches(0.7)   # 우측 % 표시 공간 확보
    max_val = 70                  # 축 최대값
    bar_h = Inches(0.42)
    row_gap = (chart_h - bar_h * len(rows)) / max(1, len(rows) - 1)

    # 축 라인 (좌측 세로선)
    add_rect(sl, bar_area_l, chart_top, Inches(0.02), chart_h, BLUE)

    for i, (label, val, strong) in enumerate(rows):
        ry = chart_top + i * (bar_h + row_gap)
        # 카테고리 라벨 (우측 정렬)
        add_simple_text(sl, PAD_X, ry, label_w - Inches(0.1), bar_h,
                        label, 13, LIGHT,
                        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
        # 막대
        bw = int(bar_area_w * val / max_val)
        bar_color = YELLOW if strong else CYAN
        add_rect(sl, bar_area_l + Inches(0.02), ry, bw, bar_h, bar_color)
        # 값 라벨 (% — 막대 끝 우측)
        add_simple_text(sl, bar_area_l + Inches(0.02) + bw + Inches(0.08),
                        ry, Inches(0.7), bar_h,
                        f"{val}%", 13, YELLOW,
                        bold=True, anchor=MSO_ANCHOR.MIDDLE)

    # small question
    qy = chart_top + chart_h + Inches(0.15)
    draw_question(sl, PAD_X, qy, left_w,
                  "하지만 개발자는 명확한 역할 분리가 어렵다.",
                  size=14, height=Inches(0.5))

    # Right — insight panel
    rl, rt, rw, rh = draw_card(sl, PAD_X + left_w + gap, body_top, right_w, body_h, top_color=CYAN)
    card_h3(sl, rl, rt, rw, "핵심 인사이트", size=18)
    add_bullets(sl, rl, rt + Inches(0.55), rw, rh - Inches(0.55), [
        [("AI 코딩이 가장 큰 영향을 주는 분야는 ", {}),
         ("웹·앱", {"bold": True, "color": YELLOW}), (" 개발 영역", {})],
        [("시스템·임베디드·보안은 ", {}),
         ("AI가 쉽게 대체하기 어렵다", {"bold": True, "color": YELLOW})],
        [("AI 발전 → 새로운 ", {}),
         ("AI 관련 직군이 새로 생겨나는 중", {"bold": True, "color": YELLOW})],
    ], size=15, color=WHITE, line_spacing=1.5)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 6 : 03. AI가 잘하는 것 vs 시장 (twocol panels)
# ────────────────────────────────────────────────────────────────────────────
def slide_lang_market():
    sl = base_slide(page_no=6)
    body_top = draw_h1(sl, "03. AI가 잘하는 것 vs 시장이 원하는 것")
    gap = Inches(0.4)
    total_w = W - 2 * PAD_X
    pw = (total_w - gap) / 2
    body_h = H - body_top - Inches(0.85)

    def panel_table(x, top_color, header_text, table_rows, foot=None):
        cl, ct, cw, ch = draw_card(sl, x, body_top, pw, body_h, top_color=top_color)
        card_h3(sl, cl, ct, cw, header_text, size=17, color=top_color)
        # table
        th_h = Inches(0.45)
        tr_h = Inches(0.45)
        tx = cl
        ty = ct + Inches(0.55)
        col1 = cw * 0.6
        col2 = cw - col1
        add_rect(sl, tx, ty, cw, th_h, BLUE)
        add_rect(sl, tx, ty + th_h - Inches(0.03), cw, Inches(0.03), top_color)
        add_simple_text(sl, tx + Inches(0.1), ty, col1, th_h, "  " + table_rows[0][0],
                        13, top_color, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        add_simple_text(sl, tx + col1, ty, col2 - Inches(0.1), th_h, table_rows[0][1],
                        13, top_color, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
        for i, (label, val, strong) in enumerate(table_rows[1:]):
            ry = ty + th_h + i * tr_h
            add_rect(sl, tx, ry, cw, tr_h, NAVY_DARK)
            add_rect(sl, tx, ry + tr_h - Inches(0.012), cw, Inches(0.012), BLUE)
            add_simple_text(sl, tx + Inches(0.15), ry, col1, tr_h, label,
                            12, LIGHT, anchor=MSO_ANCHOR.MIDDLE)
            add_simple_text(sl, tx + col1, ry, col2 - Inches(0.15), tr_h, val,
                            13, YELLOW if strong else LIGHT, bold=strong,
                            anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
        if foot:
            fy = ty + th_h + (len(table_rows) - 1) * tr_h + Inches(0.2)
            add_simple_text(sl, cl, fy, cw, Inches(0.4), foot, 12, GRAY, italic=True)

    # Left: 언어 TOP 5
    panel_table(PAD_X, CYAN, "AI 코딩 도구 사용 언어 TOP 5",
                [("언어", "점유율"),
                 ("Python", "35%", True),
                 ("JavaScript", "28%", False),
                 ("TypeScript", "15%", False),
                 ("Java", "12%", False),
                 ("기타", "10%", False)],
                foot="→ 주로 웹·데이터·스크립트 영역에 집중")
    # Right: 시장 규모
    panel_table(PAD_X + pw + gap, YELLOW, "글로벌 SW 시장 규모 (2025 추정)",
                [("분야", "규모"),
                 ("클라우드 서비스", "$800B", True),
                 ("엔터프라이즈 SW", "$650B", False),
                 ("임베디드·IoT", "$300B", False),
                 ("AI/ML 플랫폼", "$200B", False),
                 ("보안 SW", "$180B", False)])

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 7 : 04. 임베디드 (twocol wide-left)
# ────────────────────────────────────────────────────────────────────────────
def slide_embedded():
    sl = base_slide(page_no=7)
    body_top = draw_h1(sl, "04. 사례 ① 임베디드 소프트웨어", "AI가 쉽게 들어오지 못하는 이유")
    gap = Inches(0.3)
    total_w = W - 2 * PAD_X
    left_w = (total_w - gap) * 3 / 5
    right_w = total_w - gap - left_w
    body_h = H - body_top - Inches(0.85)

    # Left orange panel
    cl, ct, cw, ch = draw_card(sl, PAD_X, body_top, left_w, body_h, top_color=ORANGE)
    add_text(sl, cl, ct, cw, Inches(0.5),
             [[("임베디드란?", {"size": 17, "color": ORANGE, "bold": True}),
               (" — 세탁기·TV·자동차 안에 들어가는 소프트웨어", {"size": 14, "color": LIGHT})]])
    add_bullets(sl, cl, ct + Inches(0.6), cw, ch - Inches(0.6), [
        [("외부에 공개되지 않는 ", {}), ("독점 코드", {"bold": True, "color": YELLOW}),
         (" → AI 학습 데이터 없음", {})],
        [("하드웨어와 밀접 → ", {}),
         ("물리적 테스트 없이 검증 불가", {"bold": True, "color": YELLOW})],
        [("AI 할루시네이션(엉뚱한 코드)이 하드웨어 고장으로 이어짐", {})],
        [("현장에서 통하는 농담: ", {}),
         ('"우리는 AI의 인간 하네스가 됐다"', {"italic": True, "color": GRAY})],
        [("그러나 ", {}), ("문서 작성·패턴 분석", {"bold": True, "color": YELLOW}),
         ("에는 AI가 크게 도움됨", {})],
    ], size=14, color=WHITE, line_spacing=1.45)

    # Right: stacked two panels
    rx = PAD_X + left_w + gap
    sub_h = (body_h - gap) / 2
    # top
    pl, pt, pw, ph = draw_card(sl, rx, body_top, right_w, sub_h, top_color=ORANGE)
    card_h3(sl, pl, pt, pw, "개발자 반응", size=17, color=ORANGE)
    add_text(sl, pl, pt + Inches(0.55), pw, ph - Inches(0.55),
             [[("AI 도입을 환영하지만", {"size": 15, "color": WHITE})],
              [("생각만큼 활용하지", {"size": 15, "color": YELLOW, "bold": True})],
              [("못하고 있다", {"size": 15, "color": YELLOW, "bold": True})]],
             align=PP_ALIGN.CENTER, line_spacing=1.5)
    # bottom
    pl, pt, pw, ph = draw_card(sl, rx, body_top + sub_h + gap, right_w, sub_h, top_color=CYAN)
    card_h3(sl, pl, pt, pw, "핵심", size=17)
    add_text(sl, pl, pt + Inches(0.55), pw, ph - Inches(0.55),
             [[("전문 도메인 지식 +", {"size": 15, "color": WHITE})],
              [("하드웨어 이해는", {"size": 15, "color": WHITE})],
              [("여전히 인간의 영역", {"size": 16, "color": YELLOW, "bold": True})]],
             align=PP_ALIGN.CENTER, line_spacing=1.5)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 8 : 04. 보안·금융·방위산업 (3 cards)
# ────────────────────────────────────────────────────────────────────────────
def slide_security_finance():
    sl = base_slide(page_no=8)
    body_top = draw_h1(sl, "04. 사례 ② 보안 · 금융 · 방위산업", "신뢰성과 검증이 최우선인 분야")
    cards = [
        ("보안 분야", CYAN, [
            [("AI 생성 코드에서 ", {}), ("보안 취약점", {"bold": True, "color": YELLOW}),
             (" 발견 사례 증가", {})],
            [("OWASP Top 10 — AI도 이 실수를 반복함", {})],
            [("오히려 보안 검증 전문가 수요 증가", {})],
        ]),
        ("금융 분야", YELLOW, [
            [("금융 사고 예방 = ", {}), ("수천억 원 손실 방지", {"bold": True, "color": YELLOW})],
            [("규제·컴플라이언스 코드는 AI가 임의 생성 불가", {})],
            [("AI 코드 감사(audit) 전문가가 새 직군으로 등장", {})],
        ]),
        ("방위산업", ORANGE, [
            [("이중·삼중 안전장치 의무화", {})],
            [("AI 생성 코드는 ", {}), ("보안 인증 통과 불가", {"bold": True, "color": YELLOW})],
            [("전문 인력의 역할이 오히려 더 중요해짐", {})],
        ]),
    ]
    gap = Inches(0.25)
    total_w = W - 2 * PAD_X
    cw = (total_w - gap * 2) / 3
    body_h = H - body_top - Inches(0.85)
    for i, (title, top_c, items) in enumerate(cards):
        cx = PAD_X + i * (cw + gap)
        cl, ct, ciw, cih = draw_card(sl, cx, body_top, cw, body_h, top_color=top_c)
        card_h3(sl, cl, ct, ciw, title, size=18, color=top_c)
        add_bullets(sl, cl, ct + Inches(0.6), ciw, cih - Inches(0.6),
                    items, size=13, color=LIGHT, line_spacing=1.5)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 9 : 05. 내 일상이 달라졌다 (5 cards + question)
# ────────────────────────────────────────────────────────────────────────────
def slide_work_change():
    sl = base_slide(page_no=9)
    body_top = draw_h1(sl, "05. 내 일상이 달라졌다", "현직 개발자가 경험한 AI 도입 전·후")
    cards = [
        ("코드 작성", "95% 감소", "설계·기능 명세 후 직접 코딩하는 시간이 거의 사라짐", CYAN),
        ("문서 작성", "줄었다", "가장 힘든 업무였던 코드 설명 문서를 AI가 초안 작성", CYAN),
        ("자료 분석", "빨라졌다", "연구개발 실험·결과 정리·통계 분석을 AI로 대체", YELLOW),
        ("유튜브 시청", "줄었다", "공식 문서·영상을 AI가 즉시 요약. 데모 영상도 AI 제작", ORANGE),
        ("할 일의 양", "늘었다!", "1년 계획이 3개월 만에 끝나서 더 할 일을 찾고 있음", PINK),
    ]
    gap = Inches(0.18)
    total_w = W - 2 * PAD_X
    cw = (total_w - gap * 4) / 5
    ch = Inches(3.5)
    for i, (title, big, desc, top_c) in enumerate(cards):
        cx = PAD_X + i * (cw + gap)
        cl, ct, ciw, cih = draw_card(sl, cx, body_top, cw, ch, top_color=top_c)
        card_h3(sl, cl, ct, ciw, title, size=15, color=top_c)
        add_simple_text(sl, cl, ct + Inches(0.55), ciw, Inches(0.5),
                        big, 18, YELLOW, bold=True, align=PP_ALIGN.CENTER)
        add_simple_text(sl, cl, ct + Inches(1.15), ciw, cih - Inches(1.2),
                        desc, 11, LIGHT, align=PP_ALIGN.CENTER)
    # question
    qy = body_top + ch + Inches(0.25)
    draw_question(sl, PAD_X, qy, total_w,
                  "생산성이 오를수록, 더 많은 일·더 큰 목표가 생긴다",
                  size=18, height=Inches(0.65))

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 10 : 06-1. 개발자의 삶 (twocol wide-left + blockquote)
# ────────────────────────────────────────────────────────────────────────────
def slide_future_dev():
    sl = base_slide(page_no=10)
    body_top = draw_h1(sl, "06-1. 앞으로의 전망 — 개발자의 삶")
    gap = Inches(0.3)
    total_w = W - 2 * PAD_X
    left_w = (total_w - gap) * 3 / 5
    right_w = total_w - gap - left_w
    body_h = H - body_top - Inches(0.85)

    # Left panel
    cl, ct, cw, ch = draw_card(sl, PAD_X, body_top, left_w, body_h, top_color=CYAN)
    add_simple_text(sl, cl, ct, cw, Inches(0.4),
                    "10년 전에 10년·20년 후를 상상했을 때와", 13, GRAY, italic=True)
    add_simple_text(sl, cl, ct + Inches(0.4), cw, Inches(0.7),
                    "크게 다르지 않다 — 끊임없는 학습", 22, CYAN, bold=True)
    add_rect(sl, cl, ct + Inches(1.15), cw, Inches(0.025), BLUE)
    add_bullets(sl, cl, ct + Inches(1.3), cw, ch - Inches(1.3), [
        [("끊임없는 학습과 자기 계발", {"bold": True, "color": YELLOW}),
         (" — 새 언어·프레임워크가 나올 때마다 배워왔다 → AI 도구도 마찬가지", {})],
        [("전문가의 역할은 더 커진다", {"bold": True, "color": YELLOW}),
         (" — 확실한 미래", {})],
        [("비전문가가 늘어나면서 ", {}),
         ("전문가의 진입 장벽이 더 높아짐", {"bold": True, "color": YELLOW})],
        [("AI 도구를 다루는 기술 자체가 하나의 능력", {"bold": True, "color": YELLOW})],
    ], size=14, color=WHITE, line_spacing=1.5)

    # Right blockquote — left border 4px cyan, italic
    rx = PAD_X + left_w + gap
    add_rect(sl, rx, body_top, right_w, body_h, NAVY_DARK)
    add_rect(sl, rx, body_top, Inches(0.06), body_h, CYAN)
    add_text(sl, rx + Inches(0.3), body_top + Inches(0.5), right_w - Inches(0.5), body_h - Inches(1.0),
             [[("AI는 주니어 개발자를 대체하는 것이 아니라,",
                {"size": 14, "color": WHITE, "italic": True})],
              [("", {})],
              [("AI를 쓰는 개발자가",
                {"size": 16, "color": YELLOW, "bold": True})],
              [("AI를 안 쓰는 개발자를 대체한다",
                {"size": 16, "color": YELLOW, "bold": True})]],
             line_spacing=1.4)
    add_simple_text(sl, rx + Inches(0.3), body_top + body_h - Inches(0.6), right_w - Inches(0.5), Inches(0.4),
                    "— 실리콘밸리 엔지니어링 리더", 11, GRAY, italic=True)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 11 : 06-2. 미래의 불확실성 (cards.four)
# ────────────────────────────────────────────────────────────────────────────
def slide_uncertainty():
    sl = base_slide(page_no=11)
    body_top = draw_h1(sl, "06-2. 앞으로의 전망 — 미래의 불확실성")
    cards = [
        ("비트코인의 교훈", YELLOW, [
            ("처음엔 ", LIGHT, False, False),
            ('"암호키 다단계 아냐?"', GRAY, False, True),
            (" → 지금은 디지털 금. ", LIGHT, False, False),
            ("양자 컴퓨터가 나오면?", YELLOW, True, False),
            (" 아무도 모른다", LIGHT, False, False),
        ]),
        ("정치적 영향", CYAN, [
            ("기술 도입은 ", LIGHT, False, False),
            ("효용·경제성보다 정치적 영향", YELLOW, True, False),
            ("이 더 큼. 의료·법률 AI 도입의 가장 큰 걸림돌", LIGHT, False, False),
        ]),
        ("트렌드 속도", ORANGE, [
            ("기술 변화 속도가 ", LIGHT, False, False),
            ("점점 빨라진다", YELLOW, True, False),
            (". 특정 분야에 집중하지 않으면 따라잡기 어려움", LIGHT, False, False),
        ]),
        ("AI 신뢰성", PINK, [
            ("작고 단순한 작업은 OK. ", LIGHT, False, False),
            ("크고 복잡한 영역", YELLOW, True, False),
            ("에서 AI의 처리 능력은 아직 믿기 어려움", LIGHT, False, False),
        ]),
    ]
    gap = Inches(0.2)
    total_w = W - 2 * PAD_X
    cw = (total_w - gap * 3) / 4
    body_h = H - body_top - Inches(0.85)
    for i, (title, top_c, runs) in enumerate(cards):
        cx = PAD_X + i * (cw + gap)
        cl, ct, ciw, cih = draw_card(sl, cx, body_top, cw, body_h, top_color=top_c)
        card_h3(sl, cl, ct, ciw, title, size=17, color=top_c)
        # paragraph with rich runs
        para = [(text, {"size": 13, "color": color, "bold": bold, "italic": italic})
                for text, color, bold, italic in runs]
        add_text(sl, cl, ct + Inches(0.7), ciw, cih - Inches(0.7),
                 [para], align=PP_ALIGN.LEFT, line_spacing=1.6)

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 12 : 06-3/4. 나를 위한 결정과 준비 (twocol panels + question)
# ────────────────────────────────────────────────────────────────────────────
def slide_decision():
    sl = base_slide(page_no=12)
    body_top = draw_h1(sl, "06-3 / 06-4. 나를 위한 결정과 준비")
    gap = Inches(0.4)
    total_w = W - 2 * PAD_X
    pw = (total_w - gap) / 2
    body_h = H - body_top - Inches(1.5)   # leave room for question

    # Left
    cl, ct, cw, ch = draw_card(sl, PAD_X, body_top, pw, body_h, top_color=CYAN)
    card_h3(sl, cl, ct, cw, "나를 위한 결정", size=18)
    add_bullets(sl, cl, ct + Inches(0.6), cw, ch - Inches(0.6), [
        [("내가 ", {}), ("하고 싶은 것", {"bold": True, "color": YELLOW}),
         (", 원하는 것", {})],
        [("무엇을 공부할지는 ", {}),
         ("내가 결정", {"bold": True, "color": YELLOW}), ("하는 것", {})],
        [("남의 말·뉴스에 휩쓸리지 말 것", {})],
    ], size=15, color=WHITE, line_spacing=1.6)

    # Right
    rl, rt, rw, rh = draw_card(sl, PAD_X + pw + gap, body_top, pw, body_h, top_color=YELLOW)
    card_h3(sl, rl, rt, rw, "불확실성에 대응하는 준비", size=18, color=YELLOW)
    add_bullets(sl, rl, rt + Inches(0.6), rw, rh - Inches(0.6), [
        [("학습과 부지런한 정보 수집", {"bold": True, "color": YELLOW})],
        [("현상을 분석·이해하는 ", {}),
         ("안목과 유연성", {"bold": True, "color": YELLOW})],
        [("공식 문서 + AI 요약 조합 활용", {})],
        [("작은 프로젝트로 ", {}),
         ("직접 써보고 느껴라", {"bold": True, "color": YELLOW})],
    ], size=15, color=WHITE, line_spacing=1.6)

    # question
    qy = body_top + body_h + Inches(0.3)
    draw_question(sl, PAD_X, qy, total_w,
                  "불확실한 미래일수록, 결정의 주체는 '나' 자신이다",
                  size=18, height=Inches(0.65))

# ────────────────────────────────────────────────────────────────────────────
# 슬라이드 13 : 마무리 (closing — bg #16213E)
# ────────────────────────────────────────────────────────────────────────────
def slide_closing():
    sl = base_slide(page_no=13, bg=NAVY_DARK)
    body_top = draw_h1(sl, "마무리 — 여러분에게 전하고 싶은 말")
    gap = Inches(0.4)
    total_w = W - 2 * PAD_X
    pw = (total_w - gap) / 2
    body_h = H - body_top - Inches(0.85)

    # Left — 오늘의 핵심 (panel)
    cl, ct, cw, ch = draw_card(sl, PAD_X, body_top, pw, body_h, top_color=CYAN)
    card_h3(sl, cl, ct, cw, "오늘의 핵심", size=18)
    items = [
        ("1.", "AI가 모든 개발자를 대체하진 않는다", False),
        ("2.", "전문성 있는 개발자는 더 강해진다", True),
        ("3.", "AI는 도구 — 잘 쓰는 사람이 앞서간다", False),
        ("4.", "불확실성 속에서 내 결정이 중요하다", True),
    ]
    for i, (n, txt, strong) in enumerate(items):
        ny = ct + Inches(0.6) + i * Inches(0.6)
        add_simple_text(sl, cl, ny, Inches(0.4), Inches(0.5),
                        n, 16, CYAN, bold=True)
        add_text(sl, cl + Inches(0.45), ny, cw - Inches(0.45), Inches(0.5),
                 [[(txt, {"size": 15, "color": YELLOW if strong else WHITE,
                          "bold": strong})]])

    # Right — 메시지 + Q&A
    rx = PAD_X + pw + gap
    rw = pw
    add_text(sl, rx, body_top, rw, Inches(2.6),
             [[("AI 시대에도 결국 중요한 건",
                {"size": 18, "color": WHITE})],
              [("'사람'과 '전문성'", {"size": 22, "color": YELLOW, "bold": True}),
               ("입니다.", {"size": 18, "color": WHITE})],
              [("", {})],
              [("여러분이 무엇을 좋아하고", {"size": 16, "color": WHITE})],
              [("무엇을 잘하고 싶은지", {"size": 16, "color": WHITE})],
              [("그것부터 찾으세요.",
                {"size": 18, "color": YELLOW, "bold": True})]],
             line_spacing=1.4)
    qy = body_top + body_h - Inches(0.8)
    draw_question(sl, rx, qy, rw,
                  "Q & A  |  궁금한 것은 무엇이든 물어보세요!",
                  size=18, height=Inches(0.7))

# ── 실행 ────────────────────────────────────────────────────────────────────
slide_cover()
slide_toc()
slide_intro()
slide_news()
slide_role_diversity()
slide_lang_market()
slide_embedded()
slide_security_finance()
slide_work_change()
slide_future_dev()
slide_uncertainty()
slide_decision()
slide_closing()

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "developer_in_the_ai_era.v0.4.pptx")
prs.save(out_path)
print(f"저장 완료: {out_path}")
print(f"총 슬라이드: {len(prs.slides)}")
