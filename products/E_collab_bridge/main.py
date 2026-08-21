# E안 — 인간-AI 협업 다리 건설
#
# 컨셉: 사람(파란 구)이 슬라이더로 '다리의 목표 지점(x)'을 정하면, AI(초록 구)가 안전 규칙을
#       지키며 블록을 하나씩 놓아 다리를 완성한다. 사람이 방향을 정하고 AI가 안전하게 실행 →
#       "AI와 미래의 공존"을 협업으로 형상화.
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작)
#
# 재사용 부품: vpython_utils(make_scene) / ui_widgets(make_labeled_slider, make_toggle)

import os
import sys

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import box, sphere, vector, color, rate
from vpython_utils import make_scene
from ui_widgets import make_labeled_slider, make_toggle

# ============================================================
# 1. 설정값
# ============================================================
MAX_HEIGHT = 3.0          # 안전 규칙: 블록 높이 상한
BLOCK_SPACING = 1.0       # 블록 간 간격
START = vector(-6, 0, 0)  # AI가 다리를 놓기 시작하는 지점
STEP_FRAMES = 30          # 몇 프레임마다 블록 하나씩 (순차 건설)
UNSAFE_RISE = 0.3         # 규칙 OFF일 때 한 칸마다 올라가는 높이(불안정 연출)
HOLD_FRAMES = 90          # 목표 도달 후 완성 상태를 보여주는 시간(그 뒤 처음부터 재건설)

# ============================================================
# 2. 상태 + 콜백
# ============================================================
target_x = 0.0            # 사람이 지정한 목표 x
safe_mode = True
last_pos = vector(START.x, START.y, 0)   # 마지막으로 놓은 블록 위치
blocks = []


def on_target(v):
    global target_x
    target_x = v


def on_safe(c):
    global safe_mode
    safe_mode = c


# ============================================================
# 3. 씬 + UI
# ============================================================
scene = make_scene("E안 — 인간-AI 협업 다리 건설", width=900, height=550)
scene.append_to_caption("<b>사람이 목표를 정하고, AI가 안전 규칙을 지키며 다리를 놓는다</b>\n\n")

make_labeled_slider(-6, 6, target_x, on_target, "목표 지점 x(사람 지정)", length=320, decimals=1)
make_toggle("AI 안전 규칙: ON (평평하게 건설)", "AI 안전 규칙: OFF (불안정하게 쌓음)",
            on_safe, initial=True, checkbox_text="AI 안전 규칙")

human_marker = sphere(pos=vector(target_x, 1, 0), radius=0.3, color=color.blue)   # 사람(목표 지시자)
ai_marker = sphere(pos=last_pos + vector(0, 1, 0), radius=0.3, color=color.green)  # AI(건설자)

# ============================================================
# 4. 애니메이션 루프
# ============================================================
step_timer = 0
reached_frames = 0        # 목표 도달 후 경과 프레임(재건설 타이밍용)
while True:
    rate(60)
    step_timer += 1

    # 사람 마커는 항상 목표 지점을 가리킴
    human_marker.pos = vector(target_x, 1, 0)

    still_building = abs(last_pos.x - target_x) > BLOCK_SPACING

    if still_building:
        reached_frames = 0
        # STEP_FRAMES마다 목표를 향해 블록 하나씩 (한 번에 다 놓지 않음)
        if step_timer % STEP_FRAMES == 0:
            direction = 1 if target_x > last_pos.x else -1
            next_x = last_pos.x + BLOCK_SPACING * direction

            if safe_mode:
                next_y = min(last_pos.y, MAX_HEIGHT)   # 안전: 높이 제한 → 평평한 다리
                block_color = color.orange
            else:
                next_y = last_pos.y + UNSAFE_RISE      # 불안정: 점점 위로 쌓임
                block_color = color.red

            blocks.append(box(pos=vector(next_x, next_y, 0),
                              size=vector(0.9, 0.3, 0.9), color=block_color))
            last_pos = vector(next_x, next_y, 0)
            ai_marker.pos = last_pos + vector(0, 1, 0)   # AI 마커는 마지막 블록 위로

    elif blocks:
        # 목표 도달 → 완성된 다리를 잠깐 보여준 뒤, 처음부터 다시 건설(반복 시연)
        reached_frames += 1
        if reached_frames >= HOLD_FRAMES:
            for b in blocks:
                b.visible = False
            blocks.clear()
            last_pos = vector(START.x, START.y, 0)
            ai_marker.pos = last_pos + vector(0, 1, 0)
            reached_frames = 0
