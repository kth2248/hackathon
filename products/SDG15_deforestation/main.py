# SDG15_deforestation/main.py — 삼림 파괴와 재생 (격자 생태, 다른 각도)
# SDG 15. 벌목 속도 vs 재생 속도의 균형에 따라 숲(초록)이 유지되거나 사라진다.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

COLS, ROWS = 16, 16
clearing = 0.05
forest = [[True] * ROWS for _ in range(COLS)]
scene = make_scene("SDG15 — 삼림 파괴와 재생", width=900, height=560)
scene.append_to_caption("<b>벌목이 재생보다 빠르면 숲(초록)이 갈색 맨땅으로 사라진다</b>\n\n")
cells = [[box(pos=vector(x - COLS / 2, 0, y - ROWS / 2), size=vector(0.9, 0.3, 0.9), color=color.green)
          for y in range(ROWS)] for x in range(COLS)]
def on_clear(v):
    global clearing
    clearing = v
make_labeled_slider(0.0, 0.2, clearing, on_clear, "벌목 속도", length=320, decimals=3)
forest_curve = make_line_curve("숲 면적 비율(%)", "시간", "%", col=color.green)
REGROW = 0.03
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 4: continue
    t += 1
    green = 0
    for x in range(COLS):
        for y in range(ROWS):
            if forest[x][y]:
                if random.random() < clearing:
                    forest[x][y] = False
            else:
                if random.random() < REGROW:
                    forest[x][y] = True
            cells[x][y].color = color.green if forest[x][y] else vector(0.4, 0.25, 0.1)
            green += forest[x][y]
    forest_curve.plot(t, 100.0 * green / (COLS * ROWS))
