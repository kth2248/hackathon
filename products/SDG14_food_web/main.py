# SDG14_food_web/main.py — 해양 먹이사슬 (포식자-피식자, 다른 각도)
# SDG 14. 물고기(피식)와 포식자의 개체수 진동. 플라스틱 오염이 피식자 성장을 억제한다.
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, label
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

prey, pred = 40.0, 9.0
pollution = 0.0
DT = 0.04
scene = make_scene("SDG14 — 해양 먹이사슬(포식자-피식자)", width=900, height=560)
scene.append_to_caption("<b>물고기와 포식자 개체수의 진동. 플라스틱 오염이 물고기 성장을 억제</b>\n\n")
box(pos=vector(0, -1, 0), size=vector(10, 0.2, 4), color=vector(0.1, 0.3, 0.5))
prey_box = box(pos=vector(-2, 0, 0), size=vector(1.5, 0.1, 1.5), color=color.cyan)
pred_box = box(pos=vector(2, 0, 0), size=vector(1.5, 0.1, 1.5), color=color.red)
label(pos=vector(-2, -0.6, 0), text="물고기", box=False, height=14)
label(pos=vector(2, -0.6, 0), text="포식자", box=False, height=14)
def on_poll(v):
    global pollution
    pollution = v
make_labeled_slider(0.0, 0.9, pollution, on_poll, "플라스틱 오염", length=320, decimals=2)
prey_c, pred_c = make_lines("개체수 진동", "시간", "개체수",
                            [("물고기", color.cyan), ("포식자", color.red)])
t = 0
while True:
    rate(40)
    alpha = 0.7 * (1 - pollution * 0.8)      # 오염이 물고기 번식률 억제
    beta, delta, gamma = 0.02, 0.012, 0.5
    dprey = prey * (alpha - beta * pred)
    dpred = pred * (delta * prey - gamma)
    prey = max(0.0, min(200.0, prey + dprey * DT))
    pred = max(0.0, min(200.0, pred + dpred * DT))
    t += 1
    prey_box.size = vector(1.5, max(0.05, prey / 15), 1.5); prey_box.pos = vector(-2, prey_box.size.y / 2 - 0.9, 0)
    pred_box.size = vector(1.5, max(0.05, pred / 15), 1.5); pred_box.pos = vector(2, pred_box.size.y / 2 - 0.9, 0)
    if t % 3 == 0:
        prey_c.plot(t, prey); pred_c.plot(t, pred)
