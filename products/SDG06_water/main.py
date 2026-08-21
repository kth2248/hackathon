# SDG06_water/main.py — 가뭄 속 물 분배 대시보드 (자원배분 + 저수지)
#
# SDG 6(깨끗한 물) + 2(농업용수) + 13(가뭄). 부품: allocate + resource.
# 저수지 물을 농업/식수/공업에 분배한다. 강수량이 줄면 어디가 먼저 위험해지나.
# 탐구 포인트: "농업 우선도"를 높이면 식수/공업 만족도가 어떻게 희생되나(트레이드오프).
#
# 실행: python main.py

import os
import sys
import math

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import color, rate, vector, box, sphere, label
from vpython_utils import make_scene
from allocate import proportional_allocate, satisfaction
from resource import reservoir_step
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve, make_bars

# ============================================================
# 1. 설정
# ============================================================
CAPACITY = 100.0
SECTORS = ["농업", "식수", "공업"]
BASE_DEMAND = [6.0, 4.0, 3.0]       # 부문별 기본 수요
SECTOR_COLORS = [color.green, color.cyan, color.orange]

level = 60.0
agri_weight = 1.0
rain = 6.0                          # 평균 유입(강수량)

# ============================================================
# 2. 씬 + UI
# ============================================================
scene = make_scene("SDG06 — 물 분배 대시보드", width=900, height=560)
scene.append_to_caption("<b>제한된 물을 농업·식수·공업에 분배. 부문 만족도의 트레이드오프를 관찰</b>\n\n")


def on_agri(v):
    global agri_weight
    agri_weight = v


def on_rain(v):
    global rain
    rain = v


make_labeled_slider(0.2, 3.0, agri_weight, on_agri, "농업 우선도", length=300, decimals=1)
make_labeled_slider(1.0, 12.0, rain, on_rain, "강수량(평균 유입)", length=300, decimals=1)
level_curve = make_line_curve("저수지 수위", "시간", "수위", col=color.blue)
sat_bars = make_bars("부문별 만족도(0~1)", "부문(0농 1식 2공)", "만족도", col=color.green)

# 저수지 3D(수위에 따라 높이 변함)
water = box(pos=vector(-4, 0, 0), size=vector(3, level / 20, 3), color=color.blue, opacity=0.6)
tank = box(pos=vector(-4, 0, 0), size=vector(3.2, CAPACITY / 20, 3.2), color=color.gray(0.4), opacity=0.15)
# 부문 표시 구(만족도에 따라 초록~빨강)
sector_balls = [sphere(pos=vector(0 + i * 2.2, 0, 0), radius=0.6, color=SECTOR_COLORS[i])
                for i in range(3)]
sector_labels = [label(pos=vector(0 + i * 2.2, 1.2, 0), text=SECTORS[i], box=False, height=14)
                 for i in range(3)]

# ============================================================
# 3. 루프
# ============================================================
t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1

    # 계절 유입(강수량 주위로 sin 변동) — 가뭄기엔 유입이 확 줄어듦
    inflow = max(0.0, rain + rain * 0.6 * math.sin(t * 0.15))

    # 가중 수요: 농업에 우선도 반영
    weighted = [BASE_DEMAND[0] * agri_weight, BASE_DEMAND[1], BASE_DEMAND[2]]
    total_demand = sum(weighted)

    # 저수지에서 뽑을 수 있는 양 = 수위와 수요 중 작은 값
    supply = min(level, total_demand)
    alloc = proportional_allocate(supply, weighted)
    sats = [satisfaction(alloc[i], BASE_DEMAND[i]) for i in range(3)]

    # 저수지 갱신
    level = reservoir_step(level, inflow, supply, capacity=CAPACITY)

    # 시각화 갱신
    water.size = vector(3, max(0.02, level / 20), 3)
    water.pos = vector(-4, -CAPACITY / 40 + level / 40, 0)
    for i in range(3):
        s = sats[i]
        sector_balls[i].color = vector(1 - s, s, 0)   # 빨강(부족)~초록(충분)
    level_curve.plot(t, level)
    sat_bars.data = [[i, sats[i]] for i in range(3)]
