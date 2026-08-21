# SDG08_skill_match/main.py — 일자리 스킬 매칭 (다른 각도)
# SDG 8. 노동자의 스킬과 일자리 요구 스킬을 매칭. 교육투자(스킬↑)로 매칭률을 올린다.
import os, sys, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, cylinder
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

N = 12
training = 0.0
worker_skill = [random.uniform(0, 6) for _ in range(N)]
job_req = sorted([random.uniform(2, 8) for _ in range(N)])
scene = make_scene("SDG08 — 일자리 스킬 매칭", width=900, height=560)
scene.append_to_caption("<b>노동자 스킬(왼쪽)이 일자리 요구(오른쪽) 이상이면 매칭(초록선)</b>\n\n")
def on_train(v):
    global training
    training = v
make_labeled_slider(0.0, 5.0, training, on_train, "직업훈련 투자", length=320, decimals=1)
match_curve = make_line_curve("매칭된 일자리 수", "시간", "매칭", col=color.green)
w_balls = [sphere(pos=vector(-4, i * 0.8 - N * 0.4, 0), radius=0.25, color=color.cyan) for i in range(N)]
j_balls = [sphere(pos=vector(4, i * 0.8 - N * 0.4, 0), radius=0.25, color=color.orange) for i in range(N)]
links = []
t = 0; frame = 0
while True:
    rate(30); frame += 1
    if frame % 6: continue
    t += 1
    for lk in links: lk.visible = False
    links = []
    skills = [min(10, worker_skill[i] + training) for i in range(N)]
    used = [False] * N
    matched = 0
    for i in range(N):        # 각 노동자를 조건 맞는 가장 낮은 일자리에 매칭
        for j in range(N):
            if not used[j] and skills[i] >= job_req[j]:
                used[j] = True; matched += 1
                links.append(cylinder(pos=w_balls[i].pos,
                                      axis=j_balls[j].pos - w_balls[i].pos,
                                      radius=0.03, color=color.green))
                break
    match_curve.plot(t, matched)
