# SDG14_ocean_cleanup/main.py — 해양 청소 로봇 함대
#   군집(flocking) + 작업 분담 + 장애물(배·부표) 회피 + 조류에 떠다니는 쓰레기
#
# SDG 14(해양) + 12(폐기물). 청소로봇들이 무리 규칙을 지키며 '서로 다른' 쓰레기를 나눠 맡아
# 수거하고, 배와 부표는 피해 간다. 쓰레기는 조류를 따라 천천히 떠다닌다.
#
# 실행: python main.py

import os
import sys
import math
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import color, rate, vector, sphere, box, cylinder
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
AVOID_MARGIN = 1.6          # 장애물에 이만큼 가까우면 밀려남
DRIFT = 0.02                # 쓰레기가 조류에 떠다니는 세기

# 장애물: (중심, 반지름, 종류) — 종류 "ship"=배, "buoy"=부표
OBSTACLES = [(vector(0, 0, 0), 1.5, "ship"),
             (vector(5.5, 0, -4.5), 1.0, "buoy"),
             (vector(-5.5, 0, 4.5), 1.0, "buoy")]

num_robots = NUM_ROBOTS
sep_range = 1.0

# ============================================================
# 2. 씬 + 장애물 그리기(배·부표)
# ============================================================
scene = make_scene("SDG14 — 군집 AI 해양 청소 로봇", width=900, height=560)
scene.append_to_caption("<b>로봇들이 협력해 떠다니는 쓰레기를 나눠 수거(배·부표는 회피)</b>\n\n")
box(pos=vector(0, -0.6, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=vector(0.1, 0.3, 0.5))  # 바다


def draw_ship(c):
    box(pos=c + vector(0, 0.25, 0), size=vector(2.6, 0.5, 1.1), color=vector(0.55, 0.1, 0.1))  # 붉은 선체
    box(pos=c + vector(0, 0.55, 0), size=vector(2.1, 0.2, 0.8), color=color.white)             # 갑판
    box(pos=c + vector(-0.6, 0.9, 0), size=vector(0.7, 0.6, 0.6), color=color.gray(0.6))       # 선실


def draw_buoy(c):
    sphere(pos=c + vector(0, 0.3, 0), radius=0.6, color=color.yellow)                # 부표 몸통
    cylinder(pos=c + vector(0, 0.3, 0), axis=vector(0, 1.1, 0), radius=0.06, color=color.gray(0.7))  # 기둥
    sphere(pos=c + vector(0, 1.4, 0), radius=0.16, color=color.red)                  # 위 표시등


for op, orad, kind in OBSTACLES:
    (draw_ship if kind == "ship" else draw_buoy)(op)


def on_robots(v):
    global num_robots
    num_robots = int(v)
    reset()


def on_sep(v):
    global sep_range
    sep_range = v


make_labeled_slider(1, 12, NUM_ROBOTS, on_robots, "로봇 수", length=300, decimals=0)
make_labeled_slider(0.5, 4.0, sep_range, on_sep, "충돌 회피 범위(로봇 간격)", length=300, decimals=1)
remaining_curve = make_line_curve("남은 쓰레기", "시간", "개수", col=color.red)

robots = []      # {obj, vel}
plastics = []    # {obj, vel, phase}


def rand_pos():
    while True:
        p = vector(random.uniform(-AREA, AREA), 0, random.uniform(-AREA, AREA))
        if all((p - op).mag > orad + 0.8 for op, orad, _ in OBSTACLES):
            return p


def reset():
    global robots, plastics, t
    for r in robots:
        r["obj"].visible = False
    for p in plastics:
        p["obj"].visible = False
    robots = []
    for _ in range(num_robots):
        robots.append({"obj": sphere(pos=rand_pos(), radius=ROBOT_R, color=color.cyan,
                                     make_trail=True, trail_radius=0.02),
                       "vel": vector(0, 0, 0)})
    plastics = []
    for _ in range(NUM_PLASTIC):
        pos = rand_pos()
        pos.y = 0.18
        plastics.append({"obj": sphere(pos=pos, radius=0.18, color=color.orange),
                         "vel": vector(0, 0, 0), "phase": random.uniform(0, 6.28)})
    t = 0


def repulsion(pos):
    a = vector(0, 0, 0)
    for op, orad, _ in OBSTACLES:
        diff = pos - op
        d = diff.mag
        reach = orad + AVOID_MARGIN
        if 0 < d < reach:
            a = a + diff.norm() * ((reach - d) / reach)
    return a


def push_out(p):
    """장애물 안으로 못 들어가게 바깥으로 밀어냄."""
    for op, orad, _ in OBSTACLES:
        diff = p - op
        d = diff.mag
        mind = orad + 0.3
        if 0 < d < mind:
            p = op + diff.norm() * mind
    return p


t = 0
reset()

# ============================================================
# 3. 루프
# ============================================================
while True:
    rate(30)
    t += 1

    # 3-0. 쓰레기가 조류를 따라 천천히 떠다니고 물결에 바동거림
    current = vector(math.cos(t * 0.008), 0, math.sin(t * 0.008))   # 완만히 도는 조류
    for p in plastics:
        p["vel"] = p["vel"] * 0.9 + (current * DRIFT
                                     + vector(random.uniform(-1, 1), 0, random.uniform(-1, 1)) * 0.006)
        np = p["obj"].pos + p["vel"]
        np.x = max(-AREA, min(AREA, np.x))
        np.z = max(-AREA, min(AREA, np.z))
        np = push_out(np)
        np.y = 0.18 + 0.06 * math.sin(t * 0.12 + p["phase"])         # 물결 바동
        p["obj"].pos = np

    claimed = set()      # 이번 프레임에 이미 배정된 쓰레기(중복 방지)

    for i, r in enumerate(robots):
        pos = r["obj"].pos

        # 이웃 로봇으로 군집(충돌 회피 범위는 슬라이더로 조절)
        perceive = max(NEIGHBOR_R, sep_range)
        nbr_pos, nbr_vel = [], []
        for j, other in enumerate(robots):
            if j != i and (other["obj"].pos - pos).mag < perceive:
                nbr_pos.append(other["obj"].pos)
                nbr_vel.append(other["vel"])
        flock_dir = flock(pos, nbr_pos, nbr_vel, sep_radius=sep_range, weights=(2.0, 0.3, 0.2))

        # 작업 분담: 아직 아무도 안 맡은 '가장 가까운' 쓰레기를 맡는다
        target = None
        best_d = float("inf")
        for p in plastics:
            if p["obj"] in claimed:
                continue
            dd = (p["obj"].pos - pos).mag
            if dd < best_d:
                best_d, target = dd, p
        if target is None and plastics:
            target = min(plastics, key=lambda pp: (pp["obj"].pos - pos).mag)
        target_dir = vector(0, 0, 0)
        if target is not None:
            claimed.add(target["obj"])
            target_dir = seek(pos, target["obj"].pos, 1.0)

        # 목표 + 군집 + 장애물 회피
        direction = target_dir * 1.3 + flock_dir * 0.5 + repulsion(pos) * 2.5
        if direction.mag > 0:
            direction = direction.norm()
        r["vel"] = direction
        newpos = pos + direction * ROBOT_SPEED
        newpos.x = max(-AREA, min(AREA, newpos.x))
        newpos.z = max(-AREA, min(AREA, newpos.z))
        newpos = push_out(newpos)
        r["obj"].pos = newpos

        # 수거 판정
        for p in list(plastics):
            if (p["obj"].pos - newpos).mag < COLLECT_R:
                p["obj"].visible = False
                plastics.remove(p)

    remaining_curve.plot(t, len(plastics))

    if not plastics:       # 전부 수거 → 리셋 반복
        remaining_curve.data = []
        reset()
