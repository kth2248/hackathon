# SDG04_school_access/main.py — 교육 접근성 지도 (다른 각도)
# SDG 4. 학생들이 학교에서 멀면 교육 접근이 어렵다. 학교를 늘리면 접근률이 오른다.
import os, sys, math, random
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, box, sphere
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider
from live_graph import make_line_curve

AREA = 8.0
NUM_STUDENTS = 60
REACH = 3.5
num_schools = 2
STUDENTS = [(random.uniform(-AREA, AREA), random.uniform(-AREA, AREA)) for _ in range(NUM_STUDENTS)]
scene = make_scene("SDG04 — 교육 접근성 지도", width=900, height=560)
scene.append_to_caption("<b>학교(노랑)를 늘리면 통학권(초록) 안 학생이 늘어난다</b>\n\n")
box(pos=vector(0, -0.3, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=color.gray(0.3))
student_objs = [sphere(pos=vector(sx, 0.2, sz), radius=0.22, color=color.red) for sx, sz in STUDENTS]
access_curve = make_line_curve("교육 접근률(%)", "학교 수", "%", col=color.green)
school_objs = []
def place_schools(n):
    global school_objs
    for o in school_objs: o.visible = False
    school_objs = []
    schools = [(random.uniform(-AREA, AREA), random.uniform(-AREA, AREA)) for _ in range(n)]
    for sx, sz in schools:
        school_objs.append(box(pos=vector(sx, 0.5, sz), size=vector(0.8, 1, 0.8), color=color.yellow))
    reached = 0
    for i, (x, z) in enumerate(STUDENTS):
        ok = any(math.hypot(x - kx, z - kz) <= REACH for kx, kz in schools)
        student_objs[i].color = color.green if ok else color.red
        reached += ok
    access_curve.plot(n, 100.0 * reached / NUM_STUDENTS)
def on_schools(v):
    global num_schools
    num_schools = int(v); place_schools(num_schools)
make_labeled_slider(1, 10, num_schools, on_schools, "학교 수", length=320, decimals=0)
place_schools(num_schools)
while True:
    rate(20)
