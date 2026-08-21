# SDG09_resilience/main.py — 인프라 네트워크 복원력 (다른 각도)
# SDG 9. 도시 네트워크에서 링크가 끊겨도 얼마나 연결이 유지되나(복원력).
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, cylinder
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 9
POS = [vector(6 * math.cos(2 * math.pi * i / N), 0, 6 * math.sin(2 * math.pi * i / N)) for i in range(N)]
# 링크: 원형 이웃 + 몇 개의 교차 링크
EDGES = [(i, (i + 1) % N) for i in range(N)] + [(0, 4), (1, 5), (2, 6), (3, 7)]
removed = 0
scene = make_scene("SDG09 — 인프라 네트워크 복원력", width=900, height=560)
scene.append_to_caption("<b>링크를 끊어도(회색) 도시들이 얼마나 연결(초록)을 유지하나</b>\n\n")
nodes = [sphere(pos=POS[i], radius=0.5, color=color.cyan) for i in range(N)]
edge_objs = []
conn_curve = make_line_curve("연결된 도시 비율(%)", "끊긴 링크 수", "%", col=color.green)

def connected_fraction(active_edges):
    # 0번 도시에서 도달 가능한 도시 수 / N (단순 BFS)
    adj = {i: [] for i in range(N)}
    for a, b in active_edges:
        adj[a].append(b); adj[b].append(a)
    seen = {0}; stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return len(seen) / N

def update(k):
    global edge_objs
    for e in edge_objs: e.visible = False
    edge_objs = []
    active = EDGES[:] if k <= 0 else EDGES[:-k] if k < len(EDGES) else []
    for a, b in active:
        edge_objs.append(cylinder(pos=POS[a], axis=POS[b] - POS[a], radius=0.06, color=color.green))
    frac = connected_fraction(active)
    for nd in nodes: nd.color = color.cyan
    conn_curve.plot(k, 100.0 * frac)

def on_removed(v):
    global removed
    removed = int(v); update(removed)
make_labeled_slider(0, len(EDGES), removed, on_removed, "끊긴 링크 수", length=320, decimals=0)
update(removed)
while True:
    rate(20)
