# SDG12_recycling/main.py — 자원 순환과 재활용 (자원 흐름 모델)
#
# SDG 12(책임있는 소비·생산). 부품: resource + dataviz.
# 자원→생산→폐기 흐름에서 재활용률을 높이면 폐기물과 신규 자원 소비가 얼마나 주나.
# 탐구 포인트: "재활용률"을 올리면 누적 폐기물이 어떻게 달라지나.
import os, sys, math
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

recycle_rate = 0.2
raw_stock = 100.0        # 남은 신규 자원
waste = 0.0              # 누적 폐기물
CONSUME = 4.0            # 매 스텝 생산에 쓰는 양

scene = make_scene("SDG12 — 자원 순환과 재활용", width=900, height=560)
scene.append_to_caption("<b>재활용률을 높이면 신규 자원 소비와 폐기물이 함께 줄어든다</b>\n\n")

def on_recycle(v):
    global recycle_rate
    recycle_rate = v
make_labeled_slider(0.0, 0.9, recycle_rate, on_recycle, "재활용률", length=320, decimals=2)
raw_c, waste_c = make_lines("자원/폐기물", "시간", "양",
                            [("남은 자원", color.green), ("누적 폐기물", color.red)])

raw_box = box(pos=vector(-3, 0, 0), size=vector(2, raw_stock / 20, 2), color=color.green, opacity=0.6)
waste_box = box(pos=vector(3, 0, 0), size=vector(2, 0.1, 2), color=color.red, opacity=0.6)
label(pos=vector(-3, -1.2, 0), text="신규 자원", box=False, height=14)
label(pos=vector(3, -1.2, 0), text="누적 폐기물", box=False, height=14)

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    # 생산에 CONSUME 필요. 그 중 recycle_rate만큼은 폐기물에서 재활용, 나머지는 신규 자원에서.
    from_recycle = min(waste, CONSUME * recycle_rate)
    from_raw = CONSUME - from_recycle
    raw_stock = max(0.0, raw_stock - from_raw)
    waste = waste - from_recycle + CONSUME * (1 - recycle_rate)   # 소비 후 일부는 폐기물로
    if raw_stock <= 0:      # 자원 고갈 → 리셋 반복
        raw_stock, waste = 100.0, 0.0
        raw_c.data = []
        waste_c.data = []
    raw_box.size = vector(2, max(0.02, raw_stock / 20), 2)
    raw_box.pos = vector(-3, raw_box.size.y / 2, 0)
    waste_box.size = vector(2, max(0.02, waste / 20), 2)
    waste_box.pos = vector(3, waste_box.size.y / 2, 0)
    raw_c.plot(t, raw_stock)
    waste_c.plot(t, waste)
