# TEMPLATE_sdg_base/main.py — 공용 뼈대 (에이전트 + 격자맵 + 실시간 그래프)
#
# 어떤 SDG가 나와도 이 뼈대 위에 '주제 로직'만 얹으면 된다.
# 지금 상태로도 실행됨(에이전트가 랜덤 워크). ①②③ 표시된 곳만 바꾸면 주제별 시뮬이 된다.
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작)
#
# 조립된 부품: scene(make_scene/make_agent) + world(GridWorld) + scene/grid_render +
#             ui(슬라이더/토글) + dataviz(실시간 그래프)

import os
import sys
import math
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import color, rate
from vpython_utils import make_scene, make_agent            # scene 부품
from ui_widgets import make_labeled_slider, make_toggle     # ui 부품
from grid import GridWorld                                  # world 부품
from grid_render import render_floor, render_obstacles, cell_pos  # scene/grid_render 부품
from live_graph import make_line_curve                      # dataviz 부품
# 필요하면 추가로 조립:
# from astar import astar            # 경로탐색(대피/인프라)
# from steering import flock         # 군집(해양 로봇)
# from genetic import genetic_optimize   # 최적화(에너지/숲)
# from epidemic import infect_step, counts   # 전염병
# from allocate import proportional_allocate # 자원배분

# ============================================================
# 1. 설정값
# ============================================================
COLS, ROWS = 16, 16
NUM_AGENTS = 12
OBSTACLE_CELLS = [(7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (4, 10), (10, 10)]  # 예시 벽

# ============================================================
# 2. 상태 + 콜백
# ============================================================
speed = 5.0          # 이동 속도(=몇 프레임마다 한 칸 이동)
running = True


def on_speed(v):
    global speed
    speed = v


def on_run(c):
    global running
    running = c


# ============================================================
# 3. 씬 + 격자 + UI + 그래프 (부품 조립)
# ============================================================
scene = make_scene("공용 뼈대 — 에이전트 + 격자맵 + 그래프", width=900, height=560)
scene.append_to_caption("<b>이 뼈대 위에 SDG 주제 로직만 얹으면 된다</b>\n\n")

world = GridWorld(COLS, ROWS)
for cell in OBSTACLE_CELLS:
    world.block(cell)

render_floor(world)
render_obstacles(world)

make_labeled_slider(1, 10, speed, on_speed, "속도", length=300, decimals=0)
make_toggle("실행: ON", "실행: 일시정지", on_run, initial=True, checkbox_text="실행")
metric_curve = make_line_curve("지표(예: 중심까지 평균거리)", "시간", "값")


def free_cell():
    """장애물이 아닌 임의의 칸."""
    while True:
        cell = (random.randrange(COLS), random.randrange(ROWS))
        if world.passable(cell):
            return cell


# 에이전트 생성 (격자 위). 각 에이전트는 {obj, cell} 딕셔너리로 관리.
agents = []
for _ in range(NUM_AGENTS):
    c = free_cell()
    obj = make_agent(pos=cell_pos(world, c, y=0.35), radius=0.35,
                     agent_color=color.cyan, trail=False)
    agents.append({"obj": obj, "cell": c})

CENTER = (COLS / 2, ROWS / 2)

# ============================================================
# 4. 애니메이션 루프
# ============================================================
t = 0
frame = 0
while True:
    rate(30)
    if not running:
        continue
    frame += 1

    # 속도: speed가 클수록 자주 한 칸 이동
    hop = (frame % max(1, int(11 - speed)) == 0)
    if not hop:
        continue
    t += 1

    # ── ① 여기에 '각 에이전트를 어떻게 움직일지'를 채운다 ─────────────────
    #    지금은 예시로 '랜덤 워크'. 주제에 맞게 아래를 교체:
    #      · 대피(11)/인프라(9): astar로 목표까지 경로 따라가기
    #      · 해양(14):          steering.flock로 군집 협력
    #      · 전염병(3):         infect_step로 상태 갱신 + 접촉 이동
    for a in agents:
        cx, cy = a["cell"]
        nbrs = [(cx + dx, cy + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if world.passable((cx + dx, cy + dy))]
        if nbrs:
            a["cell"] = random.choice(nbrs)
            a["obj"].pos = cell_pos(world, a["cell"], y=0.35)
    # ────────────────────────────────────────────────────────────────

    # ── ② 여기에 '그래프에 무엇을 그릴지'를 채운다 ──────────────────────
    #    지금은 예시로 '중심까지 평균 거리'. 주제 지표로 교체:
    #      · 대피: 아직 못 나간 사람 수 / 해양: 남은 쓰레기 / 전염병: 감염자 수 ...
    metric = sum(math.hypot(a["cell"][0] - CENTER[0], a["cell"][1] - CENTER[1])
                 for a in agents) / len(agents)
    metric_curve.plot(t, metric)
    # ────────────────────────────────────────────────────────────────

    # ── ③ (선택) 리셋/종료 조건을 여기에 ───────────────────────────────
    #    예: 모두 목표 도착하면 초기화하고 반복 시연
    # ────────────────────────────────────────────────────────────────
