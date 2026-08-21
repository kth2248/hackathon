# 부천 해커톤 작업 폴더 — 전체 지도

두 개로 딱 나뉜다: **함수는 `parts/`(기능별), 완성품은 `products/`(실행 데모).**

```
contest/
├── parts/                 # 🧩 함수 = 기능 종류별 폴더
│   ├── vectors/           #   벡터 수학 (direction_to, distance, steer_around, ...)
│   ├── scene/             #   3D 씬·객체 (make_scene, make_agent, ...)
│   ├── ui/                #   슬라이더·토글 (make_labeled_slider, make_toggle)
│   ├── pathfinding/       #   A* 경로탐색 (게임AI 길찾기)
│   ├── world/             #   격자 맵·장애물
│   ├── steering/          #   이동·군집 (seek/arrive/flocking)
│   ├── optimization/      #   유전알고리즘·자원배분
│   ├── nlp/               #   자연어 명령 파서
│   ├── models/            #   시뮬 모델 (전염병 SIR·저수지)
│   ├── risk/              #   위험도 점수
│   ├── generation/        #   절차적 배치 (줄/나선/원/격자)
│   ├── dataviz/           #   실시간 그래프
│   ├── tests/             #   순수 부품 자동 테스트 (47개)
│   ├── verify/            #   VPython 검증 스크립트 (오프라인·UI 데모)
│   ├── CATALOG.md         #   ⭐ 전체 함수 통합 인덱스 (여기부터 보기)
│   └── README.md          #   주제(A~G)별 부품 조합표
│
├── products/              # 🚀 완성품 = 실행 데모 (python main.py)
│   ├── A_safe_avoidance/      A안 — 무해한 AI 장애물 회피
│   ├── B_nl3d/                B안 — 자연어로 만드는 3D
│   ├── D_trust_visualizer/    D안 — AI 신뢰도(안전 판단) 시각화
│   ├── E_collab_bridge/       E안 — 인간-AI 협업 다리
│   ├── F_growth_tree/         F안 — 안전 경계 성장 나무
│   └── combined_adef/         통합안 — A+D+E+F 파이프라인
│
├── requirements.txt       # vpython, pytest
├── IDEAS_INDEX.md         # 아이디어 요약 + 실행법
└── STATUS.md              # 진행 체크리스트
```

## 빠른 시작
```bash
pip install -r requirements.txt

# 완성품 실행 (각 폴더 안에서)
cd products/combined_adef && python main.py

# 부품 로직 자동 검증 (vpython 불필요)
pytest parts/tests/ -q          # 47개 통과
```

## 어디를 볼까?
- **"이 기능(함수) 어디 있지?"** → [parts/CATALOG.md](parts/CATALOG.md)
- **"주제별로 어떤 부품 조합하지?"** → [parts/README.md](parts/README.md)
- **"완성품 어떻게 실행/뭐가 있지?"** → [products/](products/) 각 폴더의 HANDOFF.md
- **"뭐가 다 됐고 뭐가 남았지?"** → [STATUS.md](STATUS.md)

## 원칙
- **완제품이 아니라 부품 조립.** 대회장에서 주제 보고 `parts/`에서 골라 `products/`처럼 조립한다.
- `products/`의 main.py는 맨 위에서 `../../parts/<기능>`을 경로에 추가해 부품을 불러온다.
- 순수(알고리즘) 부품은 오프라인·pytest로 검증됨. VPython 부품은 실행해서 눈으로 확인.
