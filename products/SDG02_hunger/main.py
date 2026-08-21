# SDG02_hunger/main.py — 작물 배치 최적화 (유전알고리즘: 비옥한 땅 찾기)
#
# SDG 2(기아 종식). 부품: genetic_optimize.
# 비옥한 땅(초록 진한 곳)에 작물을 놓아야 수확량이 는다. AI가 최적 위치를 스스로 탐색.
# 탐구 포인트: 무작위 파종 vs 유전알고리즘 파종의 총 수확량 차이.
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere
from vpython_utils import make_scene
from genetic import genetic_optimize
from ui_widgets import make_labeled_slider, make_toggle
from live_graph import make_line_curve

FIELD = 8.0
num_crops = 12
POP, GENS = 24, 30
HOTSPOTS = [(random.uniform(-FIELD, FIELD), random.uniform(-FIELD, FIELD), random.uniform(1.5, 3.0)) for _ in range(4)]
use_ga = True

scene = make_scene("SDG02 — 유전알고리즘 작물 배치", width=900, height=560)
scene.append_to_caption("<b>비옥한 땅에 작물을 배치해 수확량을 최대화(AI가 탐색)</b>\n\n")
box(pos=vector(0, -0.3, 0), size=vector(2 * FIELD, 0.2, 2 * FIELD), color=vector(0.3, 0.2, 0.1))
# 비옥지 표시(연한 초록 원반)
for hx, hz, hr in HOTSPOTS:
    box(pos=vector(hx, -0.19, hz), size=vector(hr * 2, 0.05, hr * 2), color=color.green, opacity=0.25)

def fertility(x, z):
    return sum(math.exp(-((x - hx) ** 2 + (z - hz) ** 2) / (2 * hr * hr)) for hx, hz, hr in HOTSPOTS)

crop_objs = []
def clear_crops():
    global crop_objs
    for o in crop_objs:
        o.visible = False
    crop_objs = []
def draw_crops(layout, col):
    for x, z in layout:
        crop_objs.append(sphere(pos=vector(x, 0.4, z), radius=0.35, color=col))

def rand_pt():
    return (random.uniform(-FIELD, FIELD), random.uniform(-FIELD, FIELD))
def create_individual():
    return [rand_pt() for _ in range(num_crops)]
def fitness(ind):
    return sum(fertility(x, z) for x, z in ind)
def mutate(ind):
    c = list(ind); c[random.randrange(len(c))] = rand_pt(); return c

fit_curve = make_line_curve("세대별 총 수확량", "세대", "수확량", col=color.green)

def run():
    clear_crops(); fit_curve.data = []
    hist = []
    best, _ = genetic_optimize(create_individual, fitness, mutate,
                               pop_size=POP, generations=GENS,
                               on_generation=lambda g, b, f: hist.append((g, f)))
    for g, f in hist:
        fit_curve.plot(g, f)
    draw_crops(best if use_ga else create_individual(),
               color.green if use_ga else color.gray(0.5))

def on_crops(v):
    global num_crops
    num_crops = int(v); run()
def on_use(c):
    global use_ga
    use_ga = c; run()
make_labeled_slider(4, 24, num_crops, on_crops, "작물 수", length=300, decimals=0)
make_toggle("유전알고리즘 배치", "무작위 파종(비교)", on_use, initial=True, checkbox_text="최적화 사용")
run()
while True:
    rate(20)
