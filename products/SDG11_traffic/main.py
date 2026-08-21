# SDG11_traffic/main.py — 교통 신호와 혼잡 (다른 각도)
# SDG 11. 신호 녹색시간을 조절해 교차로 대기 차량(혼잡)을 줄인다.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

green_time = 5.0
queue = 0.0
scene = make_scene("SDG11 — 교통 신호와 혼잡", width=900, height=560)
scene.append_to_caption("<b>녹색시간을 늘리면 통과량이 늘어 대기 차량(혼잡)이 줄어든다</b>\n\n")
box(pos=vector(0, -0.3, 0), size=vector(14, 0.2, 4), color=color.gray(0.3))
signal = sphere(pos=vector(0, 1.5, 0), radius=0.5, color=color.red)
cars = []
def on_green(v):
    global green_time
    green_time = v
make_labeled_slider(1.0, 10.0, green_time, on_green, "녹색시간", length=320, decimals=1)
queue_curve = make_line_curve("대기 차량 수", "시간", "대수", col=color.red)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 4: continue
    t += 1
    arrivals = random.uniform(2, 5)                 # 도착 차량
    is_green = (t % 10) < green_time
    signal.color = color.green if is_green else color.red
    passed = green_time * 0.9 if is_green else 0     # 녹색일 때만 통과
    queue = max(0.0, queue + arrivals - passed)
    # 대기 차량 시각화(빨간 점들이 줄지어)
    for c in cars: c.visible = False
    cars = []
    for i in range(int(min(queue, 20))):
        cars.append(sphere(pos=vector(-6 + i * 0.5, 0.2, 0), radius=0.2, color=color.red))
    queue_curve.plot(t, queue)
