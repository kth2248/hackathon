# SDG10_inequality/main.py — 부의 불평등과 재분배 (지니계수 그래프)
#
# SDG 10(불평등 감소). 부품: dataviz + 규칙 실험.
# '부익부' 규칙은 격차를 키우고, 재분배는 줄인다. 지니계수(0=평등,1=극단)로 측정.
# 탐구 포인트: "재분배 강도"를 높이면 지니계수가 얼마나 낮아지나.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 20
redistribution = 0.0     # 0=재분배 없음, 1=완전 균등화
wealth = [random.uniform(5, 15) for _ in range(N)]

def gini(xs):
    s = sorted(xs)
    n = len(s)
    tot = sum(s)
    if tot == 0:
        return 0.0
    cum = sum((i + 1) * v for i, v in enumerate(s))
    return (2 * cum) / (n * tot) - (n + 1) / n

scene = make_scene("SDG10 — 불평등과 재분배 (지니계수)", width=900, height=560)
scene.append_to_caption("<b>부익부 vs 재분배. 막대는 개인 재산, 그래프는 지니계수(낮을수록 평등)</b>\n\n")

def on_redis(v):
    global redistribution
    redistribution = v
make_labeled_slider(0.0, 1.0, redistribution, on_redis, "재분배 강도", length=320, decimals=2)
gini_curve = make_line_curve("지니계수(0=평등 ~ 1=극단)", "시간", "지니", col=color.red)

bars = [box(pos=vector(i * 0.8 - N * 0.4, 0, 0), size=vector(0.6, wealth[i], 0.6), color=color.cyan) for i in range(N)]

t = 0
frame = 0
while True:
    rate(30)
    frame += 1
    if frame % 6 != 0:
        continue
    t += 1
    # 부익부: 재산 비례로 이익이 붙음(부자가 더 벌기 쉬움)
    total = sum(wealth)
    for i in range(N):
        wealth[i] += (wealth[i] / total) * 3.0 * random.uniform(0.5, 1.5)
    # 재분배: 평균 쪽으로 당김
    avg = sum(wealth) / N
    for i in range(N):
        wealth[i] += (avg - wealth[i]) * redistribution
    for i in range(N):
        h = max(0.05, wealth[i])
        bars[i].size = vector(0.6, h, 0.6)
        bars[i].pos = vector(i * 0.8 - N * 0.4, h / 2, 0)
    gini_curve.plot(t, gini(wealth))
    if t % 60 == 0:      # 주기적 리셋(초기화해 다시 관찰)
        for i in range(N):
            wealth[i] = random.uniform(5, 15)
        gini_curve.data = []
