# SDG17_partnership/main.py — 국가 간 협력 네트워크 (자원 교환)
#
# SDG 17(지구촌 협력). 부품: dataviz + 네트워크 규칙.
# 국가 노드들이 자원을 주고받는다. 협력 수준이 높을수록 전체 번영이 커진다.
# 탐구 포인트: "협력 수준"을 높이면 세계 전체 번영(총자원)이 얼마나 커지나.
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, cylinder
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 7
cooperation = 0.3     # 0=고립, 1=완전 협력
resources = [random.uniform(5, 15) for _ in range(N)]
POS = [vector(6 * math.cos(2 * math.pi * i / N), 0, 6 * math.sin(2 * math.pi * i / N)) for i in range(N)]

scene = make_scene("SDG17 — 국가 간 협력 네트워크", width=900, height=560)
scene.append_to_caption("<b>협력 수준이 높을수록 자원 교환으로 세계 전체 번영이 커진다</b>\n\n")

def on_coop(v):
    global cooperation
    cooperation = v
make_labeled_slider(0.0, 1.0, cooperation, on_coop, "협력 수준", length=320, decimals=2)
welfare_curve = make_line_curve("세계 전체 번영(총자원)", "시간", "총자원", col=color.cyan)

nodes = [sphere(pos=POS[i], radius=0.6, color=color.cyan) for i in range(N)]
# 협력 링크(원형으로 이웃 연결)
links = [cylinder(pos=POS[i], axis=POS[(i + 1) % N] - POS[i], radius=0.05, color=color.gray(0.5))
         for i in range(N)]

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    # 협력: 이웃과 자원을 평균 쪽으로 나눔(약자에게 흘러가 전체 생산성↑)
    new = list(resources)
    for i in range(N):
        j = (i + 1) % N
        flow = (resources[j] - resources[i]) * 0.1 * cooperation
        new[i] += flow
        new[j] -= flow
    # 협력이 클수록 시너지(총량 성장), 고립이면 정체
    for i in range(N):
        new[i] += new[i] * 0.01 * cooperation
        resources[i] = max(0.5, new[i])
    for i in range(N):
        nodes[i].radius = 0.3 + resources[i] * 0.05
        links[i].opacity = 0.2 + 0.8 * cooperation
    welfare_curve.plot(t, sum(resources))
    if t % 80 == 0:
        for i in range(N):
            resources[i] = random.uniform(5, 15)
        welfare_curve.data = []
