# D안 — AI 신뢰도(안전 판단) 시각화
#
# 컨셉: 중심의 "AI 판단" 구 주위를 여러 선택지 입자가 공전한다. 각 입자는 안전 점수(0~1)를
#       가지며 색이 초록(안전)~빨강(위험)으로 바뀐다. AI는 매 순간 '가장 안전한 선택지'로
#       연결선(시선)을 옮긴다. => "무해한 AI"를 결과가 아니라 '판단 과정'으로 보여준다.
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작)
#
# 재사용 부품: vpython_utils(make_scene) / ui_widgets(make_labeled_slider)

import os
import sys
import math
import random

# hackathon_kit 부품 폴더를 경로에 추가 (어느 위치에서 실행해도 import 되도록)
_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import sphere, cylinder, vector, color, rate, wtext
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider

# ============================================================
# 1. 설정값
# ============================================================
NUM_PARTICLES = 6
ORBIT_RADIUS = 4
ORBIT_SPEED = 0.01       # 입자 공전 속도
WOBBLE_AMP = 0.2         # 안전 점수가 흔들리는 폭 (재판단 느낌)
WOBBLE_SPEED = 0.02      # 흔들림 속도 (너무 빠르면 이 값을 줄일 것)

# ============================================================
# 2. 상태 + 콜백
# ============================================================
safety_bar = 0.0         # 안전 기준선: 이 점수 미만인 선택지는 후보에서 제외


def on_bar(v):
    global safety_bar
    safety_bar = v


# ============================================================
# 3. 씬 + UI
# ============================================================
scene = make_scene("D안 — AI 신뢰도 시각화", width=900, height=550)
scene.append_to_caption("<b>여러 선택지 중 '가장 안전한 것'으로 판단을 옮기는 AI</b>\n\n")

# 안전 기준선 슬라이더: 올릴수록 위험한 선택지를 후보에서 배제(더 엄격 = 더 무해)
make_labeled_slider(0.0, 1.0, safety_bar, on_bar, "안전 기준선", length=320, decimals=2)
status_label = wtext(text="\n")

# 중심 = AI의 판단
center = sphere(pos=vector(0, 0, 0), radius=0.4, color=color.white)

# 선택지 입자들 (공전) — 고정 기준값 base 주위로 점수가 진동한다
particles = []
for i in range(NUM_PARTICLES):
    angle = (2 * math.pi / NUM_PARTICLES) * i
    base = random.uniform(0.2, 0.9)      # 이 입자의 평균 안전도
    pos = vector(ORBIT_RADIUS * math.cos(angle), ORBIT_RADIUS * math.sin(angle), 0)
    obj = sphere(pos=pos, radius=0.25, color=vector(1 - base, base, 0))
    particles.append({"obj": obj, "angle": angle, "base": base, "phase": angle, "score": base})

# 가장 안전한 선택지로 향하는 연결선(시선)
link = cylinder(pos=center.pos, axis=vector(1, 0, 0), radius=0.04, color=color.yellow)

# ============================================================
# 4. 애니메이션 루프
# ============================================================
t = 0
while True:
    rate(60)
    t += WOBBLE_SPEED

    best = None
    for p in particles:
        # 4-1. 공전
        p["angle"] += ORBIT_SPEED
        p["obj"].pos = vector(ORBIT_RADIUS * math.cos(p["angle"]),
                              ORBIT_RADIUS * math.sin(p["angle"]), 0)

        # 4-2. 안전 점수: 고정 base 주위로 진동 (계속 재평가하는 느낌, 극단으로 안 쏠림)
        score = p["base"] + math.sin(t + p["phase"]) * WOBBLE_AMP
        score = min(1.0, max(0.0, score))
        p["score"] = score
        p["obj"].color = vector(1 - score, score, 0)

        # 4-3. 안전 기준선 미달 선택지는 흐리게 + 후보에서 제외
        eligible = score >= safety_bar
        p["obj"].opacity = 1.0 if eligible else 0.3
        if eligible and (best is None or score > best["score"]):
            best = p

    # 4-4. 연결선 갱신: 기준을 넘는 가장 안전한 선택지로
    if best is not None:
        link.visible = True
        link.pos = center.pos
        link.axis = best["obj"].pos - center.pos
        status_label.text = (f"  안전 기준선: {safety_bar:.2f}   "
                             f"→ 선택된 안전 점수: {best['score']:.2f} ✅\n")
    else:
        # 아무 선택지도 기준을 못 넘음 = 위험하다고 판단해 행동 보류
        link.visible = False
        status_label.text = (f"  안전 기준선: {safety_bar:.2f}   "
                             f"→ 기준을 넘는 선택지 없음 ⚠️ 판단 보류\n")
