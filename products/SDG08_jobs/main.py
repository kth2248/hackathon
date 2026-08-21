# SDG08_jobs/main.py — 노동 배치와 실업 (자원배분)
#
# SDG 8(양질의 일자리·성장). 부품: allocate.proportional_allocate.
# 노동자를 여러 산업에 배치할 때 일자리 수요를 못 채우면 실업이 생긴다.
# 탐구 포인트: 총 노동자 수를 바꾸면 실업률이 어떻게 변하나(수요-공급 균형).
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere, label
from vpython_utils import make_scene
from allocate import proportional_allocate
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

INDUSTRIES = ["농업", "제조", "서비스"]
JOB_OPENINGS = [15.0, 25.0, 30.0]     # 산업별 일자리 수
IND_COLORS = [color.green, color.orange, color.cyan]
workers = 60.0

scene = make_scene("SDG08 — 노동 배치와 실업", width=900, height=560)
scene.append_to_caption("<b>노동자를 산업에 배치. 일자리보다 노동자가 많으면 실업 발생</b>\n\n")

def on_workers(v):
    global workers
    workers = v
make_labeled_slider(0, 120, workers, on_workers, "총 노동자 수", length=320, decimals=0)
unemp_curve = make_line_curve("실업자 수", "시간", "인원", col=color.red)

# 산업 기둥(고용된 인원에 비례해 높이 변함)
bars = [box(pos=vector(i * 3 - 3, 0, 0), size=vector(1.5, 0.1, 1.5), color=IND_COLORS[i]) for i in range(3)]
labels = [label(pos=vector(i * 3 - 3, -0.8, 0), text=INDUSTRIES[i], box=False, height=14) for i in range(3)]

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    total_jobs = sum(JOB_OPENINGS)
    # 일자리 비율대로 노동자 배치, 단 각 산업은 일자리 수까지만 고용
    placed = proportional_allocate(min(workers, total_jobs), JOB_OPENINGS)
    employed = [min(placed[i], JOB_OPENINGS[i]) for i in range(3)]
    unemployed = max(0.0, workers - sum(employed))
    for i in range(3):
        h = max(0.1, employed[i] / 5)
        bars[i].size = vector(1.5, h, 1.5)
        bars[i].pos = vector(i * 3 - 3, h / 2, 0)
    unemp_curve.plot(t, unemployed)
