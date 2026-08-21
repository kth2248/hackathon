# SDG05_wage_gap/main.py — 성별 임금 격차 대시보드 (다른 각도)
# SDG 5. 두 집단의 평균 임금 격차를 정책(동일임금 강도)으로 얼마나 좁히나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

policy = 0.0
wageA, wageB = 10.0, 7.0     # 초기 격차
scene = make_scene("SDG05 — 성별 임금 격차", width=900, height=560)
scene.append_to_caption("<b>동일임금 정책을 강화하면 두 집단 임금 격차가 좁혀진다</b>\n\n")
def on_policy(v):
    global policy
    policy = v
make_labeled_slider(0.0, 1.0, policy, on_policy, "동일임금 정책 강도", length=320, decimals=2)
A_c, B_c = make_lines("집단별 평균 임금", "시간", "임금",
                      [("A 집단", color.orange), ("B 집단", color.cyan)])
barA = box(pos=vector(-1.5, 0, 0), size=vector(1, wageA, 1), color=color.orange)
barB = box(pos=vector(1.5, 0, 0), size=vector(1, wageB, 1), color=color.cyan)
gap_label = label(pos=vector(0, 12, 0), text="", box=False, height=16)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    avg = (wageA + wageB) / 2
    wageA += (avg - wageA) * policy * 0.5 + random.uniform(-0.1, 0.1)
    wageB += (avg - wageB) * policy * 0.5 + random.uniform(-0.1, 0.1)
    barA.size = vector(1, max(0.1, wageA), 1); barA.pos = vector(-1.5, wageA / 2, 0)
    barB.size = vector(1, max(0.1, wageB), 1); barB.pos = vector(1.5, wageB / 2, 0)
    gap_label.text = f"격차: {abs(wageA - wageB):.1f}"
    A_c.plot(t, wageA); B_c.plot(t, wageB)
