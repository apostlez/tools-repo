---
marp: true
theme: default
size: 16:9
paginate: true
backgroundColor: "#1A1A2E"
color: "#FFFFFF"
style: |
  section {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    padding: 50px 60px;
    background: #1A1A2E;
    color: #FFFFFF;
    border-top: 6px solid #00D4FF;
  }
  h1 {
    color: #FFFFFF;
    font-size: 38px;
    border-bottom: 3px solid #0F3C88;
    padding-bottom: 12px;
    margin-bottom: 20px;
  }
  h2 {
    color: #00D4FF;
    font-size: 22px;
    margin-top: 0;
  }
  h3 {
    color: #00D4FF;
    font-size: 20px;
  }
  strong { color: #FFD700; }
  em { color: #B0BEC5; }
  ul, ol { font-size: 18px; line-height: 1.6; }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 16px;
    margin-top: 12px;
  }
  th {
    background: #0F3C88;
    color: #00D4FF;
    padding: 10px;
    text-align: left;
    border-bottom: 2px solid #00D4FF;
  }
  td {
    background: #16213E;
    color: #E0F0FF;
    padding: 10px;
    border-bottom: 1px solid #0F3C88;
  }
  blockquote {
    border-left: 4px solid #00D4FF;
    background: #16213E;
    color: #FFFFFF;
    padding: 16px 24px;
    font-style: italic;
    margin: 16px 0;
  }
  code {
    background: #0F3C88;
    color: #00D4FF;
    padding: 2px 6px;
    border-radius: 3px;
  }
  footer {
    color: #B0BEC5;
    font-size: 11px;
  }
  section.cover {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 70%, #0F3C88 100%);
    text-align: left;
    padding: 80px;
  }
  section.cover h1 {
    font-size: 64px;
    border: none;
    color: #00D4FF;
    margin-bottom: 0;
  }
  section.cover h2 {
    font-size: 48px;
    color: #FFFFFF;
    border: none;
    margin-top: 8px;
  }
  section.cover hr {
    border: none;
    border-top: 4px solid #00D4FF;
    width: 320px;
    margin: 30px 0;
  }
  section.cover p { font-size: 22px; color: #B0BEC5; }
  section.section {
    background: #16213E;
    text-align: center;
    border-top: 6px solid #00D4FF;
  }
  section.section h1 {
    font-size: 56px;
    color: #00D4FF;
    border: none;
  }
  section.section h2 {
    font-size: 24px;
    color: #FFFFFF;
  }
  section.closing {
    background: #16213E;
  }
  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
  }
  .cards.four { grid-template-columns: repeat(4, 1fr); }
  .card {
    background: #16213E;
    border-top: 4px solid #00D4FF;
    padding: 16px;
    border-radius: 4px;
  }
  .card.yellow { border-top-color: #FFD700; }
  .card.orange { border-top-color: #FF8000; }
  .card.pink { border-top-color: #FF4080; }
  .card h3 {
    margin: 4px 0 8px;
    font-size: 18px;
    text-align: center;
  }
  .card .icon { font-size: 32px; text-align: center; display: block; margin-bottom: 8px; }
  .card p { font-size: 13px; color: #E0F0FF; margin: 4px 0; }
  .card ul { font-size: 13px; padding-left: 18px; }
  .twocol {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .twocol.wide-left { grid-template-columns: 3fr 2fr; }
  .panel {
    background: #16213E;
    border-top: 4px solid #00D4FF;
    padding: 18px 22px;
  }
  .panel.yellow { border-top-color: #FFD700; }
  .panel.orange { border-top-color: #FF8000; }
  .badge {
    display: inline-block;
    background: #00D4FF;
    color: #1A1A2E;
    padding: 4px 12px;
    font-weight: bold;
    border-radius: 4px;
    margin-right: 8px;
  }
  .question {
    background: #0F3C88;
    color: #FFD700;
    font-size: 22px;
    font-weight: bold;
    padding: 16px 24px;
    margin-top: 24px;
    border-radius: 4px;
  }
  .bar {
    background: #0F3C88;
    height: 22px;
    border-radius: 3px;
    margin: 4px 0;
  }
  .bar-fill {
    background: #00D4FF;
    height: 100%;
    border-radius: 3px;
  }
footer: "AI 시대의 소프트웨어 개발자의 새로운 역할"
---

<!-- _class: cover -->
<!-- _paginate: false -->
<!-- _footer: "" -->

# AI 시대의

## 소프트웨어 개발자의<br>새로운 역할

<hr>

건국대학교사범대학부속고등학교  |  2026

---

# 목차

## 오늘 강의에서 다룰 내용

| # | 주제 |
|---|---|
| **01** | 강사 소개 |
| **02** | 문제 제기 — 개발자, 사라지는 걸까? |
| **03** | 현상 분석 — 실제로 무슨 일이 일어나고 있나 |
| **04** | 사례 제시 — AI가 못하는 영역 |
| **05** | 업무의 변화 — 내 일상이 달라졌다 |
| **06** | 앞으로의 전망 — 개발자의 삶, 불확실성, 나의 결정과 준비 |

---

# 01. 강사 소개

<div class="twocol wide-left">
<div class="panel">

### 오늘 이 자리에 온 이유

- AI가 개발자를 대체한다는 뉴스, 여러분도 들어봤나요?
- 현직 개발자로서 **실제 변화를 직접 겪고 있습니다**
- 매체로 접하는 이야기 vs 현업의 목소리
- 여러분이 미래를 선택하는 데 도움이 되길 바랍니다

</div>
<div class="panel">

### 프로필

**플랫폼 소프트웨어 개발자**

- LG전자 CTO Software Platform Lab
- 2012 ~
- webOS, ThinQ, UP가전
- AI 도구 도입·활용

</div>
</div>

---

# 02. 뉴스로 본 현실

## AI 도입 이후 일어나고 있는 일들

<div class="cards">
<div class="card">

### 대규모 해고

구글·메타 등 빅테크, **AI 도입 이후** 수만 명 SW 개발자 정리해고

</div>
<div class="card yellow">

### 앱 생태계 혼란

AI **바이브 코딩**으로 앱 스토어에 저품질 앱이 폭발적으로 증가

</div>
<div class="card">

### AI가 코드 작성

GitHub Copilot 등 AI 코딩 도우미, **생산성 55% 향상** 보고

</div>
</div>

<div class="question">그렇다면 앞으로 SW 개발자의 전망은?</div>

---

# 03. SW 개발자의 세계 — 얼마나 다양한가?

<div class="twocol">
<div>

**전 세계 SW 개발자 직군 비율 (추정)**

| 직군 | 비율 |
|---|---:|
| 웹/앱 개발 | **60%** |
| 서버/백엔드 | 20% |
| 시스템 소프트웨어 | 10% |
| 임베디드 | 7% |
| 기타(AI·보안 등) | 3% |

<div class="question" style="font-size: 16px; padding: 10px 16px;">하지만 개발자는 명확한 역할 분리가 어렵다.</div>

</div>


<div class="panel">

### 핵심 인사이트

- AI 코딩이 가장 큰 영향을 주는 분야는 **웹·앱** 개발 영역
- 시스템·임베디드·보안은 **AI가 쉽게 대체하기 어렵다**
- AI 발전 → 새로운 **AI 관련 직군이 새로 생겨나는 중**

</div>
</div>

---

# 03. AI가 잘하는 것 vs 시장이 원하는 것

<div class="twocol">
<div class="panel">

### AI 코딩 도구 사용 언어 TOP 5

| 언어 | 점유율 |
|---|---:|
| Python | **35%** |
| JavaScript | 28% |
| TypeScript | 15% |
| Java | 12% |
| 기타 | 10% |

*→ 주로 웹·데이터·스크립트 영역에 집중*

</div>
<div class="panel yellow">

### 글로벌 SW 시장 규모 (2025 추정)

| 분야 | 규모 |
|---|---:|
| 클라우드 서비스 | **$800B** |
| 엔터프라이즈 SW | $650B |
| 임베디드·IoT | $300B |
| AI/ML 플랫폼 | $200B |
| 보안 SW | $180B |

</div>
</div>

---

# 04. 사례 ① 임베디드 소프트웨어

## AI가 쉽게 들어오지 못하는 이유

<div class="twocol wide-left">
<div class="panel orange">

**임베디드란?** — 세탁기·TV·자동차 안에 들어가는 소프트웨어

- 외부에 공개되지 않는 **독점 코드** → AI 학습 데이터 없음
- 하드웨어와 밀접 → **물리적 테스트 없이 검증 불가**
- AI 할루시네이션(엉뚱한 코드)이 하드웨어 고장으로 이어짐
- 현장에서 통하는 농담: *"우리는 AI의 인간 하네스가 됐다"*
- 그러나 **문서 작성·패턴 분석**에는 AI가 크게 도움됨

</div>
<div>

<div class="panel orange">

### 개발자 반응

AI 도입을 환영하지만<br>**생각만큼 활용하지<br>못하고 있다**

</div>

<div class="panel">

### 핵심

전문 도메인 지식 +<br>하드웨어 이해는<br>**여전히 인간의 영역**

</div>

</div>
</div>

---

# 04. 사례 ② 보안 · 금융 · 방위산업

## 신뢰성과 검증이 최우선인 분야

<div class="cards">
<div class="card">

### 보안 분야

- AI 생성 코드에서 **보안 취약점** 발견 사례 증가
- OWASP Top 10 — AI도 이 실수를 반복함
- 오히려 보안 검증 전문가 수요 증가

</div>
<div class="card yellow">

### 금융 분야

- 금융 사고 예방 = **수천억 원 손실 방지**
- 규제·컴플라이언스 코드는 AI가 임의 생성 불가
- AI 코드 감사(audit) 전문가가 새 직군으로 등장

</div>
<div class="card orange">

### 방위산업

- 이중·삼중 안전장치 의무화
- AI 생성 코드는 **보안 인증 통과 불가**
- 전문 인력의 역할이 오히려 더 중요해짐

</div>
</div>

---

# 05. 내 일상이 달라졌다

## 현직 개발자가 경험한 AI 도입 전·후

<div class="cards" style="grid-template-columns: repeat(5, 1fr);">
<div class="card">

### 코드 작성

**95% 감소**

설계·기능 명세 후 직접 코딩하는 시간이 거의 사라짐

</div>
<div class="card">

### 문서 작성

**줄었다**

가장 힘든 업무였던 코드 설명 문서를 AI가 초안 작성

</div>
<div class="card yellow">

### 자료 분석

**빨라졌다**

연구개발 실험·결과 정리·통계 분석을 AI로 대체

</div>
<div class="card orange">

### 유튜브 시청

**줄었다**

공식 문서·영상을 AI가 즉시 요약. 데모 영상도 AI 제작

</div>
<div class="card pink">

### 할 일의 양

**늘었다!**

1년 계획이 3개월 만에 끝나서 더 할 일을 찾고 있음

</div>
</div>

<div class="question">생산성이 오를수록, 더 많은 일·더 큰 목표가 생긴다</div>

---

# 06-1. 앞으로의 전망 — 개발자의 삶

<div class="twocol wide-left">
<div class="panel">

10년 전에 10년·20년 후를 상상했을 때와

## 크게 다르지 않다 — 끊임없는 학습

- **끊임없는 학습과 자기 계발** — 새 언어·프레임워크가 나올 때마다 배워왔다 → AI 도구도 마찬가지
- **전문가의 역할은 더 커진다** — 확실한 미래
- 비전문가가 늘어나면서 **전문가의 진입 장벽이 더 높아짐**
- **AI 도구를 다루는 기술 자체가 하나의 능력**

</div>
<div>

> AI는 주니어 개발자를 대체하는 것이 아니라,<br>
> **AI를 쓰는 개발자가**<br>
> **AI를 안 쓰는 개발자를 대체한다**
>
> *— 실리콘밸리 엔지니어링 리더*

</div>
</div>

---

# 06-2. 앞으로의 전망 — 미래의 불확실성

<div class="cards four">
<div class="card yellow">

### 비트코인의 교훈

처음엔 *"암호키 다단계 아냐?"* → 지금은 디지털 금. **양자 컴퓨터가 나오면?** 아무도 모른다

</div>
<div class="card">

### 정치적 영향

기술 도입은 **효용·경제성보다 정치적 영향**이 더 큼. 의료·법률 AI 도입의 가장 큰 걸림돌

</div>
<div class="card orange">

### 트렌드 속도

기술 변화 속도가 **점점 빨라진다**. 특정 분야에 집중하지 않으면 따라잡기 어려움

</div>
<div class="card pink">

### AI 신뢰성

작고 단순한 작업은 OK. **크고 복잡한 영역**에서 AI의 처리 능력은 아직 믿기 어려움

</div>
</div>

---

# 06-3 / 06-4. 나를 위한 결정과 준비

<div class="twocol">
<div class="panel">

### 나를 위한 결정

- 내가 **하고 싶은 것**, 원하는 것
- 무엇을 공부할지는 **내가 결정**하는 것
- 남의 말·뉴스에 휩쓸리지 말 것

</div>
<div class="panel yellow">

### 불확실성에 대응하는 준비

- **학습과 부지런한 정보 수집**
- 현상을 분석·이해하는 **안목과 유연성**
- 공식 문서 + AI 요약 조합 활용
- 작은 프로젝트로 **직접 써보고 느껴라**

</div>
</div>

<div class="question">불확실한 미래일수록, 결정의 주체는 '나' 자신이다</div>

---

<!-- _class: closing -->

# 마무리 — 여러분에게 전하고 싶은 말

<div class="twocol">
<div class="panel">

### 오늘의 핵심

1. AI가 모든 개발자를 대체하진 않는다
2. **전문성 있는 개발자는 더 강해진다**
3. AI는 도구 — 잘 쓰는 자가 이긴다
4. 불확실성 속에서 **내 결정이 중요하다**

</div>
<div>

AI 시대에도 결국 중요한 건<br>
**'사람'과 '전문성'**입니다.

여러분이 무엇을 좋아하고<br>
무엇을 잘하고 싶은지<br>
**그것부터 찾으세요.**

<div class="question">Q & A  |  궁금한 것은 무엇이든 물어보세요!</div>

</div>
</div>
