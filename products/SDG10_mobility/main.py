# SDG10_mobility/main.py — 기회의 사다리와 계층 이동 (다른 각도)
# SDG 10. 출발점이 불평등해도 '사회 이동성'이 높으면 아래 계층도 위로 올라갈 수 있다.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, box
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 24
mobility = 0.2
# 절반은 낮은 출발, 절반은 높은 출발(불평등한 시작)
level = [random.uniform(0, 2) if i < N // 2 else random.uniform(6, 8) for i in range(N)]
scene = make_scene("SDG10 — 기회의 사다리(계층 이동)", width=900, height=560)
scene.append_to_caption("<b>사회 이동성을 높이면 낮은 출발선의 사람도 위로 올라간다</b>\n\n")
for h in range(9):     # 계층 눈금
    box(pos=vector(0, h, 0), size=vector(N, 0.03, 2), color=color.gray(0.4), opacity=0.3)
def on_mob(v):
    global mobility
    mobility = v
make_labeled_slider(0.0, 1.0, mobility, on_mob, "사회 이동성", length=320, decimals=2)
top_curve = make_line_curve("상위 계층(레벨6+) 인원", "시간", "인원", col=color.green)
balls = [sphere(pos=vector(i * 0.9 - N * 0.45, level[i], 0), radius=0.28,
                color=color.cyan if i < N // 2 else color.orange) for i in range(N)]
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    top = 0
    for i in range(N):
        # 이동성이 높으면 노력만큼 오를 확률↑ (출발 무관)
        level[i] += random.uniform(-0.3, 0.3 + mobility)
        level[i] = max(0, min(8, level[i]))
        balls[i].pos = vector(i * 0.9 - N * 0.45, level[i], 0)
        if level[i] >= 6: top += 1
    top_curve.plot(t, top)
