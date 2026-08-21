# SDG06_pipe_network/main.py — 상수도 공급망 (다른 각도)
# SDG 6. 수원에서 파이프가 닿는 범위 안의 가구만 물을 받는다. 파이프를 늘리면 공급률↑.
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, cylinder
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

AREA = 8.0
NUM_HOUSES = 40
pipe_reach = 3.0
SOURCE = vector(0, 0, 0)
HOUSES = [(random.uniform(-AREA, AREA), random.uniform(-AREA, AREA)) for _ in range(NUM_HOUSES)]
scene = make_scene("SDG06 — 상수도 공급망", width=900, height=560)
scene.append_to_caption("<b>수원(파랑)에서 파이프가 닿는 가구만 물을 받는다. 파이프를 늘리면 공급률↑</b>\n\n")
source_ball = sphere(pos=SOURCE, radius=0.6, color=color.blue)
house_objs = [sphere(pos=vector(hx, 0.2, hz), radius=0.25, color=color.red) for hx, hz in HOUSES]
supply_curve = make_line_curve("물 공급률(%)", "파이프 도달거리", "%", col=color.blue)
pipes = []
def update(reach):
    global pipes
    for p in pipes: p.visible = False
    pipes = []
    served = 0
    for i, (x, z) in enumerate(HOUSES):
        d = math.hypot(x, z)
        ok = d <= reach
        house_objs[i].color = color.cyan if ok else color.red
        if ok:
            pipes.append(cylinder(pos=SOURCE, axis=vector(x, 0.2, z) - SOURCE, radius=0.04, color=color.blue))
            served += 1
    supply_curve.plot(reach, 100.0 * served / NUM_HOUSES)
def on_reach(v):
    global pipe_reach
    pipe_reach = v; update(pipe_reach)
make_labeled_slider(1.0, 12.0, pipe_reach, on_reach, "파이프 도달거리", length=320, decimals=1)
update(pipe_reach)
while True:
    rate(20)
