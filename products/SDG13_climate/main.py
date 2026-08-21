# SDG13_climate/main.py — 탄소 배출 vs 숲 흡수 (기후 모델)
#
# SDG 13(기후변화 대응). 부품: dataviz + 간단 모델.
# 탄소 배출은 기온을 올리고, 숲은 탄소를 흡수해 기온 상승을 늦춘다.
# 탐구 포인트: "숲 면적"을 늘리면 기온 상승 곡선이 얼마나 완만해지나.
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

emission = 5.0       # 매 스텝 배출량
forest = 3.0         # 숲 면적(흡수량에 비례)
co2 = 50.0
temp = 14.0          # 기온(도)

scene = make_scene("SDG13 — 탄소 배출 vs 숲 흡수", width=900, height=560)
scene.append_to_caption("<b>배출은 기온을 올리고, 숲은 탄소를 흡수해 상승을 늦춘다</b>\n\n")

def on_emission(v):
    global emission
    emission = v
def on_forest(v):
    global forest
    forest = v
make_labeled_slider(0.0, 12.0, emission, on_emission, "탄소 배출량", length=300, decimals=1)
make_labeled_slider(0.0, 12.0, forest, on_forest, "숲 면적(흡수)", length=300, decimals=1)
co2_c, temp_c = make_lines("CO2와 기온", "시간", "값",
                           [("CO2 농도", color.gray(0.6)), ("기온(도)", color.red)])

# 숲(초록 박스, 면적에 비례) + 공장(회색)
forest_box = box(pos=vector(3, 0, 0), size=vector(forest, 0.5, 3), color=color.green)
box(pos=vector(-3, 0.5, 0), size=vector(1.5, 2, 1.5), color=color.gray(0.5))

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    absorb = forest * 0.8
    co2 = max(0.0, co2 + emission - absorb)
    # 기온은 CO2가 기준(50)보다 높을수록 서서히 오름
    temp += (co2 - 50.0) * 0.002
    forest_box.size = vector(max(0.1, forest), 0.5, 3)
    forest_box.pos = vector(3, 0.25, 0)
    co2_c.plot(t, co2)
    temp_c.plot(t, temp)
    if t % 80 == 0:      # 주기적 리셋
        co2, temp = 50.0, 14.0
        co2_c.data = []
        temp_c.data = []
