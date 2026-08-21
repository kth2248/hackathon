# demo_ui_widgets.py
"""
ui_widgets.py의 슬라이더/토글이 브라우저에서 실제로 조작되는지 빠르게 확인하는 데모.
offline_test.py와 별개로, 'UI 위젯만' 눈으로 검증하는 용도.

실행 방법:
    python demo_ui_widgets.py
브라우저 창이 뜨고, 슬라이더를 움직이거나 체크박스를 누르면 아래 구슬이 반응하면 정상.
"""
from vpython import canvas, sphere, vector, color, rate

import os, sys
for _cat in ("ui", "scene", "vectors"):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", _cat))
from ui_widgets import make_labeled_slider, make_toggle

scene = canvas(title="UI 위젯 데모 — 슬라이더/토글 동작 확인", width=800, height=500)

ball = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.cyan)

# --- 조작할 상태 변수 ---
state = {"radius": 0.5, "visible": True}


def on_radius_change(value):
    """슬라이더로 구슬 크기 조절."""
    state["radius"] = value
    ball.radius = value


def on_visible_toggle(checked):
    """체크박스로 구슬 표시/숨김."""
    state["visible"] = checked
    ball.visible = checked


# 슬라이더 + 라벨: 구슬 반지름 0.1 ~ 2.0
make_labeled_slider(0.1, 2.0, 0.5, on_radius_change, "구슬 크기", unit="")

# 줄바꿈용 여백
scene.append_to_caption("\n\n")

# 토글 + 라벨: 구슬 보이기/숨기기
make_toggle("구슬: 보임", "구슬: 숨김", on_visible_toggle, initial=True)

print("데모 실행 중 — 브라우저에서 슬라이더/체크박스를 조작해 보세요. (Ctrl+C로 종료)")

# 창을 유지하기 위한 최소 루프 (구슬을 천천히 회전시켜 살아있음을 표시)
angle = 0
while True:
    rate(30)
    angle += 0.01
    # 구슬을 원 궤도로 살짝 움직여 화면이 살아있음을 보여줌
    ball.pos = vector(2 * __import__("math").cos(angle), 2 * __import__("math").sin(angle), 0)
