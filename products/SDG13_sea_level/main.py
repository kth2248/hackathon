# SDG13_sea_level/main.py — 해수면 상승 (다른 각도)
# SDG 13. 기온이 오르면 해수면이 상승해 낮은 땅이 잠긴다. 얼마나 잠기나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

COLS = 24
temp = 0.0
HEIGHT = [random.uniform(0.5, 6) for _ in range(COLS)]   # 땅 높이
scene = make_scene("SDG13 — 해수면 상승", width=900, height=560)
scene.append_to_caption("<b>기온을 올리면 해수면(파란 판)이 상승해 낮은 땅이 잠긴다</b>\n\n")
land = [box(pos=vector(i * 0.8 - COLS * 0.4, HEIGHT[i] / 2, 0),
            size=vector(0.75, HEIGHT[i], 3), color=color.green) for i in range(COLS)]
sea = box(pos=vector(0, 0, 1.6), size=vector(COLS * 0.8, 0.1, 0.2), color=color.blue, opacity=0.5)
def on_temp(v):
    global temp
    temp = v
make_labeled_slider(0.0, 6.0, temp, on_temp, "기온 상승(도)", length=320, decimals=1)
sub_curve = make_line_curve("잠긴 땅 비율(%)", "기온", "%", col=color.blue)
frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    sea_level = temp                      # 기온만큼 해수면 상승(단순화)
    submerged = 0
    for i in range(COLS):
        if HEIGHT[i] <= sea_level:
            land[i].color = color.blue; submerged += 1
        else:
            land[i].color = color.green
    sea.size = vector(COLS * 0.8, max(0.05, sea_level), 3)
    sea.pos = vector(0, sea_level / 2, 0)
    sub_curve.plot(temp, 100.0 * submerged / COLS)
