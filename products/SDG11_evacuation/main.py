# SDG11_evacuation/main.py — 재난 대피 시뮬레이터 (A* 경로탐색)
#
# SDG 11(지속가능한 도시) + 13(재난). 게임AI: A* 길찾기.
# 사람들이 벽을 피해 가장 가까운 출구로 스스로 최단경로를 찾아 대피한다.
# 탐구 포인트: "출구 개수"를 바꾸면 대피 시간이 얼마나 달라지나.
#
# 실행: python main.py

import os
import sys
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import color, rate
from vpython_utils import make_scene, make_agent
from grid import GridWorld
from grid_render import render_floor, render_obstacles, cell_pos
from astar import astar, path_length
from ui_widgets import make_labeled_slider, make_toggle
from live_graph import make_line_curve

# ============================================================
# 1. 설정 + 격자
# ============================================================
COLS, ROWS = 18, 18
NUM_PEOPLE = 20
WALL = [(9, r) for r in range(3, 15)]          # 가운데 세로 벽
EXIT_RIGHT = (17, 9)
EXIT_LEFT = (0, 9)

speed = 6.0
two_exits = True

world = GridWorld(COLS, ROWS)
for c in WALL:
    world.block(c)

scene = make_scene("SDG11 — A* 재난 대피 시뮬레이터", width=900, height=560)
scene.append_to_caption("<b>사람들이 A* 경로탐색으로 가장 가까운 출구로 대피</b>\n\n")
render_floor(world)
render_obstacles(world, obstacle_color=color.gray(0.5))

# 출구 표시(초록)
exit_markers = [make_agent(pos=cell_pos(world, EXIT_RIGHT, y=0.3), radius=0.5,
                           agent_color=color.green, trail=False),
                make_agent(pos=cell_pos(world, EXIT_LEFT, y=0.3), radius=0.5,
                           agent_color=color.green, trail=False)]


def current_exits():
    return [EXIT_RIGHT, EXIT_LEFT] if two_exits else [EXIT_RIGHT]


def on_speed(v):
    global speed
    speed = v


def on_exits(c):
    global two_exits
    two_exits = c
    exit_markers[1].visible = c
    reset()


make_labeled_slider(1, 10, speed, on_speed, "대피 속도", length=300, decimals=0)
make_toggle("출구 2개 (양쪽)", "출구 1개 (오른쪽만)", on_exits, initial=True, checkbox_text="출구 2개")
remaining_curve = make_line_curve("아직 대피 못한 인원", "시간", "인원", col=color.red)

# ============================================================
# 2. 사람 에이전트
# ============================================================
people = []


def free_cell():
    while True:
        c = (random.randrange(COLS), random.randrange(ROWS))
        if world.passable(c) and c not in current_exits():
            return c


def plan_path(cell):
    """여러 출구 중 A* 경로가 가장 짧은 출구로 가는 경로."""
    best = []
    best_len = float("inf")
    for ex in current_exits():
        p = astar(cell, ex, world.passable)
        if p and path_length(p) < best_len:
            best_len, best = path_length(p), p
    return best


def reset():
    global people, t
    for pr in people:
        pr["obj"].visible = False
    people = []
    for _ in range(NUM_PEOPLE):
        c = free_cell()
        obj = make_agent(pos=cell_pos(world, c, y=0.35), radius=0.35,
                         agent_color=color.cyan, trail=False)
        people.append({"obj": obj, "cell": c, "path": [], "done": False})
    t = 0


t = 0
reset()

# ============================================================
# 3. 루프
# ============================================================
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % max(1, int(11 - speed)) != 0:
        continue
    t += 1

    active = 0
    for pr in people:
        if pr["done"]:
            continue
        # A*: 경로가 없으면 새로 계산
        if not pr["path"] or len(pr["path"]) < 2:
            pr["path"] = plan_path(pr["cell"])
        # 경로 따라 한 칸 이동
        if pr["path"] and len(pr["path"]) >= 2:
            pr["cell"] = pr["path"][1]
            pr["path"] = pr["path"][1:]
            pr["obj"].pos = cell_pos(world, pr["cell"], y=0.35)
        if pr["cell"] in current_exits():
            pr["done"] = True
            pr["obj"].visible = False
        else:
            active += 1

    remaining_curve.plot(t, active)

    if active == 0:      # 전원 대피 완료 → 리셋 후 반복 시연
        remaining_curve.data = []
        reset()
