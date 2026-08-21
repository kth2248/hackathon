# SDG15_forest_ga/main.py — 숲 배치 최적화 (유전알고리즘)
#
# SDG 15(육상 생태계) + 13(기후). 부품: genetic_optimize.
# 나무를 어디에 심어야 넓게 퍼져(=커버리지 최대) 자라는지 AI가 스스로 탐색한다.
# 탐구 포인트: 무작위 배치 vs 유전알고리즘 최적 배치의 커버리지 차이. 세대별 개선 곡선.
#
# 실행: python main.py

import os
import sys
import math
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import color, rate, vector, box, cylinder, sphere
from vpython_utils import make_scene
from genetic import genetic_optimize
from ui_widgets import make_labeled_slider, make_toggle
from live_graph import make_line_curve

# ============================================================
# 1. 설정
# ============================================================
FIELD = 8.0            # 땅 반경(-FIELD~FIELD)
num_trees = 12
GENERATIONS = 30
POP = 24

show_optimized = True

# ============================================================
# 2. 씬 + UI
# ============================================================
scene = make_scene("SDG15 — 유전알고리즘 숲 배치 최적화", width=900, height=560)
scene.append_to_caption("<b>AI가 세대를 거치며 나무를 넓게 퍼뜨리는 최적 배치를 스스로 찾음</b>\n\n")
box(pos=vector(0, -0.3, 0), size=vector(2 * FIELD, 0.2, 2 * FIELD), color=vector(0.35, 0.25, 0.1))  # 땅

fitness_curve = make_line_curve("세대별 커버리지(클수록 넓게 퍼짐)", "세대", "점수", col=color.green)

tree_objs = []      # 현재 그려진 나무(cylinder+sphere)


def clear_trees():
    global tree_objs
    for o in tree_objs:
        o.visible = False
    tree_objs = []


def draw_trees(layout, trunk=color.orange, leaf=None):
    for (x, z) in layout:
        tree_objs.append(cylinder(pos=vector(x, 0, z), axis=vector(0, 0.8, 0), radius=0.12, color=vector(0.4, 0.25, 0.1)))
        tree_objs.append(sphere(pos=vector(x, 1.0, z), radius=0.5,
                                color=leaf if leaf is not None else color.green))


# --- 유전알고리즘 정의 ---
def rand_tree():
    return (random.uniform(-FIELD, FIELD), random.uniform(-FIELD, FIELD))


def create_individual():
    return [rand_tree() for _ in range(num_trees)]


def fitness(ind):
    """커버리지 = 각 나무에서 가장 가까운 이웃까지 거리의 합(클수록 넓게 퍼짐)."""
    total = 0.0
    for i, a in enumerate(ind):
        nearest = min(math.hypot(a[0] - b[0], a[1] - b[1])
                      for j, b in enumerate(ind) if j != i) if len(ind) > 1 else 0
        total += nearest
    return total


def mutate(ind):
    child = list(ind)
    k = random.randrange(len(child))
    child[k] = rand_tree()
    return child


def crossover(a, b):
    cut = len(a) // 2
    return a[:cut] + b[cut:]


def run_optimization():
    """GA 실행 + 세대별 점수 그래프 + 결과 배치 그리기 (무작위 배치와 비교)."""
    global tree_objs
    clear_trees()
    fitness_curve.data = []

    history = []
    best, best_fit = genetic_optimize(
        create_individual, fitness, mutate, crossover=crossover,
        pop_size=POP, generations=GENERATIONS,
        on_generation=lambda gen, b, f: history.append((gen, f)),
    )
    for gen, f in history:
        fitness_curve.plot(gen, f)

    if show_optimized:
        draw_trees(best, leaf=color.green)                 # 최적 배치(초록)
    else:
        draw_trees(create_individual(), leaf=color.gray(0.5))  # 무작위 배치(회색) 비교용


def on_trees(v):
    global num_trees
    num_trees = int(v)
    run_optimization()


def on_show(c):
    global show_optimized
    show_optimized = c
    run_optimization()


make_labeled_slider(4, 24, num_trees, on_trees, "나무 수", length=300, decimals=0)
make_toggle("최적 배치(유전알고리즘)", "무작위 배치(비교)", on_show, initial=True, checkbox_text="최적화 사용")

run_optimization()

# 화면 유지(조작 대기)
while True:
    rate(20)
