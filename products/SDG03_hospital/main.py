# SDG03_hospital/main.py — 병상 수용력 대시보드 (다른 각도)
# SDG 3. 감염자 수 vs 병상 수. 감염이 병상을 넘으면 의료붕괴(빨강). 거리두기로 곡선 낮추기.
import os, sys, math
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

BEDS = 40.0
distancing = 0.3
infected = 5.0
scene = make_scene("SDG03 — 병상 수용력 대시보드", width=900, height=560)
scene.append_to_caption("<b>감염자가 병상(노란 선)을 넘으면 의료붕괴. 거리두기로 정점을 낮춘다</b>\n\n")
def on_dist(v):
    global distancing
    distancing = v
make_labeled_slider(0.0, 0.9, distancing, on_dist, "거리두기 강도", length=320, decimals=2)
inf_c, bed_c = make_lines("감염자 vs 병상", "시간", "인원",
                          [("감염자", color.red), ("병상", color.yellow)])
inf_box = box(pos=vector(0, 0, 0), size=vector(2, 0.1, 2), color=color.red)
bed_line = box(pos=vector(0, BEDS / 10, 0), size=vector(4, 0.08, 3), color=color.yellow, opacity=0.5)
status = label(pos=vector(0, 9, 0), text="", box=False, height=18)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    growth = (1 - distancing) * 0.25
    infected = max(1.0, infected + infected * growth - infected * 0.05)   # 성장 - 회복
    if infected > 200: infected = 5.0   # 유행 종료 후 리셋
    h = infected / 10
    inf_box.size = vector(2, max(0.1, h), 2); inf_box.pos = vector(0, h / 2, 0)
    inf_box.color = color.red if infected > BEDS else color.green
    status.text = ("의료붕괴!" if infected > BEDS else "안정")
    inf_c.plot(t, infected); bed_c.plot(t, BEDS)
