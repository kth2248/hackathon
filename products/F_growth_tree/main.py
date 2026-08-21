# F안 — 안전 경계 안에서 자라는 성장 나무
#
# 컨셉: 가지가 프랙탈처럼 계속 뻗어 나가되(무한한 상상), 투명한 '안전 경계' 구에 닿으려 하면
#       방향을 안쪽으로 꺾어 경계 밖으로 나가지 않는다(무해함). 경계 크기를 슬라이더로 조절.
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작)
#
# 재사용 부품: vpython_utils(make_scene) / ui_widgets(make_labeled_slider)

import os
import sys
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import sphere, cylinder, vector, color, rate
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider

# ============================================================
# 1. 설정값
# ============================================================
SAFE_RADIUS_INIT = 4.0
GROWTH_SPEED = 0.05
BRANCH_PROB = 0.02        # 매 스텝 새 가지가 갈라질 확률
MAX_TIPS = 40             # 동시에 자라는 가지 끝 개수 상한(성능)
MAX_BRANCHES = 1500       # 화면에 남기는 가지(cylinder) 최대 개수 → 넘으면 오래된 것부터 숨김

# ============================================================
# 2. 상태 + 콜백
# ============================================================
safe_radius = SAFE_RADIUS_INIT


def set_radius(v):
    global safe_radius
    safe_radius = v


# ============================================================
# 3. 씬 + UI
# ============================================================
scene = make_scene("F안 — 안전 경계 안에서 자라는 나무", width=900, height=550)
scene.append_to_caption("<b>무한한 상상(성장) × 무해함(안전 경계 안에 머무름)</b>\n\n")

make_labeled_slider(1, 6, SAFE_RADIUS_INIT, set_radius, "안전 경계 반지름", length=300, decimals=1)

# 투명한 안전 경계(구)
boundary = sphere(pos=vector(0, 0, 0), radius=SAFE_RADIUS_INIT, color=color.cyan, opacity=0.15)

# 가지 끝점들: 각각 (현재 위치, 성장 방향)
tips = [{"pos": vector(0, 0, 0), "dir": vector(0, 1, 0)}]
branches = []   # 그려진 가지(cylinder)

# ============================================================
# 4. 성장 루프
# ============================================================
while True:
    rate(60)
    boundary.radius = safe_radius   # 경계 크기 실시간 반영

    new_tips = []
    for tip in tips:
        # 방향을 살짝 랜덤하게 흔들어 자연스러운 성장
        wobble = vector(random.uniform(-0.1, 0.1),
                        random.uniform(-0.1, 0.1),
                        random.uniform(-0.1, 0.1))
        direction = (tip["dir"] + wobble).norm()
        next_pos = tip["pos"] + direction * GROWTH_SPEED

        # 안전 경계를 벗어나려 하면 원점 방향으로 꺾어 안에 머물게 함
        redirected = False
        if next_pos.mag > safe_radius:
            inward = (vector(0, 0, 0) - next_pos).norm()
            direction = (direction + inward * 0.8).norm()
            next_pos = tip["pos"] + direction * GROWTH_SPEED
            redirected = True

        # 꺾인 순간은 빨강(제약 작동), 평소는 초록
        branch_color = color.red if redirected else color.green
        branches.append(cylinder(pos=tip["pos"], axis=next_pos - tip["pos"],
                                 radius=0.03, color=branch_color))

        tip["pos"] = next_pos
        tip["dir"] = direction
        new_tips.append(tip)

        # 일정 확률로 새 가지 분기 (개수 상한 지킴)
        if random.random() < BRANCH_PROB and len(tips) < MAX_TIPS:
            branch_dir = vector(random.uniform(-1, 1),
                                random.uniform(-1, 1),
                                random.uniform(-1, 1)).norm()
            new_tips.append({"pos": next_pos, "dir": branch_dir})

    tips = new_tips

    # 성능 보호: 가지가 너무 많으면 오래된 것부터 화면에서 숨김
    while len(branches) > MAX_BRANCHES:
        old = branches.pop(0)
        old.visible = False
