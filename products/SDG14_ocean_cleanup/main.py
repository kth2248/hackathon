# SDG14_ocean_cleanup/main.py — 해양 청소 로봇 함대 (군집 flocking + 작업 분담 + 장애물 회피)
#
# SDG 14(해양) + 12(폐기물). 게임AI: 군집(Flocking) + seek + 작업 분담 + 회피.
# 청소로봇들이 무리 규칙을 지키며, '서로 다른' 플라스틱을 나눠 맡아 수거하고, 바위는 피해 간다.
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
AREA = 10.0
NUM_ROBOTS = 6
NUM_PLASTIC = 40
ROBOT_SPEED = 0.12
COLLECT_R = 0.6
NEIGHBOR_R = 2.5
ROBOT_R = 0.35

# 장애물(바위): (중심, 반지름)
OBSTACLES = [(vector(0, 0, 0), 1.5),
             (vector(5.5, 0, -4.5), 1.1),
             (vector(-5.5, 0, 4.5), 1.1)]
AVOID_MARGIN = 1.6          # 이 거리 안에 들어오면 밀려남

num_robots = NUM_ROBOTS

# ============================================================
# 2. 씬
# ============================================================
scene = make_scene("SDG14 — 군집 AI 해양 청소 로봇", width=900, height=560)
scene.append_to_caption("<b>로봇들이 협력하며 '서로 다른' 플라스틱을 나눠 맡아 수거(바위는 회피)</b>\n\n")
box(pos=vector(0, -0.6, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=vector(0.1, 0.3, 0.5))  # 바다
# 바위 그리기
for op, orad in OBSTACLES:
    sphere(pos=op, radius=orad, color=color.gray(0.5))


def on_robots(v):
    global num_robots
    num_robots = int(v)
    reset()


make_labeled_slider(1, 12, NUM_ROBOTS, on_robots, "로봇 수", length=300, decimals=0)
remaining_curve = make_line_curve("남은 플라스틱", "시간", "개수", col=color.red)

robots = []      # {obj, vel}
plastics = []    # sphere 객체들


def rand_pos():
    """바위와 겹치지 않는 임의 위치."""
    while True:
        p = vector(random.uniform(-AREA, AREA), 0, random.uniform(-AREA, AREA))
        if all((p - op).mag > orad + 0.8 for op, orad in OBSTACLES):
            return p


def reset():
    global robots, plastics, t
    for r in robots:
        r["obj"].visible = False
    for p in plastics:
        p.visible = False
    robots = []
    for _ in range(num_robots):
        robots.append({"obj": sphere(pos=rand_pos(), radius=ROBOT_R, color=color.cyan,
                                     make_trail=True, trail_radius=0.02),
                       "vel": vector(0, 0, 0)})
    plastics = [sphere(pos=rand_pos(), radius=0.18, color=color.orange) for _ in range(NUM_PLASTIC)]
    t = 0


def repulsion(pos):
    """바위에서 밀려나는 방향(가까울수록 강함)."""
    a = vector(0, 0, 0)
    for op, orad in OBSTACLES:
        diff = pos - op
        d = diff.mag
        reach = orad + AVOID_MARGIN
        if 0 < d < reach:
            a = a + diff.norm() * ((reach - d) / reach)
    return a


t = 0
reset()

# ============================================================
# 3. 루프
# ============================================================
while True:
    rate(30)
    t += 1

    claimed = set()      # 이번 프레임에 이미 배정된 플라스틱(중복 방지)

    for i, r in enumerate(robots):
        pos = r["obj"].pos

        # 이웃 로봇으로 군집 방향(주로 충돌 방지용 분리 위주)
        nbr_pos, nbr_vel = [], []
        for j, other in enumerate(robots):
            if j != i and (other["obj"].pos - pos).mag < NEIGHBOR_R:
                nbr_pos.append(other["obj"].pos)
                nbr_vel.append(other["vel"])
        flock_dir = flock(pos, nbr_pos, nbr_vel, sep_radius=1.0, weights=(2.0, 0.3, 0.2))

        # 작업 분담: 아직 아무도 안 맡은 '가장 가까운' 플라스틱을 이 로봇이 맡는다
        target = None
        best_d = float("inf")
        for p in plastics:
            if p in claimed:
                continue
            dd = (p.pos - pos).mag
            if dd < best_d:
                best_d, target = dd, p
        if target is None and plastics:      # 남은 게 다 배정됨(로봇이 더 많음) → 가장 가까운 것
            target = min(plastics, key=lambda p: (p.pos - pos).mag)
        target_dir = vector(0, 0, 0)
        if target is not None:
            claimed.add(target)
            target_dir = seek(pos, target.pos, 1.0)

        # 목표 + 군집 + 바위 회피를 섞어 이동 방향
        direction = target_dir * 1.3 + flock_dir * 0.5 + repulsion(pos) * 2.5
        if direction.mag > 0:
            direction = direction.norm()
        r["vel"] = direction
        newpos = pos + direction * ROBOT_SPEED

        # 바다 경계 안에 가두기
        newpos.x = max(-AREA, min(AREA, newpos.x))
        newpos.z = max(-AREA, min(AREA, newpos.z))
        # 바위 안으로 못 들어가게 밀어내기(하드 제약)
        for op, orad in OBSTACLES:
            diff = newpos - op
            d = diff.mag
            mind = orad + ROBOT_R
            if 0 < d < mind:
                newpos = op + diff.norm() * mind
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
