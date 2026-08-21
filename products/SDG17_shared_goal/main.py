# SDG17_shared_goal/main.py — 공동 목표와 무임승차 (다른 각도)
# SDG 17. 여러 나라가 공동 기금(기후 목표)에 기여한다. 무임승차가 많으면 목표 달성이 늦어진다.
import os, sys, math
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 8
free_rider = 0.3
progress = 0.0
GOAL = 100.0
POS = [vector(6 * math.cos(2 * math.pi * i / N), 0, 6 * math.sin(2 * math.pi * i / N)) for i in range(N)]
scene = make_scene("SDG17 — 공동 목표와 무임승차", width=900, height=560)
scene.append_to_caption("<b>무임승차가 늘면 나라들의 기여가 줄어 공동 목표 달성이 늦어진다</b>\n\n")
nodes = [sphere(pos=POS[i], radius=0.5, color=color.cyan) for i in range(N)]
goal_bar = box(pos=vector(0, 0, 0), size=vector(2, 0.1, 2), color=color.green)
status = label(pos=vector(0, 8, 0), text="", box=False, height=16)
def on_free(v):
    global free_rider
    free_rider = v
make_labeled_slider(0.0, 1.0, free_rider, on_free, "무임승차 비율", length=320, decimals=2)
prog_curve = make_line_curve("공동 목표 진행도(%)", "시간", "%", col=color.green)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    contributing = 0
    total = 0.0
    for i in range(N):
        rides = (i / N) < free_rider     # 앞쪽 일부가 무임승차
        nodes[i].color = color.gray(0.5) if rides else color.cyan
        if not rides:
            total += 1.5; contributing += 1
    progress = min(GOAL, progress + total)
    goal_bar.size = vector(2, max(0.05, progress / 10), 2); goal_bar.pos = vector(0, goal_bar.size.y / 2, 0)
    status.text = f"기여국 {contributing}/{N}"
    prog_curve.plot(t, 100.0 * progress / GOAL)
    if progress >= GOAL:      # 목표 달성 → 리셋 반복
        progress = 0.0; prog_curve.data = []
