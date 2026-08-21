# SDG04_education/main.py — 자연어 코딩 학습 도구 (자연어 파서 + 절차 배치)
#
# SDG 4(양질의 교육). 부품: nlp.command_parser + generation.patterns.
# "빨간 공 5개를 원으로" 처럼 말로 명령하면 3D로 생성 — 코딩을 쉽게 배우는 교육용.
# 탐구 포인트: 규칙기반 파서가 문장을 어떻게 명령으로 바꾸나(자연어처리 기본 원리).
import os, sys
_P = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors","scene","ui","pathfinding","world","steering","optimization","nlp","models","risk","generation","dataviz"):
    sys.path.insert(0, os.path.join(_P, _c))
from vpython import color, rate, vector, sphere, box, winput, wtext
from vpython_utils import make_scene
from command_parser import extract_count, extract_keyword
from patterns import line_positions, circle_positions, grid_positions

COLOR_MAP = {"빨간": color.red, "빨강": color.red, "파란": color.blue, "파랑": color.blue,
             "초록": color.green, "노란": color.yellow, "주황": color.orange}
SHAPE_MAP = {"공": "sphere", "구": "sphere", "박스": "box", "상자": "box", "큐브": "box"}

scene = make_scene("SDG04 — 말로 배우는 코딩(자연어→3D)", width=900, height=560)
scene.append_to_caption("<b>문장을 입력(Enter)하면 파서가 해석해 3D로 만든다 — 교육용</b>\n\n")
status = wtext(text="예) 빨간 공 5개를 원으로   /   파란 박스 4개를 줄로\n")

made = []
def clear_made():
    global made
    for o in made:
        o.visible = False
    made = []

def build(text):
    clear_made()
    col = extract_keyword(text, COLOR_MAP, color.white)
    shape = extract_keyword(text, SHAPE_MAP, "sphere")
    n = extract_count(text, default=1, max_count=40)
    if "원" in text or "동그라" in text:
        pts = circle_positions(n)
    elif "격자" in text or "그리드" in text:
        pts = grid_positions(n)
    else:
        pts = line_positions(n)
    for (x, y, z) in pts:
        if shape == "box":
            made.append(box(pos=vector(x, y, z), size=vector(0.7, 0.7, 0.7), color=col))
        else:
            made.append(sphere(pos=vector(x, y, z), radius=0.4, color=col))
    status.text = f"생성: {shape} {n}개  (입력: \"{text}\")\n"

def on_submit(w):
    build(w.text)

scene.append_to_caption("\n명령 입력 → ")
winput(bind=on_submit, type="string", text="빨간 공 5개를 원으로")
scene.append_to_caption("  ← Enter\n")
build("빨간 공 5개를 원으로")
while True:
    rate(20)
