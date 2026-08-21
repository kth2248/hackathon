# SDG09_infrastructure/main.py — 도로망 연결 효율 (A* 경로탐색)
#
# SDG 9(산업·혁신·인프라). 부품: astar + grid.
# 도시들 사이에 도로(통로)를 놓을수록 이동이 빨라진다. A*로 평균 이동거리를 측정.
# 탐구 포인트: 도로를 늘리면 도시 간 평균 이동거리가 얼마나 짧아지나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere
from vpython_utils import make_scene
from grid import GridWorld
from grid_render import render_floor, render_obstacles, cell_pos
from astar import astar, path_length
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

COLS, ROWS = 16, 16
NUM_CITIES = 5
num_roads = 6

# 기본: 대부분이 험지(장애물), 도로 칸만 통행 가능. 도로를 늘리면 연결이 좋아짐.
world = GridWorld(COLS, ROWS)
CITIES = []
while len(CITIES) < NUM_CITIES:
    c = (random.randrange(COLS), random.randrange(ROWS))
    if c not in CITIES:
        CITIES.append(c)

scene = make_scene("SDG09 — 도로망 연결 효율 (A*)", width=900, height=560)
scene.append_to_caption("<b>도로(통로)를 놓을수록 도시 간 A* 이동거리가 짧아진다</b>\n\n")

def rebuild_world(nroads):
    """모든 칸을 험지로 막고, 도시 주변 + 무작위 도로 칸만 통행 가능하게 뚫는다."""
    global world
    world = GridWorld(COLS, ROWS)
    for x in range(COLS):
        for y in range(ROWS):
            world.block((x, y))
    # 도시 칸은 항상 통행
    for cx, cy in CITIES:
        world.unblock((cx, cy))
    # 무작위 도로: 두 도시를 잇는 직선 경로를 nroads개 뚫음
    for _ in range(nroads):
        a, b = random.sample(CITIES, 2)
        x, y = a
        while (x, y) != b:
            world.unblock((x, y))
            if x != b[0]:
                x += 1 if b[0] > x else -1
            elif y != b[1]:
                y += 1 if b[1] > y else -1
        world.unblock(b)

def avg_travel():
    """도시 쌍들의 A* 평균 이동거리(연결 안 되면 큰 값)."""
    tot, cnt = 0.0, 0
    for i in range(len(CITIES)):
        for j in range(i + 1, len(CITIES)):
            p = astar(CITIES[i], CITIES[j], world.passable)
            tot += path_length(p) if p else COLS * ROWS   # 연결 안 되면 페널티
            cnt += 1
    return tot / cnt if cnt else 0

city_objs = []
obstacle_objs = []
def redraw():
    global obstacle_objs
    for o in obstacle_objs:
        o.visible = False
    obstacle_objs = render_obstacles(world, obstacle_color=color.gray(0.4), height=0.3)

render_floor(world)
for cx, cy in CITIES:
    city_objs.append(sphere(pos=cell_pos(world, (cx, cy), y=0.4), radius=0.5, color=color.yellow))

travel_curve = make_line_curve("도시 간 평균 이동거리(작을수록 좋음)", "도로 수", "거리", col=color.cyan)

def on_roads(v):
    global num_roads
    num_roads = int(v)
    rebuild_world(num_roads)
    redraw()
    travel_curve.plot(num_roads, avg_travel())

make_labeled_slider(1, 12, num_roads, on_roads, "도로 수", length=300, decimals=0)
rebuild_world(num_roads)
redraw()
travel_curve.plot(num_roads, avg_travel())
while True:
    rate(20)
