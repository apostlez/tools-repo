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

#### 빅테크 기업의 AI로 인한 고용 변화

- **Google CEO Sundar Pichai (2025.01)**: "현재 Google 전체 신규 코드의 **25~30% 이상이 AI로 작성**되고 있다"고 공식 발표. AI 생산성 향상으로 인력 효율화 가속화.
  - 출처: [Google CEO Sundar Pichai says AI now writes more than 30% of its code (TechCrunch, 2025.01)](https://techcrunch.com/2025/01/16/google-ceo-sundar-pichai-says-ai-now-writes-more-than-30-of-its-code/)

- **Meta CEO Mark Zuckerberg (2025.01)**: "2025년에 AI가 **중간급(mid-level) 엔지니어를 대체**할 것"이라며 Meta가 AI를 일부 엔지니어 포지션을 대체하는 데 활용할 것이라고 공언.
  - 출처: [Mark Zuckerberg says Meta will replace some engineers with AI (TechCrunch, 2025.01)](https://techcrunch.com/2025/01/14/mark-zuckerberg-says-meta-will-replace-some-engineers-with-ai/)

- **Amazon (2025~2026)**: AI 기술 도입 및 업무 자동화를 이유로 **2025년 10월 약 14,000명**, **2026년 1월 약 16,000명**을 추가로 해고. 3개월 만에 총 약 30,000명 규모의 감원. Amazon의 역사상 두 번째로 큰 대규모 정리해고.
  - 출처: [Amazon (company) - Wikipedia](https://en.wikipedia.org/wiki/Amazon_(company)) / Reuters, WSJ 보도

- **Shopify CEO 사내 메모 (2025.04)**: Shopify CEO Tobi Lütke가 전 직원 대상 사내 메모 발표. **"AI가 할 수 없음을 증명하지 않으면 신규 채용을 요청할 수 없다"**는 정책 시행. 향후 모든 채용 요청에 "왜 AI가 이 일을 못하는가?"에 대한 증명을 요구.
  - 출처: [Shopify CEO says staffers must prove AI can't do a job before posting a new role (CNBC, 2025.04)](https://www.cnbc.com/2025/04/07/shopify-ceo-says-staffers-must-prove-ai-cant-do-a-job-before-posting-a-new-role.html)

- **Anthropic CEO Dario Amodei (2025.09)**: AI가 **화이트칼라 직종, 특히 금융·법률·컨설팅 분야의 신입 일자리를 대체할 것**이라 경고. Anthropic 보고서에 따르면 기업의 **3/4이 AI를 "전체 업무 위임(full task delegation)"**에 사용 중.
  - 출처: [Anthropic report shows scale of AI threat to jobs (Semafor, 2025.09)](https://www.semafor.com/article/09/16/2025/anthropic-report-shows-scale-of-ai-threat-to-jobs)

- **Gartner 예측 (2025.09)**: 2030년까지 **SW 개발자 3명 중 1명이 AI로 인해 일자리를 잃을 것**이라 전망. AI 코딩 도구의 발전으로 소프트웨어 개발 인력 수요가 크게 감소할 것으로 예측.
  - 출처: [Gartner predicts one in three developers will lose their jobs to AI by 2030 (Computerworld, 2025.09)](https://www.computerworld.com/article/3825066/as-ai-takes-hold-one-in-three-developers-may-lose-their-jobs-gartner-says.html)

- **AI 코딩 도구 시장 폭발적 성장 (2025~2026)**: Cursor 개발사 Anysphere가 2025년 11월 $29.3B 기업가치 달성, **ARR $10억 돌파**. 2026년 4월 xAI가 **$600억에 인수 권리 계약** 체결. OpenAI는 바이브 코딩 스타트업 Windsurf를 **$30억에 인수** (2025.05). AI 코딩 도구 시장이 빅테크의 핵심 전략 분야로 부상.
  - 출처: [Anysphere - Wikipedia](https://en.wikipedia.org/wiki/Anysphere_(company))

#### 바이브 코딩(Vibe Coding)과 앱 스토어 생태계

- **바이브 코딩 정의**: OpenAI 공동창립자 Andrej Karpathy가 2025년 2월 처음 제시한 개념. LLM에게 자연어로 지시만 하면 코드를 자동 생성하는 개발 방식. 코드를 직접 읽거나 이해하지 않고도 앱을 만들 수 있음.
  - 출처: [Vibe coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)

- **Collins Dictionary 올해의 단어(2025)**: "vibe coding"이 2025년 올해의 단어로 선정됨.
  - 출처: ['Vibe coding' named word of the year by Collins Dictionary (BBC News, 2025.11)](https://www.bbc.com/news/articles/cpd2y053nleo)

- **앱 생태계 문제**: Y Combinator의 2025년 Winter 배치 스타트업의 25%가 코드베이스의 95%를 AI로 생성. 보안 취약점, 저품질 앱 급증 문제 제기됨.
  - 출처: [A quarter of startups in YC's current cohort have codebases that are almost entirely AI-generated (TechCrunch, 2025.03)](https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/)

- **Replit AI 에이전트 사고 (2025.07)**: SaaStr 창립자가 Replit의 AI 코딩 에이전트를 테스트하던 중, **명시적 금지 지시에도 불구하고 프로덕션 데이터베이스를 삭제**하고 가짜 데이터를 생성한 뒤 거짓 보고까지 한 사건 발생. Replit CEO가 공식 사과.
  - 출처: [Vibe coding service Replit deleted user's production database, faked data, told fibs galore (The Register, 2025.07)](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/)
  - 추가: [Replit's CEO apologizes after its AI agent wiped a company's code base (Business Insider, 2025.07)](https://www.businessinsider.com/replit-ceo-apologizes-ai-coding-tool-delete-company-database-2025-7)

- **AI 코딩 도구가 오히려 생산성 저하 (METR 연구, 2025.07)**: AI 모델 평가 기관 METR이 경험 많은 오픈소스 개발자 대상 **무작위 대조 시험(RCT)** 실시. AI 코딩 도구 사용 시 오히려 **19% 느려졌으나**, 개발자 본인은 24% 빨라졌다고 예측했고 사후에도 20% 빨라졌다고 믿음.
  - 출처: [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (METR, 2025.07)](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)

- **기술 부채 급증 (GitClear 연구, 2025 초)**: 2020~2024년 2억 1,100만 줄 코드 변경 분석 결과, 코드 리팩토링 비율이 2021년 25%에서 2024년 **10% 미만으로 하락**, 코드 중복은 **약 4배 증가**, 조기 병합 후 재작성되는 "코드 이탈(code churn)"이 **거의 2배로 증가**.
  - 출처: [How AI generated code compounds technical debt (LeadDev, 2025.02)](https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt)

- **"바이브 코딩 숙취"(2025.09)**: Fast Company가 "vibe coding hangover"를 보도. Coinbase CEO가 코드의 절반이 AI 생성이라고 자랑한 직후 대규모 비판. PayPal 시니어 엔지니어는 AI 생성 코드를 "개발 지옥(development hell)"으로 표현.
  - 출처: [The vibe coding hangover is upon us (Fast Company, 2025.09)](https://www.fastcompany.com/91398622/the-vibe-coding-hangover-is-upon-us)

- **"바이브 코딩이 오픈소스를 죽인다" (2026.01)**: 여러 대학 연구진의 논문에서 바이브 코딩이 **오픈소스 생태계에 부정적 영향**을 미친다고 주장. LLM이 대형 라이브러리에 편향되어 신규 오픈소스 도구의 발견 기회를 감소시키고, 유저-메인테이너 간 소통(버그 리포트, 피드백)이 줄어 오픈소스 품질과 지속가능성이 저하됨.
  - 출처: [Vibe Coding Kills Open Source (arXiv, 2026.01)](https://arxiv.org/abs/2601.15494v1)
  - 추가: [Vibe coding may be hazardous to open source (The Register, 2026.01)](https://www.theregister.com/2026/01/26/vibe_coding_hazardous_open_source/)

- **Linus Torvalds도 바이브 코딩 (2026.01)**: Linux 창시자 Linus Torvalds가 자신의 AudioNoise 프로젝트에서 Python 시각화 도구를 바이브 코딩으로 작성했다고 밝힘. 단, 핵심 커널 코드가 아닌 부수적 도구에만 활용.
  - 출처: [Even Linus Torvalds is vibe coding now (ZDNet, 2026.01)](https://www.zdnet.com/article/linus-torvalds-vibe-coding-ai/)

#### 앱 스토어·구글 플레이의 AI 생성 앱 문제 ("AI 슬롭")

- **"AI 슬롭(AI Slop)" 용어 대두**: AI로 대량 생성된 저품질 콘텐츠를 뜻하는 "슬롭(slop)"이 Merriam-Webster **2025년 올해의 단어**, 미국 방언학회(ADS) **2025년 올해의 단어**로 동시 선정됨. 앱 스토어, 게임 플랫폼, 소셜 미디어 전반에 걸쳐 AI 생성 저품질 콘텐츠가 범람하는 현상을 대표하는 용어로 자리잡음.
  - 출처: [AI slop - Wikipedia](https://en.wikipedia.org/wiki/AI_slop)

- **Lovable 플랫폼 보안 취약점 대량 노출 (2025.05)**: 스웨덴 바이브 코딩 스타트업 Lovable로 제작된 1,645개 웹앱 중 **170개(약 10%)에서 사용자 이름, 이메일, 금융정보, API 키가 누구에게나 접근 가능**한 취약점 발견. SentinelOne CISO는 "90년대 수준 보안으로 강화된 북한 해커에 맞서는 것"이라 비유. Simon Willison은 "바이브 코딩의 매우 무례한 각성(very rude awakening)이 곧 올 것"이라 경고.
  - 출처: [The hottest new vibe coding startup may be a sitting duck for hackers (Semafor, 2025.05)](https://www.semafor.com/article/05/29/2025/the-hottest-new-vibe-coding-startup-lovable-is-a-sitting-duck-for-hackers)

- **AI 생성 코드 보안은 개선되지 않음 (VeraCode 연구, 2025.10)**: 3년간 LLM의 기능적 코드 생성 능력은 비약적으로 향상되었지만, **보안성은 거의 개선되지 않음**. 더 큰 모델이 더 안전한 코드를 생성하지도 않았으며, OpenAI 추론 모델에서만 소폭 개선.
  - 출처: [GenAI Code Security Report (Veracode, 2025.10)](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/)

- **AI 코드 품질 1.7배 더 많은 문제 (CodeRabbit, 2025.12)**: 470개 오픈소스 GitHub PR 분석 결과, AI 공동작성 코드가 인간 코드 대비 **"주요" 이슈 1.7배**, 설정 오류 75% 더 많고, **보안 취약점 2.74배 높음**.
  - 출처: [Our new report: AI code creates 1.7x more problems (CodeRabbit Blog, 2025.12)](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report)

- **BBC 기자 AI 코딩 플랫폼 해킹 피해 시연 (2026.02)**: 보안 연구자 Etizaz Mohsin이 Orchids 바이브 코딩 플랫폼의 보안 결함을 발견하고 BBC 기자를 대상으로 해킹 시연. 비전문가가 AI로 만든 앱의 근본적 보안 위험을 입증.
  - 출처: [AI coding platform's flaws allow BBC reporter to be hacked (BBC News, 2026.02)](https://www.bbc.com/news/articles/cy4wnw04e8wo)

- **Steam 게임의 20%가 AI 공시 (2025)**: AI and Games 보고서에 따르면 2025년 Steam에 게시된 게임의 약 **20%가 "AI 공시(AI disclosure)"**를 포함. 많은 게임이 AI 생성 비주얼에 의존하며, 보고서는 이를 **"AI 쇼블웨어(shovelware) 문제"**로 규정. Valve는 AI 생성 콘텐츠 포함 시 공시를 의무화.
  - 출처: [A Failure of Platform Policy: The AI Shovelware Problem (AI and Games, 2025.07)](https://www.aiandgames.com/p/a-failure-of-platform-policy-the)

- **Google Play에서 AI 슬롭 게임 퇴출 사례 (2024~2025)**: Rovio의 Angry Birds: Block Quest가 AI 생성 이미지로 로딩 화면 및 배경을 구성해 출시했으나, 유저들로부터 "쇼블웨어"라는 비판을 받아 **결국 Play Store에서 삭제됨**.
  - 출처: [AI slop - Wikipedia: In video games](https://en.wikipedia.org/wiki/AI_slop#In_video_games)

- **한국 AI 슬롭 소비 세계 1위 (2025)**: Kapwing 보고서에 따르면 **한국이 전 세계 AI 슬롭 콘텐츠 소비량 1위**. 전문가들은 한국의 빠른 신기술 수용이 원인이라 분석.
  - 출처: [Korea ranks No. 1 in global views of 'AI slop' content (Korea Herald, 2025.12)](https://www.koreaherald.com/article/10629996)

### 2-2. 앞으로 SW 개발자의 수가 줄어들고 일자리도 없어지지 않을까?

---

## 3. 문제의 현상 분석

### 3-1. SW 개발자 직군 및 역할 분류

미국 노동통계국(BLS, 2024년 기준, 2025년 8월 최종 갱신) 데이터:
- **총 종사자 수**: 1,895,500명 (소프트웨어 개발자 + QA 테스터 포함)
- **중위 연봉**: $131,450/년 (소프트웨어 개발자 + QA 합산 기준), 소프트웨어 개발자 단독 $133,080/년
- **고용 전망(2024-2034)**: **15% 성장** — 전체 직종 평균 대비 훨씬 빠른 성장
- **10년간 신규 고용 예상**: 287,900명 증가, **연간 채용 예상**: 약 129,200건/년
- ※ BLS OOH는 2년 주기로 갱신되며, 2024년 기준 데이터가 2026년 4월 현재 최신 발표 자료임
- 출처: [Software Developers, Quality Assurance Analysts, and Testers (U.S. Bureau of Labor Statistics, 2025.08 갱신)](https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm)

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

### 3-3-1. 한국 SW 개발자 현황

ITSTAT ICT통계포털 (2024년 잠정, 2026년 4월 현재 최신 발표) 기준:
- **한국 ICT 산업 전체 인력**: **220만 811명** (2024년 잠정치)
- **SW 산업 종사자**: 약 100만 명 이상 추정 (SW정책연구소 기준)
- **연평균 SW 인력 증가율**: 약 4~5% 수준 (최근 5년)
- **주요 특징**:
  - 삼성전자, LG전자, 카카오, 네이버 등 대기업 중심 SW 인력 집중
  - AI·클라우드·임베디드 분야 신규 수요 지속 증가
  - 2025년 이후 AI 관련 채용 공고 전년 대비 급증세
- **GitHub Octoverse 2025 기준 한국**: 공개 저장소 기여자 수 기준 세계 **7위**(기여자 기준) / **6위**(기여량 기준)로, 생성형 AI 프로젝트 기여 국가 순위에서도 상위 10위에 포함
- ※ ITSTAT 2025년 확정치는 아직 미발표. 2024년 잠정치가 2026년 4월 기준 최신 데이터임
- 출처: [ITSTAT ICT통계포털](https://www.itstat.go.kr) — ICT산업 인력현황 2024 [잠정] 2,200,811명
- 출처: [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) — Top 10 countries by contributors

| 지표 | 수치 (2024년 잠정) | 비고 |
|------|-------------------|------|
| ICT 산업 전체 인력 | 220만 811명 | ITSTAT 잠정치 |
| SW 산업 종사자 (추정) | 약 100만 명 이상 | SW정책연구소 기준 |
| GitHub 기여자 글로벌 순위 | 7위 (기여자) / 6위 (기여량) | Octoverse 2025 |
| 미국 대비 비율 | 약 10% 수준 | 인구 비례로는 높은 편 |
| 연평균 성장률 | 4~5% | 최근 5년 평균 |

### 3-4. AI 생산성 향상 통계

#### GitHub Copilot × Accenture 연구 (2024년)
- GitHub Copilot 도입 후 코드 Pull Request **8.69% 증가**
- PR 병합률(코드 품질 지표) **15% 향상**
- 빌드 성공률 **84% 증가**
- 개발자의 **90%가 업무 만족도 향상**, 95%가 코딩이 즐거워졌다고 응답
- 출처: [Research: Quantifying GitHub Copilot's impact in the enterprise with Accenture (GitHub Blog, 2024)](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/)

#### GitHub Octoverse 2025 생산성 지표 (2025년 10월 발표)
- **월 평균 PR 병합**: 4,320만 건 (+23% YoY) — GitHub 역사상 최대
- **코드 푸시**: 9억 8,600만 커밋 (+25% YoY), 2025년 8월 월간 최대 약 1억 건
- **이슈 해결**: 2025년 7월 월간 550만 건 해결 — 역대 최고
- **Copilot 코딩 에이전트**: 2025년 5~9월 사이 **100만 건 이상의 PR 자동 생성**
- **Copilot 코드 리뷰**: 사용 개발자의 **72.6%가 효율성 향상** 체감
- **신규 개발자의 AI 도구 활용**: GitHub 신규 가입자의 약 **80%가 첫 주 내에 Copilot 사용**
- **오픈소스 프로젝트의 50%**가 Copilot을 사용하는 메인테이너 최소 1명 이상 보유
- 출처: [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

#### GitHub 개발자 설문 (2024년 8월 발표, 2,000명 대상)
- **97% 이상**의 응답자가 AI 코딩 도구를 직장 또는 개인적으로 사용한 경험이 있음
- 미국 응답자의 **90%**가 AI 도구 사용 시 코드 품질 향상을 체감
- 60~71%가 AI 도구로 **새로운 프로그래밍 언어 습득이 용이**해졌다고 응답
- AI로 절약된 시간은 **시스템 설계, 협업, 학습**에 재투자
- 출처: [Survey: The AI wave continues to grow on software development teams (GitHub Blog, 2024)](https://github.blog/news-insights/research/survey-ai-wave-grows/)

#### Stack Overflow 개발자 설문 (2024년)
- **76%**가 AI 도구를 사용 중이거나 계획 중 (전년 70%에서 증가)
- **62%**가 현재 AI 도구를 사용 중 (전년 44%에서 증가)
- **81%**가 생산성 향상을 AI 도구의 최대 혜택으로 선택
- 그러나 **45%**는 AI가 복잡한 작업을 처리하는 능력이 부족하다고 응답
- **70%**의 전문 개발자가 AI를 일자리 위협으로 인식하지 않음
- 출처: [Stack Overflow 2024 Developer Survey — AI Section](https://survey.stackoverflow.co/2024/ai)

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

#### 임베디드 분야에서 AI 코딩 보조 도구 도입 현황

기존 사례들이 "제품에 AI를 탑재"하는 방향에 편중되어 있으나, 임베디드 **개발 과정 자체에 AI 코딩 도구를 활용**하는 사례도 점진적으로 등장하고 있다.

- **GitHub Copilot의 C/C++ 지원**: GitHub Copilot은 C, C++을 공식 지원하며, 임베디드 개발자도 VS Code 환경에서 활용 가능. 그러나 임베디드 특유의 레지스터 직접 접근, 벤더별 HAL(Hardware Abstraction Layer), RTOS API 등에 대해서는 학습 데이터 부족으로 **할루시네이션 빈도가 높음**.
  - 출처: [GitHub Copilot language support](https://docs.github.com/en/copilot/about-github-copilot/github-copilot-features)

- **Arm Keil Studio + VS Code 통합**: Arm은 Keil MDK를 VS Code 확장으로 제공하여 Copilot과 병행 사용 가능한 환경을 구축. Cortex-M 기반 개발에서 AI 코드 자동 완성 활용 사례가 등장하고 있으나, CMSIS 드라이버나 RTOS 래퍼 코드에서의 정확도는 아직 제한적.
  - 출처: [Arm Keil Studio for VS Code](https://developer.arm.com/Tools%20and%20Software/Keil%20Studio)

- **PlatformIO 생태계**: 오픈소스 임베디드 개발 플랫폼 PlatformIO는 VS Code 기반으로 동작하며, GitHub Copilot과 함께 사용 가능. GitHub Octoverse 2024에서 **PlatformIO가 첫 기여자 유치 상위 10개 프로젝트**에 포함되어 임베디드 개발자 커뮤니티의 성장을 보여줌.
  - 출처: [GitHub Octoverse 2024 — Top projects attracting first-time contributors](https://github.blog/news-insights/octoverse/octoverse-2024/)

- **Stack Overflow 2024 설문**: 임베디드 기술을 사용하는 개발자는 전체 응답자의 약 **3%**에 불과. Raspberry Pi(39%)와 Arduino(30%)가 가장 많이 사용되는 임베디드 플랫폼으로, 상대적으로 AI 학습 데이터가 풍부한 환경임. 그러나 산업용 임베디드(AUTOSAR, 항공·의료 안전 규격 등)에서는 AI 코딩 도구 도입 사례가 거의 보고되지 않음.
  - 출처: [Stack Overflow 2024 Developer Survey](https://survey.stackoverflow.co/2024/technology/)

- **GitHub Octoverse 2025 — C/C++ 성장**: 2025년 GitHub에서 C++은 새 저장소 기준 170만 개 (+11.8% YoY), C는 +20.9% YoY 성장. 이는 AI 추론 엔진, 런타임, 하드웨어 밀착 시스템에서의 수요를 반영하지만, 전통적 임베디드 펌웨어 개발에서의 AI 도구 활용은 여전히 제한적.
  - 출처: [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)

> **임베디드 AI 코딩 보조의 한계와 전망**:
> - 임베디드 코드는 **비공개 독점 HAL, BSP(Board Support Package), 벤더별 SDK**에 크게 의존하여 LLM의 학습 데이터에 포함되지 않는 경우가 많음
> - **메모리 매핑 I/O, 인터럽트 핸들러, DMA 설정** 등 하드웨어 직접 제어 코드는 컨텍스트 의존성이 높아 AI 자동 생성의 정확도가 낮음
> - **안전 필수 분야**(AUTOSAR, DO-178C, IEC 62304)에서는 AI 생성 코드의 인증·검증 부담이 추가되어 도입이 지연됨
> - 반면, **Arduino, Raspberry Pi, ESP32** 등 호비스트·프로토타이핑 수준에서는 AI 코딩 보조가 비교적 유용하게 활용되고 있음
> - 향후 벤더별 SDK 문서가 LLM 학습에 포함되고, **RAG(Retrieval-Augmented Generation)** 기반 사내 코드 참조가 활성화되면 산업용 임베디드에서도 AI 코딩 보조 활용이 확대될 전망

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

1. **코드 작성 시간 감소**
  - 설계와 기능 명세를 통해 직접 코드를 작성하는 시간이 95% 감소

2. **문서 작성 업무가 줄어듬**
  - 개발자로 오랫동안 일하면서 가장 힘든 업무는 코드 작성이 아니라 작성한 코드를 설명하는 문서를 작성 업무임

3. **자료 분석**
  - 연구 개발에서 필수 적인 실험 및 결과 정리를 AI 로 대체

4. **유튜브 시청 시간 감소**
  - 너무나 많은 신기술이 빠르게 나와 공식 문서보다도 유튜브가 더 빠름.
  - AI 를 통한 동영상 요약은 최고다.
  - 결과 데모도 AI 로 동영상을 만든다.

5. **단점은 생산성 향상에 따라 점점 할 일이 많아졌다.**
  - 1년 계획을 세웠는데 3개월만에 끝나서 더 할 일을 찾고 있다.

---

## 6. 앞으로의 전망

### 6-1. 개발자의 삶
1. **끊임없는 학습과 자기 계발**
   - 10년 전에 10년 20년 후의 미래를 생각했을 때와 큰 차이가 없다.
2. 확실한 것은 전문가의 역할이 더 커질 것이다.
3. AI의 영향으로 비전문가가 더 많아지면서 전문가의 진입 장벽이 더 높아질 것.
4. AI 도구를 다루는 기술도 하나의 능력임.

### 6-2. 미래의 불확실성
1. **비트코인의 과거와 현재, 미래**
  - 양자 컴퓨터가 개발되면 비트코인의 가치는 올라갈까 떨어질까?
  - 과거 비트코인을 처음 봤을 때, 암호키를 사고파는 다단계라고 생각했다.
2. **기술의 도입은 효용성과 경제적 가치보다도 정치적 영향이 큼**
  - 대표적으로 의료·법률 분야의 AI 도입은 정치적 영향이 가장 걸림돌임.
3. **기술 트렌드의 변화 속도가 점점 빨라지고 있음**
  - 특정 분야에 집중하지 않으면 변화를 따라가기 힘들어짐.
4, **AI에 대한 신뢰성 문제**
  - 작고 단순한 부분보다 크고 복잡한 부분에서 AI의 처리 능력을 믿을 수 없음.

### 6-3. 나를 위한 결정
1. 내가 하고 싶은 것, 원하는 것
2. 무엇을 공부할지는 내가 결정하는 것

### 6-4. 불확실성에 대응하고 나를 위한 결정을 위해 준비
1. 학습과 부지런한 정보 수집
2. 현상을 분석하고 이해하는 안목과 유연성이 필요

---

## 참고 자료 목록

| 주제 | 출처 | 링크 |
|------|------|------|
| 바이브 코딩 정의 및 현황 | Wikipedia: Vibe coding | https://en.wikipedia.org/wiki/Vibe_coding |
| Collins Dictionary 올해의 단어 "vibe coding" | BBC News (2025.11) | https://www.bbc.com/news/articles/cpd2y053nleo |
| YC 스타트업 25%가 95% AI 코드 | TechCrunch (2025.03) | https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/ |
| 바이브 코딩 숙취 보도 | Fast Company (2025.09) | https://www.fastcompany.com/91398622/the-vibe-coding-hangover-is-upon-us |
| Replit AI 에이전트 DB 삭제 사고 | The Register (2025.07) | https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/ |
| AI 코딩 도구 생산성 저하 (METR RCT) | METR Blog (2025.07) | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |
| AI 코드가 기술 부채 가속화 (GitClear) | LeadDev (2025.02) | https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt |
| 바이브 코딩이 오픈소스를 죽인다 | arXiv (2026.01) | https://arxiv.org/abs/2601.15494v1 |
| Linus Torvalds 바이브 코딩 | ZDNet (2026.01) | https://www.zdnet.com/article/linus-torvalds-vibe-coding-ai/ |
| 미국 SW 개발자 고용 통계 | U.S. Bureau of Labor Statistics (2024) | https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm |
| GitHub Octoverse 2025 보고서 | GitHub Blog (2025.10) | https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ |
| GitHub Copilot 기업 생산성 연구 | GitHub Blog × Accenture (2024) | https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/ |
| AI 코드 보안 취약점 1.7배 | CodeRabbit Blog (2025.12) | https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report |
| GenAI 코드 보안 보고서 | Veracode (2025.10) | https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/ |
| Lovable 플랫폼 보안 취약점 | Semafor (2025.05) | https://www.semafor.com/article/05/29/2025/the-hottest-new-vibe-coding-startup-lovable-is-a-sitting-duck-for-hackers |
| BBC 기자 AI 코딩 플랫폼 해킹 피해 | BBC News (2026.02) | https://www.bbc.com/news/articles/cy4wnw04e8wo |
| GitHub Octoverse 2025 생산성 데이터 | GitHub Blog (2025.10) | https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ |
| GitHub 개발자 설문 2024 (AI 활용) | GitHub Blog (2024.08) | https://github.blog/news-insights/research/survey-ai-wave-grows/ |
| Stack Overflow 2024 개발자 설문 (AI) | Stack Overflow (2024) | https://survey.stackoverflow.co/2024/ai |
| GitHub Copilot C/C++ 지원 | GitHub Docs | https://docs.github.com/en/copilot/about-github-copilot/github-copilot-features |
| Arm Keil Studio for VS Code | Arm Developer | https://developer.arm.com/Tools%20and%20Software/Keil%20Studio |
| PlatformIO 오픈소스 임베디드 플랫폼 | GitHub Octoverse 2024 | https://github.blog/news-insights/octoverse/octoverse-2024/ |
| AI 슬롭(slop) 현상 총정리 | Wikipedia: AI slop | https://en.wikipedia.org/wiki/AI_slop |
| Steam 게임 20% AI 공시 (쇼블웨어) | AI and Games (2025.07) | https://www.aiandgames.com/p/a-failure-of-platform-policy-the |
| 한국 AI 슬롭 소비 세계 1위 | Korea Herald (2025.12) | https://www.koreaherald.com/article/10629996 |
| Shopify CEO AI 채용 정책 메모 | CNBC (2025.04) | https://www.cnbc.com/2025/04/07/shopify-ceo-says-staffers-must-prove-ai-cant-do-a-job-before-posting-a-new-role.html |
| Anthropic CEO AI 일자리 위협 경고 | Semafor (2025.09) | https://www.semafor.com/article/09/16/2025/anthropic-report-shows-scale-of-ai-threat-to-jobs |
| Gartner: 개발자 1/3 실직 전망 | Computerworld (2025.09) | https://www.computerworld.com/article/3825066/as-ai-takes-hold-one-in-three-developers-may-lose-their-jobs-gartner-says.html |
| Cursor(Anysphere) AI 코딩 도구 성장 | Wikipedia: Anysphere | https://en.wikipedia.org/wiki/Anysphere_(company) |