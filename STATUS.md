# ✅ 진행 상황 체크리스트 (STATUS)

> 🎉 A/D/E/F안 + 통합안 + 부품 + 오프라인 점검까지 육안 확인 완료.
> 📁 **폴더 재편(2026-08-21):** 함수는 `parts/<기능>`, 완성품은 `products/`로 이동. 전체 지도는 [README.md](README.md).
> 검증 재확인: 컴파일 OK, `pytest parts/tests/` 47개 통과, 완성품 import 정상.
> 남은 것: B안 육안 검증, 조건부 항목(matplotlib 폴백, 대회 규정 확인). SDG 주제 대비 `parts/` 부품 확충 완료.
>
> 최종 업데이트: 2026-08-21
> 대회: AI·SW 부천 연합 해커톤 / 종목: VPython / 주제: "무한한 상상, 무해한 AI"
>
> **보는 법:** `[x]`=완료, `[ ]`=아직. 각 항목은 4단계로 추적한다.
> **계획 → 구현 → 자동검증(문법·테스트) → 육안확인(내가 직접 봄).**
> 네 개가 다 `[x]`면 그 항목은 **완전히 된 것**이다.
> 지금 남은 건 대부분 **⑤ 육안확인(내 몫)** 뿐 — 브라우저 창을 눈으로 봐야 하는 것들.

---

## 한눈에 보기

