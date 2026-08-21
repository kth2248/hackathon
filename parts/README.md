# parts — 기능별 부품 라이브러리 (대회장 조립용)

> 완제품이 아니라 **부품 하나하나**. 대회장에서 주제 정해지면 필요한 부품만 골라 조립한다.
> 완성품(실행 데모)은 `../products/`에 따로 모여 있다. VPython 씬/UI/벡터 부품은
> 이 라이브러리의 `vectors/` `scene/` `ui/` 폴더에 있다(예전 hackathon_kit).

## 폴더 = 기능 종류

| 폴더/파일 | 기능 | vpython 필요? | 핵심 함수 |
|---|---|:---:|---|
| `vectors/vector_helpers.py` | 벡터 수학(방향/거리/회피/우회/혼합) | ✅ vector | `direction_to`, `distance`, `avoid_vector`, `steer_around`, `blend_vectors`, `clamp_speed` |
| `scene/vpython_utils.py` | 3D 씬·객체 생성 | ✅ vpython | `make_scene`, `make_agent`, `make_obstacle`, `make_floor` |
| `scene/grid_render.py` | 격자를 3D로(바닥·장애물·칸좌표) | ✅ vpython | `cell_pos`, `render_floor`, `render_obstacles` |
| `ui/ui_widgets.py` | 슬라이더·토글 UI | ✅ vpython | `make_labeled_slider`, `make_toggle` |
| `pathfinding/astar.py` | A* 최단경로(게임AI 길찾기) | ❌ 순수 | `astar(start, goal, passable, diagonal)` |
| `world/grid.py` | 격자 맵·장애물·좌표변환 | ❌ 순수 | `GridWorld(cols, rows)` , `.passable`, `.cell_to_world` |
| `steering/steering.py` | 이동·군집(seek/arrive/flocking) | ✅ vector | `seek`, `arrive`, `separation`, `alignment`, `cohesion`, `flock` |
| `optimization/genetic.py` | 유전알고리즘 최적화 | ❌ 순수 | `genetic_optimize(create, fitness, mutate)` |
| `optimization/allocate.py` | 자원 배분 | ❌ 순수 | `proportional_allocate`, `greedy_allocate`, `satisfaction` |
| `nlp/command_parser.py` | 자연어 명령 파서(NLP) | ❌ 순수 | `extract_count`, `extract_keyword`, `extract_all_counts` |
| `models/epidemic.py` | 전염병 SIR 모델 | ❌ 순수 | `infect_step`, `counts` |
| `models/resource.py` | 저수지/자원 수급 | ❌ 순수 | `reservoir_step`, `shortage` |
| `risk/risk.py` | 위험도 점수(위치 위험 0~100) | ❌ 순수 | `risk_score` |
| `generation/patterns.py` | 절차적 배치(줄/나선/원/격자) | ❌ 순수 | `line/spiral/circle/grid_positions` |
| `dataviz/live_graph.py` | 실시간 그래프(결과 정량화) | ✅ graph | `make_line_curve`, `make_bars` |

> 📚 **hackathon_kit까지 포함한 전체 함수 목록은 [CATALOG.md](CATALOG.md)** 참고 (기능별 통합 인덱스).

> **순수(❌) 부품**은 vpython 없이 돌아가고 `pytest`로 자동 검증됨 → 로직이 보장됨.
> **vpython(✅) 부품**은 화면 표시용이라 실행해서 눈으로 확인.

## 주제(A~G) → 부품 조합표

| 주제 | 조립 부품 (parts) + hackathon_kit |
|---|---|
| **A 대피** | `grid` + `astar` + `steering(separation)` + `dataviz` + kit(scene/agent/slider) |
| **B 탄소 숲** | `optimization/genetic` + `dataviz` + kit(scene/slider) + F안 성장나무 |
| **C 물 분배** | `models/resource` + `optimization/allocate` + `dataviz` + kit |
| **D 로봇 함대** | `astar` + `steering(flock)` + `grid` + `dataviz` + kit |
| **E 에너지 도시** | `optimization/genetic` + `models/resource` + `dataviz` + kit(협업건설) |
| **F 말로 짓기** | `nlp/command_parser` + kit(scene) + B_nl3d(생성/배치) |
| **G 전염병** | `models/epidemic` + `steering(seek)` + `dataviz` + kit(agent) |

## 조립 예시 — A 대피 시뮬레이터 (products/ 안의 main.py 기준)
```python
import os, sys
_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "world", "pathfinding", "steering", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from grid import GridWorld            # 도시 격자
from astar import astar               # 각 사람이 출구까지 최단경로
from steering import separation       # 사람끼리 안 부딪힘
from live_graph import make_line_curve
from vpython_utils import make_scene, make_agent   # scene 부품
from ui_widgets import make_labeled_slider          # ui 부품

world = GridWorld(20, 20)
# world.block((x,y))로 벽 배치
path = astar(start_cell, exit_cell, world.passable)   # AI 경로탐색
# path의 각 칸을 world.cell_to_world로 3D 좌표 변환해 에이전트를 이동
```

## 테스트 방법
```bash
# 순수 부품 로직 자동 검증 (vpython 불필요)
cd parts
pytest tests/test_parts.py -v          # 18개 통과 확인

# vpython 부품(steering, live_graph)은 실제 주제 main.py에 조립해 눈으로 확인
```

## 부품 쓰는 법 (2가지)
1. **경로 추가**: 위 예시처럼 필요한 폴더를 `sys.path`에 넣고 import (원본 유지, 권장)
2. **복사**: 부품 파일 하나를 main.py 옆에 복사해서 import (경로 신경 안 쓰고 싶을 때)
