# SDG14_ocean_cleanup/main.py — 해양 청소 로봇 함대 (군집 flocking)
#
# SDG 14(해양) + 12(폐기물). 게임AI: 군집(Flocking) + seek.
# 청소로봇들이 무리 규칙(분리/정렬/응집)을 지키며 가장 가까운 플라스틱으로 이동해 수거.
# 탐구 포인트: "로봇 수"를 늘리면 수거 효율이 얼마나 좋아지나(창발적 협력).
#
# 실행: python main.py

import os
import sys
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import color, rate, vector, sphere, box
from vpython_utils import make_scene
from steering import flock, seek
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

# ============================================================
# 1. 설정
# ============================================================
AREA = 10.0                 # 바다 반경(정사각 -AREA~AREA)
NUM_ROBOTS = 6
NUM_PLASTIC = 40
ROBOT_SPEED = 0.12
COLLECT_R = 0.6             # 이 거리 안이면 수거
NEIGHBOR_R = 2.5            # 군집 이웃 인식 거리

num_robots = NUM_ROBOTS

# ============================================================
# 2. 씬
# ============================================================
scene = make_scene("SDG14 — 군집 AI 해양 청소 로봇", width=900, height=560)
scene.append_to_caption("<b>로봇들이 군집 규칙을 지키며 협력해 플라스틱을 수거</b>\n\n")
box(pos=vector(0, -0.6, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=vector(0.1, 0.3, 0.5))  # 바다


def on_robots(v):
    global num_robots
    num_robots = int(v)
    reset()


make_labeled_slider(1, 12, NUM_ROBOTS, on_robots, "로봇 수", length=300, decimals=0)
remaining_curve = make_line_curve("남은 플라스틱", "시간", "개수", col=color.red)

robots = []      # {obj, vel}
plastics = []    # sphere 객체들


def rand_pos():
    return vector(random.uniform(-AREA, AREA), 0, random.uniform(-AREA, AREA))


def reset():
    global robots, plastics, t
    for r in robots:
        r["obj"].visible = False
    for p in plastics:
        p.visible = False
    robots = []
    for _ in range(num_robots):
        robots.append({"obj": sphere(pos=rand_pos(), radius=0.35, color=color.cyan,
                                     make_trail=True, trail_radius=0.02),
                       "vel": vector(0, 0, 0)})
    plastics = [sphere(pos=rand_pos(), radius=0.18, color=color.orange) for _ in range(NUM_PLASTIC)]
    t = 0


t = 0
reset()

# ============================================================
# 3. 루프
# ============================================================
while True:
    rate(30)
    t += 1

    positions = [r["obj"].pos for r in robots]
    vels = [r["vel"] for r in robots]

    for i, r in enumerate(robots):
        pos = r["obj"].pos
        # 이웃(가까운 로봇들)만 골라 군집 방향
        nbr_pos, nbr_vel = [], []
        for j, other in enumerate(robots):
            if j != i and (other["obj"].pos - pos).mag < NEIGHBOR_R:
                nbr_pos.append(other["obj"].pos)
                nbr_vel.append(other["vel"])
        flock_dir = flock(pos, nbr_pos, nbr_vel, sep_radius=1.0, weights=(1.6, 0.8, 0.6))

        # 가장 가까운 플라스틱으로 향하는 방향(seek)
        target_dir = vector(0, 0, 0)
        if plastics:
            nearest = min(plastics, key=lambda p: (p.pos - pos).mag)
            target_dir = seek(pos, nearest.pos, 1.0)

        # 군집 + 목표를 섞어 이동
        direction = (target_dir * 1.2 + flock_dir * 0.8)
        if direction.mag > 0:
            direction = direction.norm()
        r["vel"] = direction
        newpos = pos + direction * ROBOT_SPEED
        # 바다 경계 안에 가두기
        newpos.x = max(-AREA, min(AREA, newpos.x))
        newpos.z = max(-AREA, min(AREA, newpos.z))
        r["obj"].pos = newpos

        # 수거 판정
        for p in list(plastics):
            if (p.pos - newpos).mag < COLLECT_R:
                p.visible = False
                plastics.remove(p)

    remaining_curve.plot(t, len(plastics))

    if not plastics:       # 전부 수거 → 리셋 반복
        remaining_curve.data = []
        reset()
