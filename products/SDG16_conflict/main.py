# SDG16_conflict/main.py — 자원 분쟁과 공정성 (다른 각도)
# SDG 16. 두 집단이 자원을 나눌 때 불공정하면 분쟁이 커진다. 공정할수록 평화.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

fairness = 0.5
tension = 0.0
scene = make_scene("SDG16 — 자원 분쟁과 공정성", width=900, height=560)
scene.append_to_caption("<b>자원 분배가 불공정하면 분쟁(빨강)이 쌓이고, 공정하면 가라앉는다</b>\n\n")
def on_fair(v):
    global fairness
    fairness = v
make_labeled_slider(0.0, 1.0, fairness, on_fair, "분배 공정성", length=320, decimals=2)
tension_curve = make_line_curve("분쟁 수준", "시간", "긴장도", col=color.red)
barA = box(pos=vector(-2, 0, 0), size=vector(1.5, 1, 1.5), color=color.orange)
barB = box(pos=vector(2, 0, 0), size=vector(1.5, 1, 1.5), color=color.cyan)
status = label(pos=vector(0, 6, 0), text="", box=False, height=18)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    shareA = 0.5 + (1 - fairness) * 0.45     # 불공정할수록 A가 더 가져감
    shareB = 1 - shareA
    unfair = abs(shareA - 0.5) * 2           # 0(공정)~1(독점)
    tension = max(0.0, min(10.0, tension + (unfair - 0.3) * 0.5))
    barA.size = vector(1.5, max(0.1, shareA * 6), 1.5); barA.pos = vector(-2, barA.size.y / 2, 0)
    barB.size = vector(1.5, max(0.1, shareB * 6), 1.5); barB.pos = vector(2, barB.size.y / 2, 0)
    status.text = "분쟁 발발!" if tension > 6 else ("긴장" if tension > 3 else "평화")
    status.color = color.red if tension > 6 else color.white
    tension_curve.plot(t, tension)
