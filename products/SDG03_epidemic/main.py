# SDG03_epidemic/main.py — 전염병 확산·방역 시뮬레이터 (SIR 모델)
#
# SDG 3(건강과 웰빙) + 11(도시). 에이전트 기반 SIR.
# 사람들이 돌아다니며 접촉으로 감염(S->I)되고 회복(I->R)한다.
# 탐구 포인트: "거리두기(이동 억제)"와 "백신(초기 면역)"이 곡선을 얼마나 낮추나.
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
from epidemic import infect_step, counts
from ui_widgets import make_labeled_slider, make_toggle
from live_graph import make_lines

# ============================================================
# 1. 설정
# ============================================================
AREA = 9.0
N = 60
CONTACT_R = 0.9        # 이 거리 안이면 접촉
P_INFECT = 0.25
P_RECOVER = 0.02

move_scale = 0.06      # 이동량(거리두기 슬라이더로 조절)
vaccinate = False

COL = {"S": color.blue, "I": color.red, "R": color.gray(0.6)}

# ============================================================
# 2. 씬 + UI
# ============================================================
scene = make_scene("SDG03 — 전염병 확산·방역 (SIR)", width=900, height=560)
scene.append_to_caption("<b>접촉으로 감염(빨강), 시간이 지나면 회복(회색). 거리두기·백신 효과를 관찰</b>\n\n")
box(pos=vector(0, -0.6, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=color.gray(0.25))


def on_distancing(v):
    global move_scale
    move_scale = v


def on_vaccine(c):
    global vaccinate
    vaccinate = c
    reset()


make_labeled_slider(0.0, 0.12, move_scale, on_distancing, "이동량(작을수록 강한 거리두기)",
                    length=320, decimals=3)
make_toggle("백신: ON (30% 초기 면역)", "백신: OFF", on_vaccine, initial=False, checkbox_text="백신")
S_c, I_c, R_c = make_lines("감염 곡선", "시간", "인원",
                           [("S(취약)", color.blue), ("I(감염)", color.red), ("R(회복)", color.gray(0.6))])

# ============================================================
# 3. 사람 에이전트
# ============================================================
people = []      # {obj, vel}
states = []      # 'S'/'I'/'R'


def rand_pos():
    return vector(random.uniform(-AREA, AREA), 0.3, random.uniform(-AREA, AREA))


def reset():
    global people, states, t
    for p in people:
        p["obj"].visible = False
    people, states = [], []
    for i in range(N):
        obj = sphere(pos=rand_pos(), radius=0.25, color=COL["S"])
        vel = vector(random.uniform(-1, 1), 0, random.uniform(-1, 1)).norm()
        people.append({"obj": obj, "vel": vel})
        # 초기 상태: 백신이면 30% 면역(R), 그 외 취약(S)
        if vaccinate and random.random() < 0.3:
            states.append("R")
        else:
            states.append("S")
    # 감염자 2명 심기(취약자 중에서)
    seeds = [i for i, s in enumerate(states) if s == "S"]
    for i in random.sample(seeds, min(2, len(seeds))):
        states[i] = "I"
    for i, s in enumerate(states):
        people[i]["obj"].color = COL[s]
    t = 0


t = 0
reset()


def neighbors_of(i):
    pi = people[i]["obj"].pos
    return [j for j in range(N) if j != i and (people[j]["obj"].pos - pi).mag < CONTACT_R]


# ============================================================
# 4. 루프
# ============================================================
frame = 0
while True:
    rate(30)
    frame += 1

    # 이동(랜덤 워크 + 벽 반사)
    for p in people:
        pos = p["obj"].pos + p["vel"] * move_scale
        if abs(pos.x) > AREA:
            p["vel"].x *= -1
        if abs(pos.z) > AREA:
            p["vel"].z *= -1
        pos.x = max(-AREA, min(AREA, pos.x))
        pos.z = max(-AREA, min(AREA, pos.z))
        p["obj"].pos = pos

    # 감염 갱신(몇 프레임마다 한 스텝)
    if frame % 5 == 0:
        global_states = infect_step(states, neighbors_of, P_INFECT, P_RECOVER)
        states = global_states
        for i, s in enumerate(states):
            people[i]["obj"].color = COL[s]
        t += 1
        S, I, R = counts(states)
        S_c.plot(t, S)
        I_c.plot(t, I)
        R_c.plot(t, R)

        if I == 0:      # 유행 종료 → 리셋 반복
            for c in (S_c, I_c, R_c):
                c.data = []
            reset()
