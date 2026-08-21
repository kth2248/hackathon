# SDG02_nutrition/main.py — 영양 균형 대시보드 (다른 각도)
# SDG 2. 한정 예산을 곡물/채소/단백질에 배분해 영양 목표를 맞춘다(막대 대시보드).
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from allocate import proportional_allocate, satisfaction
from ui_widgets import make_labeled_slider
from live_graph import make_bars

GROUPS = ["곡물", "채소", "단백질"]
TARGET = [8.0, 6.0, 5.0]
COLS = [color.yellow, color.green, color.orange]
budget = 12.0
grain_w = 1.0
scene = make_scene("SDG02 — 영양 균형 대시보드", width=900, height=560)
scene.append_to_caption("<b>예산을 식품군에 배분해 영양 목표 달성도를 높인다</b>\n\n")
def on_budget(v):
    global budget
    budget = v
def on_grain(v):
    global grain_w
    grain_w = v
make_labeled_slider(3, 25, budget, on_budget, "식량 예산", length=300, decimals=0)
make_labeled_slider(0.3, 3.0, grain_w, on_grain, "곡물 우선도", length=300, decimals=1)
bars = make_bars("영양 달성도(0~1)", "식품군(0곡 1채 2단)", "달성", col=color.green)
boxes = [box(pos=vector(i * 3 - 3, 0, 0), size=vector(1.5, 0.1, 1.5), color=COLS[i]) for i in range(3)]
labels = [label(pos=vector(i * 3 - 3, -0.8, 0), text=GROUPS[i], box=False, height=14) for i in range(3)]
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    weighted = [TARGET[0] * grain_w, TARGET[1], TARGET[2]]
    alloc = proportional_allocate(budget, weighted)
    sats = [satisfaction(alloc[i], TARGET[i]) for i in range(3)]
    for i in range(3):
        h = max(0.1, sats[i] * 3)
        boxes[i].size = vector(1.5, h, 1.5); boxes[i].pos = vector(i * 3 - 3, h / 2, 0)
    bars.data = [[i, sats[i]] for i in range(3)]
