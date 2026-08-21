# SDG01_poverty/main.py — 복지 자원 분배 (자원배분: 가장 가난한 가구부터)
#
# SDG 1(빈곤 종식). 부품: allocate.greedy_allocate.
# 한정된 복지 예산을 어떻게 나눠야 빈곤선 아래 가구가 최소가 되나.
# 탐구 포인트: "예산"을 늘리면 빈곤 가구가 얼마나 주나 / 가난한 순서로 주는 게 왜 효율적인가.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere
from vpython_utils import make_scene
from allocate import greedy_allocate
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

COLS, ROWS = 6, 6
N = COLS * ROWS
POVERTY = 5.0
budget = 40.0

incomes = [random.uniform(1, 10) for _ in range(N)]

scene = make_scene("SDG01 — 복지 자원 분배", width=900, height=560)
scene.append_to_caption("<b>가난한 가구부터 예산을 배분해 빈곤선(빨강) 아래 가구를 최소화</b>\n\n")

def on_budget(v):
    global budget
    budget = v
make_labeled_slider(0, 120, budget, on_budget, "복지 예산", length=320, decimals=0)
poverty_curve = make_line_curve("빈곤선 아래 가구 수", "시간", "가구", col=color.red)

balls = []
for i in range(N):
    x, z = i % COLS - COLS / 2, i // COLS - ROWS / 2
    balls.append(sphere(pos=vector(x * 1.5, 0, z * 1.5), radius=0.5, color=color.green))

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    # 소득이 조금씩 흔들림(동적)
    for i in range(N):
        incomes[i] = max(0.5, incomes[i] + random.uniform(-0.3, 0.3))
    # 빈곤선까지 부족분 계산 → 부족이 큰(가난한) 순서로 예산 배분
    need = [max(0.0, POVERTY - inc) for inc in incomes]
    order = sorted(range(N), key=lambda i: need[i], reverse=True)
    alloc_sorted = greedy_allocate(budget, [need[i] for i in order])
    aid = [0.0] * N
    for k, i in enumerate(order):
        aid[i] = alloc_sorted[k]
    final = [incomes[i] + aid[i] for i in range(N)]
    poor = 0
    for i in range(N):
        s = min(1.0, final[i] / POVERTY)      # 0(빈곤)~1(충분)
        balls[i].color = vector(1 - s, s, 0)
        if final[i] < POVERTY:
            poor += 1
    poverty_curve.plot(t, poor)
