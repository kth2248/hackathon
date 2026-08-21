# SDG01_safety_net/main.py — 소득 사다리와 사회 안전망 (다른 각도)
# SDG 1. 사람들이 소득 사다리에서 오르내리고, 안전망(슬라이더)이 추락을 받쳐준다.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, box
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 24
net = 3.0
income = [random.uniform(1, 9) for _ in range(N)]
scene = make_scene("SDG01 — 소득 사다리와 안전망", width=900, height=560)
scene.append_to_caption("<b>안전망(파란 판)을 올리면 추락한 사람을 더 많이 받쳐준다</b>\n\n")
def on_net(v):
    global net
    net = v
make_labeled_slider(0, 9, net, on_net, "안전망 수준", length=320, decimals=1)
rescued_curve = make_line_curve("안전망이 구제한 인원", "시간", "인원", col=color.green)
net_plane = box(pos=vector(0, net, 0), size=vector(N * 0.9, 0.1, 2), color=color.blue, opacity=0.4)
balls = [sphere(pos=vector(i * 0.9 - N * 0.45, income[i], 0), radius=0.3, color=color.cyan) for i in range(N)]
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    rescued = 0
    for i in range(N):
        income[i] = max(0, income[i] + random.uniform(-1.2, 1.0))
        y = income[i]
        if income[i] < net:
            y = net; balls[i].color = color.green; rescued += 1
        else:
            balls[i].color = color.cyan
        balls[i].pos = vector(i * 0.9 - N * 0.45, y, 0)
    net_plane.pos = vector(0, net, 0)
    rescued_curve.plot(t, rescued)
