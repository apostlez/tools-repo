---
marp: true
theme: default
paginate: true
header: 'AI 시대의 소프트웨어 개발자의 새로운 역할'
footer: '건국대학교 공학박사 | LG전자 CTO Software Platform Lab'
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
  section {
    font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif;
    font-size: 22px;
    background: #fafbfc;
    color: #1e293b;
    padding: 40px 60px;
  }
  /* ── 타이틀 슬라이드 ── */
  section.title {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #2563eb 100%);
    color: #e2e8f0;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 60px;
  }
  section.title h1 {
    font-size: 46px;
    font-weight: 900;
    color: #38bdf8;
    line-height: 1.3;
    margin-bottom: 12px;
    text-shadow: 0 2px 12px rgba(56,189,248,0.3);
  }
  section.title h2 {
    font-size: 26px;
    font-weight: 400;
    color: #94a3b8;
    margin-top: 4px;
  }
  section.title p { color: #cbd5e1; font-size: 20px; }
  /* ── 챕터 구분 슬라이드 ── */
  section.chapter {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.chapter h1 {
    font-size: 56px;
    font-weight: 900;
    color: #38bdf8;
    margin-bottom: 8px;
  }
  section.chapter h2 {
    font-size: 28px;
    font-weight: 400;
    color: #e2e8f0;
  }
  section.chapter p { color: #94a3b8; font-size: 18px; }
  /* ── 경고/알림 슬라이드 ── */
  section.alert {
    background: #fffbeb;
    border-left: 6px solid #f59e0b;
  }
  section.alert h2 { color: #92400e; }
  /* ── 인사이트 슬라이드 ── */
  section.insight {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0f9ff 100%);
    border-left: 6px solid #059669;
  }
  section.insight h2 { color: #065f46; }
  /* ── 일반 스타일 ── */
  h1 { color: #0f172a; font-size: 34px; font-weight: 700; margin-bottom: 16px; }
  h2 { color: #2563eb; font-size: 26px; font-weight: 600; }
  h3 { color: #334155; font-size: 22px; }
  strong { color: #dc2626; }
  /* ── 테이블 ── */
  table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 17px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }
  th {
    background: #1e3a5f;
    color: #ffffff;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 16px;
  }
  td {
    padding: 8px 14px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }
  tr:nth-child(even) { background: #f1f5f9; }
  tr:hover { background: #e0f2fe; }
  /* ── 인용 ── */
  blockquote {
    border-left: 4px solid #2563eb;
    padding: 12px 20px;
    color: #475569;
    font-style: normal;
    background: #f8fafc;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    font-size: 20px;
  }
  blockquote strong { color: #1e40af; }
  /* ── 리스트 ── */
  ul, ol { line-height: 1.7; }
  li { margin-bottom: 4px; }
  /* ── 유틸리티 ── */
  .small { font-size: 14px; color: #94a3b8; }
---

<!-- _class: title -->

# AI 시대의
# 소프트웨어 개발자의
# 새로운 역할

## 고등학생을 위한 AI 특강

**2026년 5월**

---

# 📋 강의 순서 (90분)

| 시간 | 파트 | 내용 |
|:----:|:----:|------|
| 00–05 | 인사 | 강사 소개 |
| 05–20 | **1부** | 문제 제기 — AI가 개발자를 대체하나? |
| 20–45 | **2부** | 현상 분석 — 데이터로 보는 진실 |
| 45–55 | ☕ | 쉬는 시간 |
| 55–75 | **3부** | 사례 — AI가 잘 못하는 영역 |
| 75–85 | **4부** | 업무 변화와 미래 전망 |
| 85–90 | Q&A | 질의응답 |

---

# 👨‍💻 강사 소개

**학력**
> 건국대학교 컴퓨터공학과 공학박사

**경력**
> 2012년 ~ 현재 · LG전자 CTO Software Platform Lab

| 프로젝트 | 역할 |
|---------|------|
| webOS Platform | 개발 |
| webOS SDK | 개발 |
| LUPA Platform | 개발 |
| LUPA SDK | 개발 |

---

<!-- _class: chapter -->

# 1부
## AI가 개발자를 대체하는가?

*문제 제기*

---

# 📰 빅테크 CEO들의 선언 (2025)

| 기업 | 누가 | 무슨 말을? | 시기 |
|:----:|------|-----------|:----:|
| Google | CEO Sundar Pichai | "신규 코드의 **25~30%** 이상이 AI 작성" | 01월 |
| Meta | CEO Zuckerberg | "AI가 **중간급 엔지니어** 대체할 것" | 01월 |
| Shopify | CEO Tobi Lütke | "**AI가 못하는 걸 증명**해야 채용 가능" | 04월 |
| Anthropic | CEO Dario Amodei | 기업 3/4이 AI에 **전체 업무 위임** | 09월 |
| Gartner | 리서치 보고서 | 2030년까지 개발자 **3명 중 1명** 실직 전망 | 09월 |

> Amazon은 2025~2026년 사이 AI·자동화를 이유로 **약 30,000명** 감원

---

# 💻 바이브 코딩(Vibe Coding)의 등장

> OpenAI 공동창립자 **Andrej Karpathy**가 2025년 2월 제안한 개념
> "코드를 읽지 않고, 자연어로 지시만 하면 AI가 코드를 생성"

| 지표 | 내용 |
|------|------|
| Collins Dictionary | **2025 올해의 단어** 선정 |
| Y Combinator | 2025 Winter 배치 스타트업 **25%**가 코드의 95%를 AI로 생성 |
| Cursor (Anysphere) | 기업가치 **$293억** → xAI **$600억** 인수 논의 (2026.04) |
| OpenAI | 바이브 코딩 스타트업 Windsurf **$30억** 인수 (2025.05) |

---

# ⚠️ 바이브 코딩의 어두운 면

| 사건 | 내용 | 시기 |
|------|------|:----:|
| Replit DB 삭제 | AI 에이전트가 **프로덕션 DB 삭제** 후 거짓 보고 | 2025.07 |
| METR 연구 | AI 사용 시 오히려 **19% 느려짐** (본인은 빨라졌다고 착각) | 2025.07 |
| GitClear | 코드 리팩토링 25%→**10% 미만**, 코드 중복 **4배** 증가 | 2025 |
| 바이브 코딩 숙취 | "개발 지옥(development hell)" — 시니어 엔지니어들 | 2025.09 |
| 오픈소스 위협 | LLM이 대형 라이브러리에만 편향 → 신규 도구 발견 감소 | 2026.01 |

> Linus Torvalds: 바이브 코딩은 사용하지만, **핵심 커널 코드가 아닌 부수적 도구에만** 활용 (2026.01)

---

# 🗑️ AI 슬롭(AI Slop) — 저품질 콘텐츠의 범람

> **"Slop"** = Merriam-Webster & 미국 방언학회 **2025 올해의 단어** 동시 선정

| 플랫폼 | 문제 | 출처 |
|--------|------|------|
| **Steam** | 출시 게임의 **20%**가 AI 공시 포함 — "AI 쇼블웨어" | 2025.07 |
| **Google Play** | Angry Birds AI 이미지 비판 → **삭제** | 2025 |
| **Lovable** | 1,645개 앱 중 **170개**에서 개인정보 노출 | 2025.05 |
| **한국** | AI 슬롭 콘텐츠 소비 **세계 1위** | 2025.12 |

---

<!-- _class: alert -->

## 🤔 핵심 질문

# 앞으로 SW 개발자의 수가 줄어들고
# 일자리도 없어지지 않을까?

---

<!-- _class: chapter -->

# 2부
## 데이터로 보는 진실

*현상 분석*

---

# 📊 미국 SW 개발자 고용 현황

**미국 노동통계국 (BLS, 2024년 기준)**

| 지표 | 수치 |
|------|-----:|
| 총 종사자 수 | **1,895,500명** |
| 중위 연봉 | **$133,080 / 년** |
| 고용 전망 (2024–2034) | **+15% 성장** 📈 |
| 10년 신규 고용 | **+287,900명** |
| 연간 채용 예상 | **~129,200건 / 년** |

> 전체 직종 평균 대비 **훨씬 빠른 성장** 전망

---

# 🌍 전 세계 SW 개발자 규모

**GitHub Octoverse 2025 (2025.10 발표)**

| 지표 | 수치 | 변화 |
|------|-----:|-----:|
| GitHub 전체 개발자 | **1.5억 명 이상** | — |
| 2025년 신규 가입 | **3,600만 명** | 매 초 1명! |
| AI 관련 저장소 | **430만 개** | 2년 새 2배 |
| LLM SDK 사용 저장소 | **113만 개** | +178% YoY |
| 신규 개발자 Copilot 사용 | **~80%** | 첫 주 내 |

> 개발자 수는 **감소하지 않고 오히려 폭증** 중

---

# 🇰🇷 한국 SW 개발자 현황

**국내 ICT 인력 (ITSTAT, 2024 잠정치)**

| 지표 | 수치 |
|------|-----:|
| ICT 산업 전체 인력 | **220만 811명** |
| SW 산업 종사자 (추정) | **약 100만 명 이상** |
| 연평균 성장률 | **4~5%** (최근 5년) |
| GitHub 기여자 글로벌 순위 | **7위** (기여량 6위) |

**특징**
- 삼성·LG·카카오·네이버 등 대기업 중심 SW 인력 집중
- AI·클라우드·임베디드 분야 신규 수요 **지속 증가**
- 2025년 이후 AI 관련 채용 공고 **전년 대비 급증세**

---

# 💻 AI 코딩에서 많이 쓰는 언어

**GitHub Octoverse 2025**

| 순위 | 언어 | 성장률 (YoY) | 특징 |
|:----:|------|:-----------:|------|
| 🥇 | **TypeScript** | +66% | AI 보조 코딩의 타입 안전성 |
| 🥈 | **Python** | +48% | AI/ML 표준 언어 |
| 🥉 | **JavaScript** | +24% | TypeScript로 전환 가속 |

**AI 관련 저장소 언어별**

| 언어 | 저장소 수 | 증가율 |
|------|----------:|------:|
| Python | 582,000개 | +50.7% |
| TypeScript | 86,000개 | +77.9% |
| JavaScript | 88,000개 | +24.8% |

---

# 🚀 AI가 높이는 개발자 생산성

**GitHub Copilot × Accenture 연구 (2024)**

| 지표 | 변화 |
|------|-----:|
| Pull Request 수 | **+8.69%** |
| PR 병합률 (코드 품질) | **+15%** |
| 빌드 성공률 | **+84%** |
| 업무 만족도 향상 | **90%** 응답 |
| 코딩이 즐거워짐 | **95%** 응답 |

**GitHub 개발자 설문 (2024)**
- **97%** 이상이 AI 코딩 도구 사용 경험
- 절약된 시간 → **설계·협업·학습**에 재투자

---

<!-- _class: insight -->

## ✅ 2부 핵심 정리

**일자리가 사라지는가?**
> 미국 BLS: 2034년까지 **+15% 성장** 전망
> GitHub: 매 초 1명씩 신규 개발자 가입

**AI가 바꾸는 것은?**
> 단순 코딩 → **AI 도구 활용 + 전문적 설계·검증** 중심으로 역할 전환
> 새로운 시장: AI 에이전트 · LLM 인프라 · Edge AI · SDV

---

<!-- _class: chapter -->

# 3부
## AI가 잘 못하는 영역

*사례 제시*

---

# 🔧 임베디드 소프트웨어 — AI의 한계

**LG전자 임베디드 개발 현장의 이야기**

| 한계 요인 | 설명 |
|----------|------|
| 비공개 코드 | 외부에 없는 사내 코드 → AI 학습 불가 |
| 하드웨어 의존 | 물리적 개입 없이 테스트 불가 |
| 할루시네이션 | 존재하지 않는 API를 생성 |
| 실시간성 | 타이밍이 중요한 RTOS 환경 |
| 안전 규격 | AUTOSAR, DO-178C 등 인증 부담 |

> "우리가 AI의 **인간 하네스(harness)**가 될 수도 있다" — 현장 개발자

---

# 🚗 하지만 임베디드 × AI는 가장 뜨거운 분야

| 사례 | 내용 |
|------|------|
| **Tesla FSD v12** | 30만 줄 C++ → **엔드투엔드 신경망**으로 대체 |
| **Edge AI** | 기기 자체에서 AI 추론 (지연시간↓, 프라이버시↑) |
| **NVIDIA Jetson/DRIVE** | 자동차·로봇·드론용 AI 추론 플랫폼 |
| **SDV** | 현대·기아, BMW — OTA 업데이트 + AI 보조 |
| **LG webOS AI ThinQ** | TV·냉장고에 음성인식·에너지 최적화 탑재 |

> 임베디드 AI는 "코딩 보조"가 아닌 **제품 자체에 AI를 탑재**하는 방향

---

# 🔐 AI 코드는 안전한가?

**AI 생성 코드의 보안 연구 결과**

| 연구 | 결과 | 시기 |
|------|------|:----:|
| **CodeRabbit** | AI 코드 주요 문제 **1.7배**, 보안 취약점 **2.74배** | 2025.12 |
| **Veracode** | 3년간 기능 향상, **보안성은 미개선** | 2025.10 |
| **GitHub CodeQL** | Broken Access Control **+172%** YoY | 2025 |

**실제 해킹 사고**

| 사건 | 내용 |
|------|------|
| **Lovable** (2025.05) | 1,645개 앱 중 **170개**에서 개인정보 노출 |
| **Orchids** (2026.02) | BBC 기자 대상 **실시간 해킹 시연** 성공 |

---

# 💰 AI가 대체하기 어려운 분야

**보안·금융·방위산업**

| 분야 | AI 도입 상황 | AI의 한계 |
|------|-------------|----------|
| **금융** | 코드 생성은 가능 | 보안 검증 → **전문가 필수** |
| **방위산업** | 2중 3중 안전장치 | 검증 부담 **오히려 증가** |
| **의료기기** | IEC 62304 규격 | AI 코드 인증 **미확립** |
| **항공** | DO-178C 규격 | 모든 코드 경로 **증명 필요** |

> AI 생산성 향상 = 동시에 **검증 업무량 증가**
> → 보안·검증 전문가 수요 **급증**

---

<!-- _class: chapter -->

# 4부
## 업무의 변화와 미래

*현장 경험담 + 전망*

---

# 📝 실제 업무는 어떻게 변했나?

| 변화 | Before | After (AI 도입) |
|------|--------|----------------|
| **코드 작성** | 직접 한 줄씩 | AI 초안 → 검토·수정 |
| **문서 작성** | 가장 힘든 업무 | AI 초안 생성 → 10분 완료 |
| **자료 분석** | 1시간 이상 | AI로 **10분**에 처리 |
| **기술 학습** | 공식문서 + 유튜브 | AI에게 바로 질문 |
| **데모 영상** | 직접 촬영·편집 | AI로 자동 생성 |

**단점**
> 생산성이 올라가니 **할 일이 더 많아졌다**
> 1년 계획을 세웠는데 **3개월**에 끝남 → 더 많은 프로젝트 진행

---

# 🔮 개발자의 미래

**확실한 것들**

> 1. **끊임없는 학습**은 10년 전에도, 지금도, 미래에도 필수
> 2. **전문가의 역할**은 AI 시대에 오히려 **더 커진다**
> 3. AI는 **도구**다 — 망치를 잘 쓰는 목수가 더 좋은 가구를 만든다

**미래에 유망한 분야**

| 분야 | 이유 |
|------|------|
| AI 에이전트 개발 | 새로운 SW 패러다임 |
| 임베디드 + AI | 제품에 AI 탑재 증가 |
| 보안·검증 | AI 코드 안전성 확인 필수 |
| LLM 인프라 | AI 서비스 기반 구축 |
| Edge AI | 기기 자체에서 AI 처리 |

---

# ❓ 미래는 불확실하다

**비트코인의 교훈**
> 처음: "암호키를 사고파는 다단계?"
> 현재: **디지털 자산의 표준**

**기술 도입은 예측이 어렵다**
> 효용성·경제적 가치보다 **정치·사회적 요인**이 더 큰 영향
> 예: 의료·법률 분야의 AI 도입 → 정치적 요인이 최대 걸림돌

**양자 컴퓨터와 비트코인**
> 양자 컴퓨터가 개발되면 비트코인 가치는 올라갈까, 떨어질까?

**AI 신뢰성 문제**
> 작고 단순한 문제 → OK | 크고 복잡한 문제 → **아직 믿기 어렵다**

---

# 📚 핵심 정리

| 오해 | 진실 |
|------|------|
| AI가 개발자를 대체한다 | **일부 업무** 대체, 전체 고용은 **+15% 성장** 중 |
| 코딩만 잘하면 된다 | **문제 해결·설계·검증** 능력이 더 중요 |
| AI 코드는 안전하다 | 보안 취약점이 인간 코드의 **2.74배** |
| 개발자 수가 줄어든다 | GitHub에서 **매 초 1명** 신규 가입 |
| 임베디드는 AI와 무관 | 제품 자체에 AI 탑재 — **가장 뜨거운 분야** |
| 바이브 코딩이면 충분 | 기술 부채 **4배**, 보안 사고 **빈발** |

---

<!-- _class: insight -->

# 🎯 여러분에게 드리는 조언

## 나를 위한 결정

> 1. **내가 하고 싶은 것**을 찾아라
> 2. **무엇을 공부할지**는 남이 아닌 내가 결정한다

## 불확실성에 대응하는 방법

> - **끊임없이 배우기** — 기술은 계속 변한다
> - **부지런한 정보 수집** — 트렌드를 놓치지 않는다
> - **깊이 있는 전문성** — AI가 대체하기 어렵다
> - **호기심을 잃지 않기** — 새 기술을 두려워하지 않는다

---

<!-- _class: title -->

# 감사합니다! 🙏

## Q & A

**강사 정보**
건국대학교 컴퓨터공학과 공학박사
LG전자 CTO Software Platform Lab

---

# 📖 참고 자료

| 주제 | 출처 |
|------|------|
| 미국 SW 개발자 고용 통계 | U.S. Bureau of Labor Statistics (2025) |
| 전 세계 개발자 현황 | GitHub Octoverse 2025 (2025.10) |
| AI Copilot 기업 연구 | GitHub × Accenture (2024) |
| 바이브 코딩 정의 & 문제 | Wikipedia / Collins Dictionary (2025) |
| AI 코드 보안 취약점 | CodeRabbit (2025.12) / Veracode (2025.10) |
| AI 생태계 보안 사고 | Semafor (2025.05) / BBC News (2026.02) |
| 개발자 1/3 실직 전망 | Gartner (2025.09) |
| Shopify AI 채용 정책 | CNBC (2025.04) |
| AI 슬롭 현상 | Wikipedia: AI slop / Korea Herald (2025.12) |
| 한국 ICT 인력 현황 | ITSTAT ICT통계포털 (2024 잠정) |
| Tesla FSD | Wikipedia: Tesla Autopilot |
| Cursor (Anysphere) | Wikipedia: Anysphere |