| 산출물 | 구현 | 자동검증 | 육안확인 | 완전히 됨? |
|---|:---:|:---:|:---:|:---:|
| 환경 설치(vpython 7.6.5) | ✅ | ✅ | ✅ | **✅ 완료** |
| 부품: vector_helpers.py | ✅ | ✅(테스트 20) | — | **✅ 완료** |
| 부품: vpython_utils.py | ✅ | ✅(import) | ✅(데모) | **✅ 완료** |
| 부품: ui_widgets.py | ✅ | ✅(import) | ✅(A안서 슬라이더 한 줄 확인) | **✅ 완료** |
| offline_test.py (오프라인 검증) | ✅ | ✅ | ✅ | **✅ 완료** |
| **A안** hackathon_kit/main.py | ✅ | ✅ | ✅(정상 작동 확인) | **✅ 완료** |
| **D안** 신뢰도 시각화(신설계) | ✅ | ✅ | ✅(정상 작동 확인) | **✅ 완료** |
| **E안** 협업 다리(신설계) | ✅ | ✅ | ✅(정상 작동 확인) | **✅ 완료** |
| **F안** 성장 나무(신설계) | ✅ | ✅ | ✅(정상 작동 확인) | **✅ 완료** |
| **통합안** A+D+E+F (파이프라인) | ✅ | ✅ | ✅(정상 작동 확인) | **✅ 완료** |
| **parts/** 기능별 부품 라이브러리(SDG/AI) | ✅ | ✅(테스트 18) | — | **✅ 완료** |
| 문서(README/GUIDE/HANDOFF/INDEX) | ✅ | — | — | **✅ 완료** |

---

## 0. 환경 / 설치
- [x] 계획: vpython + pytest 준비
- [x] 구현: `requirements.txt` 작성
- [x] 자동검증: `pip install` 성공 (vpython 7.6.5)
- [x] 육안확인: 불필요
- **→ 완전히 됨 ✅**

## 1. 부품 상자 (`hackathon_kit/`)

### 1-1. vector_helpers.py (계산 로직)
- [x] 계획 / [x] 구현 (direction_to, distance, avoid_vector, clamp_speed, blend_vectors, **steer_around** 추가)
- [x] 자동검증: `pytest test_vector_helpers.py` → **20개 통과**
- [x] 육안확인: 불필요(순수 계산)
- **→ 완전히 됨 ✅**

### 1-2. vpython_utils.py (3D 객체 헬퍼)
- [x] 계획 / [x] 구현 (make_scene/agent/obstacle/floor/multiple_agents + width·height·trail_radius·floor pos 확장)
- [x] 자동검증: import OK
- [x] 육안확인: 데모/앱에서 객체 잘 생성됨
- **→ 완전히 됨 ✅**

### 1-3. ui_widgets.py (슬라이더/토글)
- [x] 계획 / [x] 구현 (make_labeled_slider, make_toggle + length·decimals·checkbox_text 확장, **슬라이더-이름 같은 줄로 배치 수정**)
- [x] 자동검증: import OK
- [x] 육안확인: A안 실행 시 슬라이더-이름이 **한 줄로 잘 표시됨** 확인
- **→ 완전히 됨 ✅**

### 1-4. 테스트/검증 스크립트
- [x] test_vector_helpers.py (자동 테스트) — 20개 통과 ✅
- [x] demo_ui_widgets.py — 육안 확인 완료 ✅ (체크박스/슬라이더 반응 봄)
- [x] offline_test.py — **오프라인에서 실행, 체크표시 + 빨간 구슬 창 확인 완료 ✅** (1초 후 닫힘=정상)
- **→ 완전히 됨 ✅**

### 1-5. main_template.py (조립 스켈레톤)
- [x] 구현 (import만 되고 실행 보류 상태)
- [x] 자동검증: import OK
- 참고: 실제 A안은 아래 `main.py`로 완성됨 → 이 파일은 참고용

## 2. A안 — 무해한 AI 장애물 회피 (`hackathon_kit/main.py`)
- [x] 계획 / [x] 구현 (부품 3개를 import해서 조립한 완성본)
- [x] 자동검증: 문법 컴파일 OK, 부품 테스트 통과
- [x] 버그수정 ①: 3D text() 한글 안 뜸 → 캡션(HTML)으로 교체
- [x] 버그수정 ②: 장애물 앞 앞뒤 진동 → `steer_around`(옆으로 우회)로 교체
- [x] 버그수정 ③: 슬라이더 이름이 윗줄 → 같은 줄로 수정
- [x] 육안확인: **정상 작동 확인** — 우회 이동 + 슬라이더 한 줄 표시 OK
- **→ 완전히 됨 ✅**

## 3. D안 — AI 신뢰도 시각화 (`D_trust_visualizer/`)
- [x] 계획 / [x] 구현 (**신설계로 교체**: 공전 선택지 입자 + 가장 안전한 것으로 연결선)
- [x] 스켈레톤 수정: 경로 오류·부품 미사용·점수 saturation·조작 없음 → 4가지 보완
- [x] 자동검증: 컴파일 OK, 부품 import·API 확인
- [x] 육안확인: **정상 작동 확인** — 입자 색 변화 + 연결선 자동 이동 + 안전 기준선 슬라이더 OK
- **→ 완전히 됨 ✅**

## 4. E안 — 인간-AI 협업 다리 건설 (`E_collab_bridge/`)
- [x] 계획 / [x] 구현 (**신설계로 교체**: 사람이 목표 지정 → AI가 안전 규칙 지키며 블록 순차 건설)
- [x] 스켈레톤 수정: 경로 오류·부품 미사용·높이 로직 정리 → 보완
- [x] 자동검증: 컴파일 OK, 부품 import·box API 확인
- [x] 추가 기능: 목표 도달 시 처음부터 다시 건설(반복 시연)
- [x] 육안확인: **정상 작동 확인** — 목표 슬라이더 + AI 순차 건설 + 규칙 OFF 불안정 + 반복 건설 OK
- **→ 완전히 됨 ✅**

## 5. F안 — 안전 경계 성장 나무 (`F_growth_tree/`)
- [x] 계획 / [x] 구현 (**신설계로 교체**: 실시간 성장 + 경계 닿으면 안쪽으로 꺾음)
- [x] 스켈레톤 수정: 경로 오류·부품 미사용·**성능(오래된 가지 숨김)**·꺾임 순간 빨강 표시 보완
- [x] 자동검증: 컴파일 OK, 부품 import·API 확인
- [x] 육안확인: **정상 작동 확인** — 나무 성장 + 경계에서 꺾임(빨강) + 반지름 슬라이더 + 성능 OK
- **→ 완전히 됨 ✅**

## 5-2. 통합안 — A+D+E+F (`combined_adef/`)
- [x] 계획 / [x] 구현 (하나의 판단 파이프라인: 상상→평가→행동→건설)
- [x] 스켈레톤 수정: **3D text() 한글 버그 제거(캡션 교체)**, 부품 재사용, 경로 처리
- [x] 확장 반영: 경계 밖 후보 반투명 처리 + 실시간 위험도 로그
- [x] 자동검증: 컴파일 OK, 부품 import 확인
- [x] 수정: 다리 별칭 버그 / 회피 거리 슬라이더 추가 / 위험도 연속화(직진↔우회 정상)
- [x] 육안확인: **정상 작동 확인** — 후보선 색 + 직진 vs 회피 + 다리 + 슬라이더 3개 + 위험도 로그 OK
- **→ 완전히 됨 ✅**

## 5-3. parts/ 기능별 부품 라이브러리 (`parts/`) — SDG·AI 주제 대비
새 대회 주제(SDGs, AI 접목)에 대비해 **기능 종류별 폴더**로 정리한 조립용 부품.
- [x] pathfinding/astar.py — A* 경로탐색 (게임AI 길찾기)
- [x] world/grid.py — 격자 맵·장애물·좌표변환
- [x] steering/steering.py — seek/arrive/separation/alignment/cohesion/flock (군집 AI)
- [x] optimization/genetic.py, allocate.py — 유전알고리즘·자원배분
- [x] nlp/command_parser.py — 자연어 명령 파서
- [x] models/epidemic.py, resource.py — 전염병 SIR·저수지 모델
- [x] risk/risk.py — 위험도 점수(앱에서 추출·부품화)
- [x] generation/patterns.py — 절차적 배치 줄/나선/원/격자(앱에서 추출·부품화)
- [x] dataviz/live_graph.py — 실시간 선/막대 그래프
- [x] tests/test_parts.py — 순수 부품 **자동 테스트 27개 통과**
- [x] README.md + **CATALOG.md** — 조합표 + hackathon_kit 포함 전체 함수 통합 인덱스
- **→ 완제품 아님(의도). 대회장에서 골라 조립. 순수 로직은 검증 완료 ✅**
- 검증 합계: 벡터 20 + 부품 27 = **자동 테스트 47개 통과**

## 5-4. 공용 뼈대 (`products/TEMPLATE_sdg_base/`) — 즉석 SDG 대비
- [x] 새 부품: `parts/scene/grid_render.py` (격자 3D 렌더링: cell_pos/render_floor/render_obstacles)
- [x] 뼈대 main.py: 에이전트 + 격자맵 + 실시간 그래프 조립, ①②③ 슬롯만 채우면 주제 완성
- [x] 자동검증: 컴파일 OK, 부품 import·격자 로직 확인
- [ ] 육안확인: `cd products/TEMPLATE_sdg_base; python main.py` → 에이전트 랜덤워크 + 그래프
- **→ 뼈대(템플릿). 대회장에서 복사해 주제 로직만 얹음. 육안 확인만 남음**

## 5-5. SDG 기법별 데모 5종 (`products/SDG*`) — 무기고 확충
어떤 SDG가 나와도 대응하도록 AI 기법별 완성 데모 추가. 전부 부품 조립.
- [x] SDG11_evacuation — **A\* 경로탐색** 재난 대피(출구 개수 실험)
- [x] SDG14_ocean_cleanup — **군집 flocking** 해양 청소 로봇(로봇 수↑ 효율↑)
- [x] SDG03_epidemic — **SIR 모델** 전염병 확산(거리두기·백신 효과)
- [x] SDG06_water — **자원배분+저수지** 물 분배 대시보드(트레이드오프)
- [x] SDG15_forest_ga — **유전알고리즘** 숲 배치 최적화(세대별 개선)
- [x] 자동검증: 5개 컴파일 OK + 부품 import OK + 테스트 48개 통과
- [x] 부품 확장: live_graph.make_lines(다중곡선), genetic on_generation(세대 콜백)
- [ ] 육안확인: 각 `cd products/SDG*; python main.py` (5개 실행 확인 대기)
- **→ 실행 가능, 시각 검증만 남음**

## 5-6. 전체 SDG 커버 데모 12종 추가 (`products/SDG01~17`)
17개 SDG 전부 하나 이상 대응하도록 나머지 12개를 각기 다른 내용으로 완성.
- [x] SDG01 빈곤(자원배분) / SDG02 기아(유전-비옥지) / SDG04 교육(자연어 파서)
- [x] SDG05 성평등(편향 승진) / SDG07 에너지(유전-입지) / SDG08 일자리(배치·실업)
- [x] SDG09 인프라(A* 도로망) / SDG10 불평등(지니계수) / SDG12 소비(재활용 순환)
- [x] SDG13 기후(탄소vs숲) / SDG16 평화(규칙→협력) / SDG17 협력(국가 네트워크)
- [x] 자동검증: 12개 컴파일 OK + 부품 import OK + 테스트 48개 유지
- [ ] 육안확인: 각 `cd products/SDG*; python main.py`
- **→ SDG 1~17 전부 데모 확보(5+12=17). 시각 검증만 남음**

## 5-7. SDG 2차(다른 각도) 데모 17종 — "아예 다른 느낌" 대비
각 SDG를 1차와 다른 장르(대시보드·네트워크·사다리·생태계 등)로 하나씩 더.
- [x] 01 안전망 / 02 영양대시보드 / 03 병상수용력 / 04 교육접근성 / 05 임금격차
- [x] 06 상수도망 / 07 발전믹스 / 08 스킬매칭 / 09 네트워크복원력 / 10 계층이동
- [x] 11 교통신호 / 12 순환경제 / 13 해수면 / 14 먹이사슬 / 15 삼림파괴
- [x] 16 자원분쟁 / 17 무임승차
- [x] 자동검증: 17개 전부 컴파일 OK (arrow 등 API 확인)
- [ ] 육안확인: 각 실행 확인 대기
- **→ SDG마다 서로 다른 각도 2종 확보(총 34 SDG 데모 + 별도 완성품). 시각 검증만 남음**

## 6. 문서
- [x] README.md (루트 — 전체 폴더 지도)
- [x] parts/CATALOG.md (전체 함수 통합 인덱스) + parts/README.md (주제별 조합표)
- [x] parts/PROJECT_GUIDE.md (초보자용 설명)
- [x] products/* 각 HANDOFF.md (개념→로직→테스트→확장)
- [x] IDEAS_INDEX.md (아이디어 인덱스 + 실행법)
- **→ 완전히 됨 ✅**

---

## 🔲 지금 내가 확인할 차례 (열린 항목만 모음)

브라우저 창을 눈으로 봐야 하는 것들. 하나씩 실행하고 확인되면 위 체크박스를 `[x]`로 바꾸면 됨.

- [x] **A안** — `cd products/A_safe_avoidance; python main.py` → 장애물 우회 + 슬라이더 한 줄 표시 ✅ 확인 완료
- [x] **D안(신설계)** — `cd products/D_trust_visualizer; python main.py` → 입자 색 변화 + 연결선 자동 이동 + 안전 기준선 ✅ 확인 완료
- [x] **E안(신설계)** — `cd products/E_collab_bridge; python main.py` → 목표 슬라이더 + AI 순차 건설 + 규칙 OFF 불안정 + 반복 건설 ✅ 확인 완료
- [x] **F안(신설계)** — `cd products/F_growth_tree; python main.py` → 나무 성장 + 경계에서 꺾임(빨강) + 반지름 슬라이더 ✅ 확인 완료
- [x] **오프라인 최종 점검** — Wi-Fi 끄고 A/D/E/F 각각 창 뜨는지 확인 ✅ 완료
- [x] **통합안(A+D+E+F)** — `cd products/combined_adef; python main.py` → 후보선 색/직진vs회피 + 다리 + 슬라이더 3개 + 위험도 로그 ✅ 확인 완료
- [ ] **B안(자연어→3D)** — `cd products/B_nl3d; python main.py` → 문장 입력(Enter)하면 색/모양/개수/패턴대로 3D 생성되는지 (컴파일 OK, 육안 검증 대기)

> 각 확인 포인트 상세는 해당 폴더 `HANDOFF.md`의 "테스트 방법" 참고.

---

## 아직 안 만든 것 (조건부 대기)
- [ ] `fallback_matplotlib.py` — offline_test가 ❌일 때만 (현재 오프라인 정상이라 불필요)
- [ ] B안 API 강화 (Claude API 자유 문장) — 온라인·규정 확인 시 (오프라인 파서는 완성)
- [ ] 대회 규정 확인 (사전 제작물 허용 범위) — 확인되면 이 문서 갱신
- [ ] SDG 주제 확정 시 — `parts/` 부품 조립해 해당 주제 MVP 제작
