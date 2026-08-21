# SDG12_supply_chain/main.py — 순환경제 공급망 점수 (다른 각도)
# SDG 12. 원료->생산->사용->폐기 4단계에서 재사용 설계를 높이면 순환경제 점수가 오른다.
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, arrow, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

STAGES = ["원료", "생산", "사용", "폐기"]
circularity = 0.2
scene = make_scene("SDG12 — 순환경제 공급망", width=900, height=560)
scene.append_to_caption("<b>재사용 설계(순환성)를 높이면 폐기 화살표가 원료로 되돌아간다</b>\n\n")
stage_boxes = [box(pos=vector(i * 3 - 4.5, 0, 0), size=vector(1.6, 1.6, 1.6),
                   color=color.gray(0.5)) for i in range(4)]
stage_labels = [label(pos=vector(i * 3 - 4.5, 1.4, 0), text=STAGES[i], box=False, height=14) for i in range(4)]
# 되돌아가는 순환 화살표(폐기->원료)
loop_arrow = arrow(pos=vector(4.5, -1.4, 0), axis=vector(-9, 0, 0), color=color.green, shaftwidth=0.1)
def on_circ(v):
    global circularity
    circularity = v
make_labeled_slider(0.0, 1.0, circularity, on_circ, "순환성(재사용 설계)", length=320, decimals=2)
score_curve = make_line_curve("순환경제 점수 / 폐기물", "시간", "값", col=color.green)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    waste = 100 * (1 - circularity)     # 순환성 높을수록 폐기 감소
    score = 100 * circularity
    loop_arrow.opacity = 0.1 + 0.9 * circularity
    stage_boxes[3].color = vector(1 - circularity, circularity, 0)   # 폐기 단계 색
    score_curve.plot(t, waste)
