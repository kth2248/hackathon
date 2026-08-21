# main.py — "무해한 AI" 시각화 시뮬레이터 (A안 완성본, 대회 제출용)
#
# 실행: hackathon_kit 폴더 안에서  ->  python main.py
# 브라우저 창이 자동으로 뜹니다. 인터넷 없이도 동작해야 정상입니다.
#
# ┌─ 구조: 앞서 만든 '부품 상자'를 조립한 완성본 ──────────────────────────┐
# │  계산   : vector_helpers.py  (direction_to / distance / avoid_vector / blend_vectors)
# │  3D 객체: vpython_utils.py   (make_scene / make_agent / make_obstacle / make_floor)
# │  UI     : ui_widgets.py      (make_toggle / make_labeled_slider)
# │  시나리오(무해한 AI 규칙) 로직만 이 파일에 있음.
# └──────────────────────────────────────────────────────────────────────┘
#
# 주제 연결: "무해한 AI" ON  = 장애물(사람 역할)을 피해 목표로 감
#            "무해한 AI" OFF = 장애물을 무시하고 직진 + 경고색(위험한 AI 형상화)

from vpython import vector, color, rate

# --- 부품 상자에서 가져오기 (여기가 '연결 지점') ---
import os
import sys
_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))
from vector_helpers import direction_to, distance, steer_around, blend_vectors
from vpython_utils import make_scene, make_agent, make_obstacle, make_floor
from ui_widgets import make_toggle, make_labeled_slider

# ============================================================
# 1. 설정값 (발표 중 급하게 바꿔야 하면 이 구간만 수정)
# ============================================================
AGENT_START = vector(-6, 0, 0)
TARGET_POS = vector(6, 0, 0)
OBSTACLE_POSITIONS = [vector(0, 0, 0), vector(2, 1.5, 0)]  # 장애물 2개
SPEED_INIT = 0.05
THRESHOLD_INIT = 1.8
FRAME_RATE = 60           # 노트북이 느리면 30으로 낮출 것
ARRIVAL_DISTANCE = 0.4    # 이 거리 안으로 들어오면 '도착'으로 간주하고 리셋
BLEND_WEIGHT = 0.6        # 회피 방향을 얼마나 강하게 반영할지 (0~1)

AGENT_SAFE_COLOR = color.blue
AGENT_DANGER_COLOR = color.red    # 안전모드 꺼짐 + 장애물 근접 시 경고색
TARGET_COLOR = color.green
OBSTACLE_COLOR = color.orange

# ============================================================
# 2. 상태 변수 (UI 콜백들이 공유해서 읽고 쓴다)
# ============================================================
safe_mode = True
speed = SPEED_INIT
avoid_threshold = THRESHOLD_INIT


def on_toggle_safe(checked):
    """체크박스 콜백: 무해한 AI 모드 on/off."""
    global safe_mode
    safe_mode = checked


def on_speed_change(value):
    """슬라이더 콜백: 이동 속도."""
    global speed
    speed = value


def on_threshold_change(value):
    """슬라이더 콜백: 회피를 시작하는 감지 거리."""
    global avoid_threshold
    avoid_threshold = value


# ============================================================
# 3. 씬 + UI 구성 (부품 조립)
# ============================================================
scene = make_scene("무해한 AI 시각화 시뮬레이터 — AI·SW 부천 연합 해커톤",
                   width=900, height=550)

# 주제 배너 — 3D text()는 한글을 못 그리므로 캡션(HTML)으로 표시한다.
scene.append_to_caption("<b>무한한 상상, 무해한 AI</b>\n\n")

# 토글: 무해한 AI ON/OFF  (ui_widgets.make_toggle 재사용)
make_toggle("무해한 AI: ON (장애물 우회)\n",
            "무해한 AI: OFF (장애물 무시하고 돌진)\n",
            on_toggle_safe, initial=True, checkbox_text="무해한 AI 모드")

# 슬라이더 2개  (ui_widgets.make_labeled_slider 재사용)
make_labeled_slider(0.01, 0.15, SPEED_INIT, on_speed_change,
                    "이동 속도", length=300, decimals=3)
make_labeled_slider(0.5, 4.0, THRESHOLD_INIT, on_threshold_change,
                    "회피 감지 거리", length=300, decimals=1)

# 바닥 + 오브젝트  (vpython_utils 재사용)
make_floor(length=16, width=8, floor_color=color.gray(0.3), pos=vector(0, -2.5, 0))
agent = make_agent(pos=AGENT_START, radius=0.35, agent_color=AGENT_SAFE_COLOR,
                   trail=True, trail_radius=0.03)
target = make_agent(pos=TARGET_POS, radius=0.35, agent_color=TARGET_COLOR, trail=False)
obstacles = [make_obstacle(pos=p, radius=0.5, obstacle_color=OBSTACLE_COLOR)
             for p in OBSTACLE_POSITIONS]

# ============================================================
# 4. 애니메이션 루프 (여기만 '시나리오 로직')
# ============================================================
while True:
    rate(FRAME_RATE)

    # 4-1. 기본 방향: 목표를 향한 직선
    direction = direction_to(agent.pos, target.pos)

    # 4-2. 가장 가까운(=가장 위협적인) 장애물의 '돌아가는' 방향 찾기
    nearest_steer = None
    nearest_dist = float("inf")
    for obs in obstacles:
        steer = steer_around(agent.pos, obs.pos, avoid_threshold, direction)
        if steer is not None:
            d = distance(agent.pos, obs.pos)
            if d < nearest_dist:
                nearest_dist = d
                nearest_steer = steer

    # 4-3. 안전모드일 때만 '돌아가는 방향'을 목표 방향과 섞는다
    if safe_mode and nearest_steer is not None:
        direction = blend_vectors(nearest_steer, direction, weight=BLEND_WEIGHT)
        agent.color = AGENT_SAFE_COLOR
    elif not safe_mode and nearest_steer is not None:
        # 안전모드 OFF + 장애물 근접 = 위험 상태를 색으로 경고
        agent.color = AGENT_DANGER_COLOR
    else:
        agent.color = AGENT_SAFE_COLOR

    # 4-4. 위치 갱신
    agent.pos = agent.pos + direction * speed

    # 4-5. 목표 도착 시 리셋 (발표 중 무한 반복 시연용)
    if distance(agent.pos, target.pos) < ARRIVAL_DISTANCE:
        agent.clear_trail()
        agent.pos = AGENT_START
