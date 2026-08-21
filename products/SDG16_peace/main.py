# SDG16_peace/main.py — 규칙 강도와 협력 (에이전트 사회 실험)
#
# SDG 16(평화·정의·제도). 부품: dataviz + 규칙 에이전트.
# 제도(규칙)의 강도가 셀수록 배신이 억제되고 협력이 늘어난다(단순 은유).
# 탐구 포인트: "규칙 강도"를 높이면 사회 전체 협력률이 얼마나 오르나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 40
rule_strength = 0.3      # 0=무법, 1=강한 제도
# 각 에이전트: 협력 성향(0~1). 규칙이 세면 배신자도 협력 쪽으로 눌림.
coop = [random.random() for _ in range(N)]

scene = make_scene("SDG16 — 규칙 강도와 협력", width=900, height=560)
scene.append_to_caption("<b>제도(규칙)가 셀수록 배신(빨강)이 줄고 협력(초록)이 늘어난다</b>\n\n")

def on_rule(v):
    global rule_strength
    rule_strength = v
make_labeled_slider(0.0, 1.0, rule_strength, on_rule, "규칙 강도", length=320, decimals=2)
coop_curve = make_line_curve("협력률 (%)", "시간", "%", col=color.green)

balls = []
for i in range(N):
    a = (i % 8) - 4
    b = (i // 8) - 2
    balls.append(sphere(pos=vector(a * 1.2, 0, b * 1.2), radius=0.4, color=color.white))

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    coop_count = 0
    for i in range(N):
        # 성향 + 규칙 압력으로 이번 라운드 협력 여부 결정
        p = coop[i] * (1 - rule_strength) + rule_strength   # 규칙이 세면 협력 확률↑
        is_coop = random.random() < p
        balls[i].color = color.green if is_coop else color.red
        if is_coop:
            coop_count += 1
        # 협력이 이득이 되도록 성향이 서서히 그쪽으로 학습
        coop[i] = min(1.0, max(0.0, coop[i] + (0.02 if is_coop else -0.01)))
    coop_curve.plot(t, 100.0 * coop_count / N)
