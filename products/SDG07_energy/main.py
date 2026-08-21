# SDG07_energy/main.py — 발전소 최적 입지 (유전알고리즘: 수요 커버)
#
# SDG 7(깨끗한 에너지). 부품: genetic_optimize.
# 도시(수요 지점)들을 최대한 많이 전력 공급 반경 안에 넣도록 발전소 위치를 AI가 탐색.
# 탐구 포인트: 발전소 수를 바꾸면 커버되는 도시 비율이 어떻게 변하나.
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere, cylinder
from vpython_utils import make_scene
from genetic import genetic_optimize
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

AREA = 8.0
NUM_CITIES = 24
NUM_PLANTS = 3
SUPPLY_R = 3.0
POP, GENS = 24, 30
CITIES = [(random.uniform(-AREA, AREA), random.uniform(-AREA, AREA)) for _ in range(NUM_CITIES)]
num_plants = NUM_PLANTS

scene = make_scene("SDG07 — 발전소 최적 입지", width=900, height=560)
scene.append_to_caption("<b>도시를 최대한 커버하도록 발전소 위치를 유전알고리즘이 탐색</b>\n\n")
box(pos=vector(0, -0.3, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=color.gray(0.3))
city_objs = [sphere(pos=vector(cx, 0.2, cz), radius=0.3, color=color.gray(0.6)) for cx, cz in CITIES]

def covered(city, plants):
    return any(math.hypot(city[0] - px, city[1] - pz) <= SUPPLY_R for px, pz in plants)

plant_objs = []
def clear_plants():
    global plant_objs
    for o in plant_objs:
        o.visible = False
    plant_objs = []

def rand_pt():
    return (random.uniform(-AREA, AREA), random.uniform(-AREA, AREA))
def create_individual():
    return [rand_pt() for _ in range(num_plants)]
def fitness(ind):
    return sum(1 for c in CITIES if covered(c, ind))
def mutate(ind):
    c = list(ind); c[random.randrange(len(c))] = rand_pt(); return c

cover_curve = make_line_curve("세대별 커버된 도시 수", "세대", "도시", col=color.yellow)

def run():
    clear_plants(); cover_curve.data = []
    hist = []
    best, best_fit = genetic_optimize(create_individual, fitness, mutate,
                                      pop_size=POP, generations=GENS,
                                      on_generation=lambda g, b, f: hist.append((g, f)))
    for g, f in hist:
        cover_curve.plot(g, f)
    for px, pz in best:
        plant_objs.append(box(pos=vector(px, 0.6, pz), size=vector(0.7, 1.2, 0.7), color=color.yellow))
        plant_objs.append(cylinder(pos=vector(px, 0.1, pz), axis=vector(0, 0.02, 0),
                                   radius=SUPPLY_R, color=color.yellow, opacity=0.12))
    # 커버 여부로 도시 색 갱신
    for i, c in enumerate(CITIES):
        city_objs[i].color = color.green if covered(c, best) else color.red

def on_plants(v):
    global num_plants
    num_plants = int(v); run()
make_labeled_slider(1, 8, NUM_PLANTS, on_plants, "발전소 수", length=300, decimals=0)
run()
while True:
    rate(20)
