---
marp: true
theme: default
paginate: true
header: 'AI 시대의 소프트웨어 개발자의 새로운 역할'
footer: '건국대학교 공학박사 | LG전자 CTO Software Platform Lab'
style: |
  section {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 22px;
    background: #ffffff;
    color: #1a1a2e;
  }
  section.title {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #e0e0e0;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  section.title h1 {
    font-size: 48px;
    color: #e94560;
    margin-bottom: 16px;
  }
  section.title h2 {
    font-size: 28px;
    color: #a0c4ff;
    margin-top: 0;
  }
  section.chapter {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.chapter h1 {
    font-size: 52px;
    color: #e94560;
  }
  section.chapter h2 {
    font-size: 30px;
    color: #a0c4ff;
  }
  section.alert {
    background: #fff3cd;
    border-left: 8px solid #ffc107;
  }
  section.alert h2 {
    color: #856404;
  }
  section.insight {
    background: #d1ecf1;
    border-left: 8px solid #0c5460;
  }
  section.insight h2 {
    color: #0c5460;
  }
  h1 { color: #0f3460; font-size: 36px; }
  h2 { color: #e94560; font-size: 28px; }
  h3 { color: #16213e; }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 18px;
  }
  th {
    background: #0f3460;
    color: white;
    padding: 8px 12px;
    text-align: center;
  }
  td {
    padding: 6px 12px;
    border-bottom: 1px solid #ddd;
  }
  tr:nth-child(even) { background: #f2f2f2; }
  blockquote {
    border-left: 4px solid #e94560;
    padding-left: 16px;
    color: #555;
    font-style: italic;
    background: #f9f9f9;
    margin: 8px 0;
    border-radius: 0 4px 4px 0;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .highlight {
    background: #e94560;
    color: white;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: bold;
  }
---

<!-- _class: title -->

# AI 시대의
# 소프트웨어 개발자의
# 새로운 역할

## 고등학생을 위한 AI 특강

**2026년**

---

## 📋 강의 목차 (90분)

| 시간 | 내용 |
|------|------|
| 00:00 ~ 05:00 | 강사 소개 |
| 05:00 ~ 20:00 | 1부: 문제 제기 — AI가 개발자를 대체하나? |
| 20:00 ~ 45:00 | 2부: 현상 분석 — 데이터로 보는 진실 |
| 45:00 ~ 55:00 | ☕ 휴식 |
| 55:00 ~ 75:00 | 3부: 사례 제시 — AI가 못하는 것들 |
| 75:00 ~ 85:00 | 4부: 업무의 변화와 전망 |
| 85:00 ~ 90:00 | Q&A |

---

<!-- _class: chapter -->

# 1부
## 강사 소개

---

# 👨‍💻 강사 소개

**학력**
> 건국대학교 컴퓨터공학과 공학박사

**경력**
> 2012년 ~ LG전자 CTO Software Platform Lab

**주요 기여 프로젝트**

| 프로젝트 | 역할 |
|---------|------|
| webOS Platform | 개발 참여 |
| webOS SDK | 개발 참여 |
| LUPA Platform | 개발 참여 |
| LUPA SDK | 개발 참여 |

---

<!-- _class: chapter -->

# 2부
## AI가 개발자를 대체하는가?

*문제 제기*

---

# 💥 충격적인 뉴스들

**AI 도입 이후 SW 개발자 대규모 해고**

> 정말 AI가 개발자를 대체하고 있을까?

---

# 🔴 Klarna의 사례 (2024)

**AI 어시스턴트 도입 결과**

- 출시 **1개월** 만에 전체 고객서비스 채팅의 **2/3** 처리
- **700명** 규모의 고객서비스 인력 업무 대체

> **CEO 발언 (2024.12)**
> "AI는 인간이 하는 모든 일을 할 수 있다. 1년간 채용을 중단했다."

**그러나...**
> 2025년 5월, AI 과의존으로 인한 **품질 저하**를 인정하고 인력 **재채용** 발표

---

# 🔴 빅테크의 AI 고용 변화

| 기업 | 발언/사건 | 시기 |
|------|-----------|------|
| **Google** CEO Sundar Pichai | "신규 코드의 **25~30%** 이상이 AI로 작성" | 2025.01 |
| **Meta** CEO Zuckerberg | "2025년 AI가 **중간급 엔지니어** 대체할 것" | 2025.01 |
| **Amazon** | AI 도입 이유로 **약 30,000명** 감원 (3개월간) | 2025~2026 |
| **Duolingo** | AI로 콘텐츠 제작 **계약직 인력 대체** 선언 | 2025.04 |

---

# 🔴 바이브 코딩(Vibe Coding)의 등장

**정의**
> OpenAI 공동창립자 **Andrej Karpathy**가 2025년 2월 제시한 개념
> LLM에게 자연어로 지시만 하면 코드를 자동 생성하는 개발 방식

**사회적 반향**
- Collins Dictionary **올해의 단어 (2025)** 선정
- Y Combinator 2025년 Winter 스타트업의 **25%**가 코드베이스의 **95%를 AI로 생성**

**부작용**
> "바이브 코딩 숙취" (Vibe Coding Hangover)
> 시니어 엔지니어들이 AI 생성 코드와 씨름하는 "개발 지옥" 경험 증가
> *(Fast Company, 2025.09)*

---

<!-- _class: alert -->

## 🤔 핵심 질문

# 앞으로 SW 개발자의 수가 줄어들고 일자리도 없어지지 않을까?

---

<!-- _class: chapter -->

# 3부
## 데이터로 보는 진실

*현상 분석*

---

# 📊 미국 SW 개발자 고용 현황

**미국 노동통계국(BLS, 2024년 기준)**

| 지표 | 수치 |
|------|------|
| 총 종사자 수 | **189만 5,500명** |
| 중위 연봉 | **$133,080 / 년** |
| 고용 전망 (2024-2034) | **+15% 성장** 🔺 |
| 연간 채용 예상 | **약 129,200건 / 년** |

> 전체 직종 평균 대비 **훨씬 빠른 성장** 전망!

*출처: U.S. Bureau of Labor Statistics, 2025*

---

# 🌏 전 세계 SW 개발자 규모

**GitHub Octoverse 2025 기준**

| 지표 | 수치 |
|------|------|
| GitHub 전체 개발자 | **1억 8천만 명 이상** |
| 2025년 신규 가입 | **3,600만 명** (매 초 1명!) |
| AI 관련 저장소 | **430만 개 이상** (2년 만에 2배) |
| LLM SDK 사용 저장소 | **113만 개 이상** (+178% YoY) |
| 신규 개발자 Copilot 사용률 | 첫 주 내 **약 80%** 사용 |

---

# 🇰🇷 한국 SW 개발자 현황

**국내 ICT 인력 현황 (ITSTAT, 2024년 잠정)**

| 지표 | 수치 |
|------|------|
| ICT 산업 전체 인력 | **220만 811명** |
| SW 산업 종사자 (추정) | **약 100만 명 이상** |
| 연평균 SW 인력 증가율 | **약 4~5% 수준** |

**주요 특징**
- 삼성전자, LG, 카카오, 네이버 등 대기업 중심 SW 인력 집중
- AI·클라우드·임베디드 분야 신규 수요 지속 증가
- 2025년 이후 AI 관련 채용 공고 전년 대비 급증세

> *출처: ITSTAT ICT통계포털 (www.itstat.go.kr), 2024년 잠정치*

---

# 💻 AI 코딩에서 많이 쓰는 언어

**GitHub Octoverse 2025 (2025년 10월 발표)**

| 언어 | GitHub 순위 | 성장률 (YoY) | 특징 |
|------|-------------|-------------|------|
| **TypeScript** | 🥇 1위 | +66% | AI 보조 코딩의 타입 안전성 요구 |
| **Python** | 🥈 2위 | +48% | AI/ML 표준 언어 |
| **JavaScript** | 🥉 3위 | +24% | TypeScript로 전환 가속 |

**AI 관련 저장소 언어별 현황**

| 언어 | 저장소 수 | 증가율 |
|------|-----------|--------|
| Python | 582,000개 | +50.7% |
| JavaScript | 88,000개 | +24.8% |
| TypeScript | 86,000개 | +77.9% |

---

# 🚀 AI가 높이는 개발자 생산성

**GitHub Copilot × Accenture 연구 (2024년)**

| 지표 | 변화 |
|------|------|
| Pull Request 수 | **+8.69%** 증가 |
| PR 병합률 (코드 품질) | **+15%** 향상 |
| 빌드 성공률 | **+84%** 증가 |
| 업무 만족도 향상 | **90%** 응답 |
| 코딩이 즐거워짐 | **95%** 응답 |

---

<!-- _class: insight -->

## ✅ 현상 분석 결론

**AI의 발전에 직접 영향받는 인력은 제한적**

> 전체 고용은 오히려 **성장 예측** (미국 기준 +15%, 2034년까지)

**새로운 SW 시장이 열리고 있다**

> AI 에이전트 · LLM 인프라 · 엣지 AI · 자율주행 · SDV

---

<!-- _class: chapter -->

# 4부
## AI가 못하는 것들

*사례 제시*

---

# 🔧 임베디드 소프트웨어 — AI의 한계

**LG전자 임베디드 개발 현장의 솔직한 이야기**

- AI 도입을 **환영**하지만, 생각만큼 **활용이 어려움**

**왜 어려울까?**

| 이유 | 설명 |
|------|------|
| 비공개 코드 | 외부에 공개되지 않은 사내 코드 |
| 하드웨어 의존성 | 물리적 개입 없이는 테스트 불가 |
| 할루시네이션 | AI가 존재하지 않는 API를 있다고 생성 |
| 실시간성 | 타이밍이 중요한 RTOS 환경 |

> "우리가 AI의 **인간 하네스**가 될 수도 있다" — 현장 개발자의 농담

---

# 🚗 임베디드 AI 도입 사례

| 사례 | 내용 |
|------|------|
| **Tesla FSD v12** | 30만 줄 C++ 코드 → 엔드투엔드 신경망으로 대체, 2026년 무인 로보택시 운행 |
| **Edge AI** | 기기 자체에서 AI 추론 (지연시간 최소화, 프라이버시 보호) |
| **NVIDIA Jetson / DRIVE** | 자동차·로봇·드론용 AI 추론 전용 플랫폼 |
| **자동차 SDV** | 현대·기아, BMW 등 OTA 업데이트·AI 운전 보조 구현 |
| **LG webOS AI ThinQ** | TV·냉장고에 음성인식·에너지 최적화 탑재 |

> **시사점**: 임베디드 AI는 "코딩 보조"가 아닌 **제품 자체에 AI 탑재**하는 방향으로 발전 중

---

# 🔐 AI 코드는 안전한가?

**AI 생성 코드의 보안 문제**

| 연구 | 결과 |
|------|------|
| **CodeRabbit (2025.12)** | AI 코드가 인간 코드보다 주요 문제 **1.7배**, 보안 취약점 **2.74배** 많음 |
| **Veracode (2025.10)** | LLM은 3년간 기능 향상됐지만 **보안성은 전혀 개선 안 됨** |
| **GitHub CodeQL (2025)** | Broken Access Control 취약점 **+172% YoY** 증가 |

**실제 사고**
- **Lovable** (2025.05): 1,645개 웹앱 중 **170개에서 개인정보 노출** 발견
- **Orchids** (2026.02): AI 코딩 플랫폼 보안 결함으로 BBC 기자 **실시간 해킹 피해**

---

# 💰 보안이 중요한 분야는 AI를 더 신중하게

**금융 분야**
> AI 코드 도입 → 보안 검증 필요성 **증가**
> AI가 만든 코드도 **인간 전문가의 검토** 필수

**방위산업**
> 2중, 3중 안전장치 필요 → 검증 부담 **오히려 증가**
> AI 생산성 향상 = 동시에 **검증 업무량 증가**

> **결론**: AI 발전 = 새로운 전문가 수요 창출

---

<!-- _class: chapter -->

# 5부
## 실제 업무는 어떻게 변했나?

*현장 경험담*

---

# 📝 업무의 변화 사례

**1. 문서 작성이 쉬워졌다**
> 개발자의 가장 힘든 업무 = 코드 작성이 아니라 **코드 설명 문서**
> → AI가 초안 작성, 개발자가 검토·수정

**2. 자료 분석이 빨라졌다**
> 실험 결과 정리, 데이터 분석 보고서
> → AI로 1시간 → 10분으로 단축

**3. 유튜브 시청 시간이 줄었다**
> 새 기술 학습: 공식 문서 + 유튜브 → **AI에게 바로 질문**
> 동영상 요약도 AI, 데모 영상도 AI로 제작

**4. 단점: 할 일이 점점 더 많아진다**
> 1년 계획이 3개월 만에 끝남 → 더 많은 프로젝트 진행

---

<!-- _class: chapter -->

# 6부
## 앞으로의 전망

*여러분의 미래*

---

# 🔮 개발자의 미래

**확실한 것들**

> 1. **끊임없는 학습**은 10년 전에도, 지금도, 미래에도 필수
> 2. **전문가의 역할**은 AI 시대에 오히려 더 커진다
> 3. AI는 **도구**다 — 망치를 잘 쓰는 목수가 더 좋은 가구를 만든다

**미래에 유망한 분야**

| 분야 | 이유 |
|------|------|
| AI 에이전트 개발 | 새로운 SW 패러다임 |
| 임베디드 + AI | 하드웨어에 AI 탑재 증가 |
| 보안·검증 | AI 코드의 안전성 확인 필수 |
| LLM 인프라 | AI 서비스 기반 구축 |
| 엣지 AI | 기기 자체에서 AI 처리 |

---

# ❓ 미래는 불확실하다

**비트코인의 교훈**
> 처음 등장했을 때: "암호키를 사고파는 다단계인가?"
> 현재: 디지털 자산의 표준

**기술의 도입은 예측이 어렵다**
> 효용성과 경제적 가치보다도 **정치·사회적 요인**이 더 큰 영향을 미친다

**양자 컴퓨터와 비트코인**
> 양자 컴퓨터가 개발되면 비트코인 가치는 올라갈까, 떨어질까?

---

<!-- _class: insight -->

# 🎯 여러분에게 드리는 조언

## 나를 위한 결정

> 1. **내가 하고 싶은 것**을 찾아라
> 2. **무엇을 공부할지**는 남이 아닌 내가 결정한다

## 불확실성에 대응하는 방법

> - **끊임없이 배우기**: 기술은 계속 변한다
> - **부지런한 정보 수집**: 트렌드를 놓치지 않는다
> - **깊이 있는 전문성**: AI가 대체하기 어렵다
> - **호기심을 잃지 않기**: 새 기술을 두려워하지 않는다

---

# 📚 핵심 정리

| 오해 | 진실 |
|------|------|
| AI가 개발자를 대체한다 | **일부 업무** 대체, 전체 고용은 성장 중 |
| 코딩만 잘하면 된다 | **문제 해결 능력**이 더 중요해진다 |
| AI 코드는 안전하다 | 보안 취약점이 인간 코드의 **2.74배** |
| 개발자 수가 줄어든다 | 전 세계 개발자는 **매 초 1명씩** 증가 중 |
| 임베디드는 AI와 무관하다 | 제품 자체에 AI 탑재 — **가장 뜨거운 분야** |

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
| GitHub Octoverse 2025 | GitHub Blog (2025.10) |
| GitHub Copilot 기업 연구 | GitHub × Accenture (2024) |
| 바이브 코딩 | Wikipedia / Collins Dictionary (2025) |
| AI 코드 보안 취약점 | CodeRabbit (2025.12) / Veracode (2025.10) |
| Lovable 플랫폼 보안 사고 | Semafor (2025.05) |
| BBC 해킹 피해 | BBC News (2026.02) |
| Tesla FSD | Wikipedia: Tesla Autopilot |
| 한국 ICT 인력 현황 | ITSTAT ICT통계포털 (2024년 잠정) |
