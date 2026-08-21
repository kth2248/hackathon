# SDG05_gender_equality/main.py — 편향 vs 공정 승진 시뮬 (에이전트 + 그래프)
#
# SDG 5(성평등). 부품: dataviz + 규칙 에이전트.
# 승진 규칙이 한 집단(A)에 편향되면 고위직 성비가 어떻게 갈리나. 공정하면?
# 탐구 포인트: "편향도"를 낮추면 고위직의 두 집단 비율이 얼마나 균형에 가까워지나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_lines

bias = 0.5      # 0=공정, 1=완전 A편향
TOP_LIMIT = 20  # 고위직 정원

scene = make_scene("SDG05 — 편향 vs 공정 승진", width=900, height=560)
scene.append_to_caption("<b>승진 규칙의 편향도에 따라 고위직 성비(A/B)가 어떻게 갈리나</b>\n\n")

def on_bias(v):
    global bias
    bias = v
make_labeled_slider(0.0, 1.0, bias, on_bias, "편향도(0=공정,1=A편향)", length=320, decimals=2)
A_c, B_c = make_lines("고위직 집단 비율", "시간", "인원",
                      [("A 집단", color.orange), ("B 집단", color.cyan)])

topA = topB = 0
markers = []   # 승진된 사람 시각화(위로 쌓임)
t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 4 != 0:
        continue
    t += 1
    if topA + topB < TOP_LIMIT:
        # 승진 후보 1명: 편향도에 따라 A가 뽑힐 확률↑
        pick_A = random.random() < (0.5 + 0.5 * bias)
        if pick_A:
            topA += 1
            x = -3
            col = color.orange
        else:
            topB += 1
            x = 3
            col = color.cyan
        markers.append(sphere(pos=vector(x + random.uniform(-0.5, 0.5),
                                         (topA if pick_A else topB) * 0.4, 0),
                              radius=0.25, color=col))
    else:
        # 정원 차면 리셋(정책 바꿔 재관찰)
        for m in markers:
            m.visible = False
        markers = []
        topA = topB = 0
        A_c.data = []
        B_c.data = []
    A_c.plot(t, topA)
    B_c.plot(t, topB)
