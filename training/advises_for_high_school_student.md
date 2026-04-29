# 주제
AI 시대의 소프트웨어 개발자의 새로운 역할

---

## 1. 강사 소개

건국대학교 컴퓨터공학과 공학박사
2012년 ~ LG전자 CTO Software Platform lab

**기여**
- webOS platform 개발
- webOS SDK 개발
- LUPA platform 개발
- LUPA SDK 개발

---

## 2. 문제 제기

### 2-1. 최근 SW 개발자 처우 관련 뉴스

#### AI 도입 이후 SW 개발자 대규모 해고

- **Klarna (2024)**: AI 어시스턴트가 700명 규모의 고객서비스 인력의 업무를 대체. 출시 1개월 만에 전체 고객서비스 채팅의 2/3를 처리.
  - 출처: [Klarna AI assistant handles two-thirds of customer service chats in its first month (Klarna, 2024.02)](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/)
  - 추가: [Klarna says its OpenAI virtual assistant does the work of 700 humans (Fast Company, 2024.02)](https://www.fastcompany.com/91039401/klarna-ai-virtual-assistant-does-the-work-of-700-humans-after-layoffs)

- **Klarna CEO (2024.12)**: "AI는 인간이 하는 모든 일을 할 수 있다. 1년간 채용을 중단했다." (이후 2025년 5월, AI 과의존으로 품질 저하를 인정하고 인력 재채용 발표)
  - 출처: [Klarna CEO says the company stopped hiring a year ago because AI 'can already do all of the jobs' (Business Insider, 2024.12)](https://www.businessinsider.com/klarna-ceo-sebastian-siemiatkowski-ai-jobs-2024-12)

- **Duolingo (2025.04)**: AI를 활용해 콘텐츠 제작 계약직 인력을 대체하겠다고 선언.

#### 빅테크 기업의 AI로 인한 고용 변화

- **Google CEO Sundar Pichai (2025.01)**: "현재 Google 전체 신규 코드의 **25~30% 이상이 AI로 작성**되고 있다"고 공식 발표. AI 생산성 향상으로 인력 효율화 가속화.
  - 출처: [Google CEO Sundar Pichai says AI now writes more than 30% of its code (TechCrunch, 2025.01)](https://techcrunch.com/2025/01/16/google-ceo-sundar-pichai-says-ai-now-writes-more-than-30-of-its-code/)

- **Meta CEO Mark Zuckerberg (2025.01)**: "2025년에 AI가 **중간급(mid-level) 엔지니어를 대체**할 것"이라며 Meta가 AI를 일부 엔지니어 포지션을 대체하는 데 활용할 것이라고 공언.
  - 출처: [Mark Zuckerberg says Meta will replace some engineers with AI (TechCrunch, 2025.01)](https://techcrunch.com/2025/01/14/mark-zuckerberg-says-meta-will-replace-some-engineers-with-ai/)

- **Amazon (2025~2026)**: AI 기술 도입 및 업무 자동화를 이유로 **2025년 10월 약 14,000명**, **2026년 1월 약 16,000명**을 추가로 해고. 3개월 만에 총 약 30,000명 규모의 감원. Amazon의 역사상 두 번째로 큰 대규모 정리해고.
  - 출처: [Amazon (company) - Wikipedia](https://en.wikipedia.org/wiki/Amazon_(company)) / Reuters, WSJ 보도

#### 바이브 코딩(Vibe Coding)과 앱 스토어 생태계

- **바이브 코딩 정의**: OpenAI 공동창립자 Andrej Karpathy가 2025년 2월 처음 제시한 개념. LLM에게 자연어로 지시만 하면 코드를 자동 생성하는 개발 방식. 코드를 직접 읽거나 이해하지 않고도 앱을 만들 수 있음.
  - 출처: [Vibe coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)

- **Collins Dictionary 올해의 단어(2025)**: "vibe coding"이 2025년 올해의 단어로 선정됨.
  - 출처: ['Vibe coding' named word of the year by Collins Dictionary (BBC News, 2025.11)](https://www.bbc.com/news/articles/cpd2y053nleo)

- **앱 생태계 문제**: Y Combinator의 2025년 Winter 배치 스타트업의 25%가 코드베이스의 95%를 AI로 생성. 보안 취약점, 저품질 앱 급증 문제 제기됨.
  - 출처: [A quarter of startups in YC's current cohort have codebases that are almost entirely AI-generated (TechCrunch, 2025.03)](https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/)

- **"바이브 코딩 숙취"(2025.09)**: Fast Company가 "vibe coding hangover"를 보도. 시니어 엔지니어들이 AI 생성 코드와 씨름하는 "개발 지옥" 경험 증가.
  - 출처: [The vibe coding hangover is upon us (Fast Company, 2025.09)](https://www.fastcompany.com/91398622/the-vibe-coding-hangover-is-upon-us)

### 2-2. 앞으로 SW 개발자의 수가 줄어들고 일자리도 없어지지 않을까?

---

## 3. 문제의 현상 분석

### 3-1. SW 개발자 직군 및 역할 분류

미국 노동통계국(BLS, 2024년 기준) 데이터:
- **총 종사자 수**: 1,895,500명 (소프트웨어 개발자 + QA 테스터 포함)
- **중위 연봉**: $133,080/년 (소프트웨어 개발자 기준)
- **고용 전망(2024-2034)**: **15% 성장** — 전체 직종 평균 대비 훨씬 빠른 성장
- **연간 채용 예상**: 약 129,200건/년
- 출처: [Software Developers, Quality Assurance Analysts, and Testers (U.S. Bureau of Labor Statistics, 2025)](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm)

### 3-2. AI를 활용한 코딩이 사용하는 언어 통계

GitHub Octoverse 2025 보고서 (2025년 10월 발표):
- **TypeScript**: 2025년 GitHub 1위 언어로 등극 (+66% YoY). AI 보조 코딩에서 타입 안전성이 중요해지며 급성장.
- **Python**: GitHub 2위 (+48% YoY). AI/ML 분야의 표준 언어. AI 관련 저장소의 절반(582,196개)이 Python 사용.
- **JavaScript**: 3위 (+24% YoY). TypeScript로의 전환 가속화.
- **AI 관련 저장소에서 언어별 현황**:
  - Python: 582,000개 저장소 (+50.7% YoY)
  - TypeScript: 86,000개 (+77.9% YoY)
  - JavaScript: 88,000개 (+24.8% YoY)
- 출처: [GitHub Octoverse 2025 - A new developer joins GitHub every second as AI leads TypeScript to #1](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

### 3-3. 전 세계 SW 개발자 규모

GitHub Octoverse 2025 기준:
- **GitHub 전체 개발자**: 1억 8천만 명 이상 (2025년 기준)
- **2025년 신규 가입**: 3,600만 명 이상 (매 초 1명씩 가입)
- **AI 관련 저장소**: 4.3백만 개 이상 (2년 만에 거의 2배)
- **LLM SDK 사용 저장소**: 113만 개 이상 (+178% YoY)
- **신규 개발자의 AI 도구 활용**: 신규 GitHub 사용자의 약 80%가 첫 주 내에 Copilot 사용
- 출처: [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

### 3-4. AI 생산성 향상 통계

GitHub Copilot × Accenture 연구 (2024년):
- GitHub Copilot 도입 후 코드 Pull Request **8.69% 증가**
- PR 병합률(코드 품질 지표) **15% 향상**
- 빌드 성공률 **84% 증가**
- 개발자의 **90%가 업무 만족도 향상**, 95%가 코딩이 즐거워졌다고 응답
- 출처: [Research: Quantifying GitHub Copilot's impact in the enterprise with Accenture (GitHub Blog, 2024)](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/)

### 3-5. 현상 분석 결론

- AI의 발전에 직접적으로 영향을 받는 인력은 제한적이며, 전체 고용은 오히려 **성장 예측**
- AI 기술의 발전에 따라 새로운 SW 시장이 열릴 가능성 제시 (AI 에이전트, LLM 인프라, 에지 AI 등)

---

## 4. 사례 제시

### 4-1. 임베디드 소프트웨어

- LG전자에 주로 종사하는 임베디드 개발자들은 오히려 AI 도입을 환영하나 생각만큼 활용하지 못함.
- 외부에 공개되지 않고 하드웨어에 의존적인 부분이 많고 물리적인 개입이 필요한 임베디드 특성 상, 할루시네이션이 많아 업무 효율이 떨어짐
- AI 의 발전에 따라 '인간 하네스' 가 될 수 있다는 농담도 할 수 있음

#### 임베디드 분야 AI 도입 사례

- **Tesla FSD (Full Self-Driving)**: 임베디드 AI의 대표적 사례. 차량에 탑재된 전용 SoC(HW3→HW4)에서 신경망이 카메라 영상을 실시간 처리하여 자율주행 수행. FSD v12부터는 기존 30만 줄 이상의 C++ 규칙 기반 코드를 제거하고 **엔드투엔드 신경망**으로 대체. 2026년 4월 기준 오스틴에서 완전 무인 로보택시 운행 중.
  - 출처: [Tesla Autopilot - Wikipedia](https://en.wikipedia.org/wiki/Tesla_Autopilot)

- **Edge AI (엣지 컴퓨팅 + AI)**: 클라우드가 아닌 기기 자체에서 AI 추론을 수행하는 패러다임. 자율주행, 스마트 팩토리, IoT 센서 등에서 **지연시간(latency) 최소화**와 **데이터 프라이버시 보호**를 위해 확산. Gartner는 2025년까지 기업 데이터의 75%가 엣지에서 생성·처리될 것으로 전망.
  - 출처: [Edge computing - Wikipedia](https://en.wikipedia.org/wiki/Edge_computing)

- **NVIDIA DRIVE / Jetson 플랫폼**: NVIDIA는 자동차·로봇·드론 등 임베디드 장치에 AI 추론을 위한 전용 플랫폼(DRIVE AGX, Jetson Orin)을 제공. 자동차 OEM들이 ADAS(첨단 운전자 보조 시스템) 개발에 활용.

- **자동차 SDV(Software-Defined Vehicle) 전환**: 현대·기아, BMW, 폭스바겐 등 주요 완성차 업체들이 차량을 "소프트웨어로 정의되는 자동차"로 전환 중. AUTOSAR Adaptive 플랫폼 위에서 OTA(Over-The-Air) 업데이트, AI 기반 운전자 보조, 음성 인식 등을 구현하며 임베디드 SW 개발자 수요 급증.

- **LG webOS AI ThinQ**: LG전자는 자사 가전(TV, 냉장고 등)의 임베디드 OS인 webOS에 AI ThinQ 엔진을 탑재하여 음성 인식, 사용 패턴 학습, 에너지 최적화 등을 기기 자체에서 수행.

> **시사점**: 임베디드 분야에서 AI는 "코딩 보조"보다는 **제품 자체에 AI를 탑재**하는 방향으로 발전 중. 전통적 임베디드 개발(C/C++, RTOS, 하드웨어 제어)에 AI/ML 모델 최적화(양자화, 경량화) 역량이 추가로 요구됨.

### 4-2. 보안·검증이 필요한 분야

#### AI 생성 코드의 보안 문제

- **CodeRabbit 연구 (2025.12)**: 470개 오픈소스 PR 분석 결과, AI 공동 작성 코드가 인간 작성 코드보다 **1.7배 많은 주요 문제** 포함. 보안 취약점은 **2.74배 높음**. 잘못된 접근 제어(Broken Access Control), 로직 오류, 설정 오류 75% 더 많음.
  - 출처: [Our new report: AI code creates 1.7x more problems (CodeRabbit, 2025.12)](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)

- **Veracode 연구 (2025.10)**: 최근 3년간 LLM은 기능적 코드 생성에서는 크게 향상되었으나, **보안성은 전혀 개선되지 않음**. 더 큰 모델도 보안 코드 생성에서 작은 모델 대비 우위 없음.
  - 출처: [October 2025 Update: GenAI Code Security Report (Veracode, 2025)](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/)

- **Lovable 플랫폼 보안 사고 (2025.05)**: 스웨덴의 바이브 코딩 앱 Lovable로 만든 1,645개 웹앱 중 **170개에서 개인정보 노출 취약점** 발견.
  - 출처: [The hottest new vibe coding startup may be a sitting duck for hackers (Semafor, 2025.05)](https://www.semafor.com/article/05/29/2025/the-hottest-new-vibe-coding-startup-lovable-is-a-sitting-duck-for-hackers)

- **GitHub CodeQL 분석 (2025)**: Broken Access Control이 가장 많이 탐지된 취약점 유형으로 부상. **151,000개 이상의 저장소**에서 발견 (+172% YoY). AI 생성 코드에서 인증·인가 로직 누락이 주요 원인.
  - 출처: [GitHub Octoverse 2025 - Security section](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

- **BBC 보도 (2026.02)**: AI 코딩 플랫폼 Orchids의 보안 결함으로 BBC 기자가 실시간 해킹 시연에 당함.
  - 출처: [AI coding platform's flaws allow BBC reporter to be hacked (BBC News, 2026.02)](https://www.bbc.com/news/articles/cy4wnw04e8wo)

#### 금융 분야, 방위산업
- 보안이나 사고예방이 필요한 금융 분야에서 AI 코드 검증의 중요성이 증가
- 신뢰성 보장을 위해 2중, 3중의 안전장치가 필요한 방위산업 분야에서는 오히려 검증 부담 증가
- AI 발전으로 생산성 향상이 되지만 오히려 검증이 추가로 필요함

---

## 5. 업무의 변화 사례

1. **문서 작성 업무가 줄어듬**
   - 개발자로 오랫동안 일하면서 가장 힘든 업무는 코드 작성이 아니라 작성한 코드를 설명하는 문서를 작성 업무임

2. **자료 분석**
   - 연구 개발에서 필수 적인 실험 및 결과 정리를 AI 로 대체

3. **유튜브 시청 시간 감소**
   - 너무나 많은 신기술이 빠르게 나와 공식 문서보다도 유튜브가 더 빠름.
   - AI 를 통한 동영상 요약은 최고다.
   - 결과 데모도 AI 로 동영상을 만든다.

4. **단점은 생산성 향상에 따라 점점 할 일이 많아졌다.**
   - 1년 계획을 세웠는데 3개월만에 끝나서 더 할 일을 찾고 있다.

---

## 6. 앞으로의 전망

### 6-1. 개발자의 삶
1. **끊임없는 학습과 자기 계발**
   - 10년 전에 10년 20년 후의 미래를 생각했을 때와 큰 차이가 없다.
2. 확실한 것은 전문가의 역할이 더 커질 것이다.

### 6-2. 미래의 불확실성
1. **비트코인의 과거와 현재, 미래**
   - 양자 컴퓨터가 개발되면 비트코인의 가치는 올라갈까 떨어질까?
   - 과거 비트코인을 처음 봤을 때, 암호키를 사고파는 다단계라고 생각했다.
2. **기술의 도입은 효용성과 경제적 가치보다도 정치적 영향이 큼**

### 6-3. 나를 위한 결정
1. 내가 하고 싶은 것, 원하는 것
2. 무엇을 공부할지는 내가 결정하는 것

### 6-4. 불확실성에 대응하고 나를 위한 결정을 위해 준비
1. 학습과 부지런한 정보 수집

---

## 참고 자료 목록

| 주제 | 출처 | 링크 |
|------|------|------|
| AI가 700명 업무 대체 (Klarna) | Klarna Press Release (2024.02) | https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ |
| Klarna AI 700명 대체 (Fast Company) | Fast Company (2024.02) | https://www.fastcompany.com/91039401/klarna-ai-virtual-assistant-does-the-work-of-700-humans-after-layoffs |
| Klarna CEO "AI가 모든 일 가능" | Business Insider (2024.12) | https://www.businessinsider.com/klarna-ceo-sebastian-siemiatkowski-ai-jobs-2024-12 |
| 바이브 코딩 정의 및 현황 | Wikipedia: Vibe coding | https://en.wikipedia.org/wiki/Vibe_coding |
| Collins Dictionary 올해의 단어 "vibe coding" | BBC News (2025.11) | https://www.bbc.com/news/articles/cpd2y053nleo |
| YC 스타트업 25%가 95% AI 코드 | TechCrunch (2025.03) | https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/ |
| 바이브 코딩 숙취 보도 | Fast Company (2025.09) | https://www.fastcompany.com/91398622/the-vibe-coding-hangover-is-upon-us |
| 미국 SW 개발자 고용 통계 | U.S. Bureau of Labor Statistics (2024) | https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm |
| GitHub Octoverse 2025 보고서 | GitHub Blog (2025.10) | https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ |
| GitHub Copilot 기업 생산성 연구 | GitHub Blog × Accenture (2024) | https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/ |
| AI 코드 보안 취약점 1.7배 | CodeRabbit Blog (2025.12) | https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report |
| GenAI 코드 보안 보고서 | Veracode (2025.10) | https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/ |
| Lovable 플랫폼 보안 취약점 | Semafor (2025.05) | https://www.semafor.com/article/05/29/2025/the-hottest-new-vibe-coding-startup-lovable-is-a-sitting-duck-for-hackers |
| BBC 기자 AI 코딩 플랫폼 해킹 피해 | BBC News (2026.02) | https://www.bbc.com/news/articles/cy4wnw04e8wo |