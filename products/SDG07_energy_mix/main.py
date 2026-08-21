# SDG07_energy_mix/main.py — 발전 믹스 대시보드 (다른 각도)
# SDG 7. 태양광/풍력/석탄 비율을 조절해 CO2와 비용의 균형을 맞춘다.
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

solar, wind = 0.3, 0.3        # 나머지는 석탄
scene = make_scene("SDG07 — 발전 믹스 대시보드", width=900, height=560)
scene.append_to_caption("<b>재생에너지 비율을 높이면 CO2는 줄지만 비용이 오른다(트레이드오프)</b>\n\n")
def on_solar(v):
    global solar
    solar = v
def on_wind(v):
    global wind
    wind = v
make_labeled_slider(0.0, 1.0, solar, on_solar, "태양광 비율", length=300, decimals=2)
make_labeled_slider(0.0, 1.0, wind, on_wind, "풍력 비율", length=300, decimals=2)
co2_c, cost_c = make_lines("CO2 vs 비용", "시간", "값",
                           [("CO2", color.gray(0.6)), ("비용", color.orange)])
co2_box = box(pos=vector(-2, 0, 0), size=vector(1.5, 0.1, 1.5), color=color.gray(0.5))
cost_box = box(pos=vector(2, 0, 0), size=vector(1.5, 0.1, 1.5), color=color.orange)
label(pos=vector(-2, -0.9, 0), text="CO2", box=False, height=14)
label(pos=vector(2, -0.9, 0), text="비용", box=False, height=14)
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    coal = max(0.0, 1 - solar - wind)
    co2 = coal * 100                       # 석탄만 CO2 배출
    cost = solar * 60 + wind * 45 + coal * 25   # 재생에너지가 더 비쌈
    co2_box.size = vector(1.5, max(0.05, co2 / 20), 1.5); co2_box.pos = vector(-2, co2_box.size.y / 2, 0)
    cost_box.size = vector(1.5, max(0.05, cost / 20), 1.5); cost_box.pos = vector(2, cost_box.size.y / 2, 0)
    co2_c.plot(t, co2); cost_c.plot(t, cost)
