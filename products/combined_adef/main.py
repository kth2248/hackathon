# main.py — 통합안 (A+D+E+F): 상상하고, 평가하고, 안전하게 행동하고, 함께 길을 만드는 AI
#
# 실행: 이 폴더에서  ->  python main.py   (인터넷 없이 동작)
#
# 파이프라인: F(여러 방향 상상) -> D(위험도 평가/색상) -> A(안전한 방향 선택/이동) -> E(사람과 함께 다리 건설)
#
# 재사용 부품: vector_helpers(direction_to, distance) / vpython_utils(make_scene) /
#             ui_widgets(make_toggle, make_labeled_slider)

import os
import sys
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _cat in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
             "optimization", "nlp", "models", "risk", "generation", "dataviz"):
    sys.path.insert(0, os.path.join(_PARTS, _cat))

from vpython import sphere, cylinder, box, vector, color, rate, wtext
from vector_helpers import direction_to, distance
from vpython_utils import make_scene
from ui_widgets import make_toggle, make_labeled_slider


# ============================================================
# 1. 위험도 계산 (D안 핵심) — 이 시나리오 전용 로직
# ============================================================
def compute_risk_score(pos, obstacles, boundary_radius, avoid_distance):
    """특정 위치가 얼마나 위험한지 0~100 점수로 계산.
    - 장애물과 가까울수록 위험도가 비선형(제곱)으로 급증
    - 안전 경계(F안)를 벗어나면 무조건 최대 위험도(100)
    - avoid_distance(슬라이더): 이 거리보다 가까우면 위험도 최대 → 장애물과 떨어지는 여유를 조절
    """
    if pos.mag > boundary_radius:
        return 100.0

    nearest_dist = min(distance(pos, obs) for obs in obstacles)
    influence = avoid_distance + 3.0           # 위험을 감지하기 시작하는 거리
    if nearest_dist >= influence:
        return 0.0

    # 가까울수록 위험 ↑(연속값, 포화 없음). avoid_distance가 클수록 같은 거리에서 위험이 더 큼.
    proximity = (influence - nearest_dist) / influence   # 0(멀다)~1(접촉)
    return round((proximity ** 2) * 100, 1)


# ============================================================
# 2. 설정값
# ============================================================
AGENT_START = vector(-6, 0, 0)
OBSTACLE_POSITIONS = [vector(-1, 0, 0), vector(2, 1, 0)]
NUM_CANDIDATES = 5           # F안: 매 프레임 상상하는 후보 방향 개수
BRANCH_LENGTH = 1.5          # 후보 방향선 길이
STEP_SPEED = 0.05
FRAME_RATE = 60
BRIDGE_INTERVAL = 20         # 몇 프레임마다 다리 블록을 놓을지
ARRIVAL_DISTANCE = 0.4
WOBBLE = 0.6                 # 후보 방향 흔들림 폭 (어지러우면 줄일 것)
TARGET_PULL = 40             # 목표로 가려는 힘 vs 위험 회피의 균형(클수록 직진 성향)

# ============================================================
# 3. 상태 + 콜백
# ============================================================
safe_mode = True
goal_x = 6.0
boundary_radius = 5.0
avoid_distance = 1.2         # 장애물과 유지하려는 여유 거리(슬라이더로 조절)
frame_count = 0
last_bridge_pos = vector(AGENT_START.x, AGENT_START.y, AGENT_START.z)   # 복사본(별칭 방지)


def on_safe(c):
    global safe_mode
    safe_mode = c


def on_goal(v):
    global goal_x
    goal_x = v
    target.pos = vector(goal_x, 0, 0)


def on_boundary(v):
    global boundary_radius
    boundary_radius = v
    boundary.radius = v


def on_avoid(v):
    global avoid_distance
    avoid_distance = v


# ============================================================
# 4. 씬 + UI
# ============================================================
scene = make_scene("통합안 — 상상하고 평가하고 행동하는 무해한 AI (A+D+E+F)", width=950, height=560)
# 주제 배너: 3D text()는 한글을 못 그리므로 캡션(HTML)으로 표시
scene.append_to_caption("<b>AI와 미래의 공존: 무한한 상상, 무해한 AI</b>\n\n")

make_toggle("무해한 AI: ON (위험을 피해서 이동)\n",
            "무해한 AI: OFF (위험을 알고도 무시하고 직진)\n",
            on_safe, initial=True, checkbox_text="무해한 AI 모드")
make_labeled_slider(-6, 6, goal_x, on_goal, "목표(다리 끝점) x", length=300, decimals=1)
make_labeled_slider(2, 7, boundary_radius, on_boundary, "안전 경계 반지름", length=300, decimals=1)
make_labeled_slider(0.6, 3.0, avoid_distance, on_avoid, "회피 거리(장애물 여유)", length=300, decimals=1)
risk_log = wtext(text="\n")   # 실시간 위험도 로그 (D안 강화)

# 안전 경계(F안): 투명한 구
boundary = sphere(pos=vector(0, 0, 0), radius=boundary_radius, color=color.cyan, opacity=0.12)
# 바닥
box(pos=vector(0, -2.5, 0), length=16, height=0.2, width=8, color=color.gray(0.3))

agent = sphere(pos=AGENT_START, radius=0.3, color=color.blue, make_trail=True, trail_radius=0.02)
target = sphere(pos=vector(goal_x, 0, 0), radius=0.3, color=color.green)
obstacles_objs = [sphere(pos=p, radius=0.5, color=color.orange) for p in OBSTACLE_POSITIONS]

# 후보 방향선(F안+D안): 미리 만들어 두고 매 프레임 위치/색/투명도만 갱신
candidate_lines = [cylinder(pos=AGENT_START, axis=vector(0, 0, 0), radius=0.02)
                   for _ in range(NUM_CANDIDATES)]

bridge_blocks = []

# ============================================================
# 5. 애니메이션 루프
# ============================================================
while True:
    rate(FRAME_RATE)
    frame_count += 1

    target_direction = direction_to(agent.pos, target.pos)

    # 5-1. F안: 후보 방향 상상 (목표 방향 1개 + 흔든 방향 4개)
    candidates = [target_direction]
    for _ in range(NUM_CANDIDATES - 1):
        wobble = vector(random.uniform(-WOBBLE, WOBBLE), random.uniform(-WOBBLE, WOBBLE), 0)
        candidates.append((target_direction + wobble).norm())

    # 5-2. D안: 후보별 위험도 계산 + 시각화(색상/투명도)
    #        선택 점수 = (목표로의 진행 × TARGET_PULL) − 위험.
    #        회피 거리가 커지면 위험이 더 넓게/세게 잡혀 더 크게 우회한다.
    risks = []
    best_direction = candidates[0]
    best_risk = 0.0
    best_score = float("-inf")
    for i, cand_dir in enumerate(candidates):
        hypo_pos = agent.pos + cand_dir * BRANCH_LENGTH
        risk = compute_risk_score(hypo_pos, OBSTACLE_POSITIONS, boundary_radius, avoid_distance)
        risks.append(risk)

        line = candidate_lines[i]
        line.pos = agent.pos
        line.axis = cand_dir * BRANCH_LENGTH
        line.color = vector(risk / 100, 1 - risk / 100, 0)     # 초록(안전)~빨강(위험)
        # 확장: 안전 경계를 벗어난 후보는 흐리게(고려 대상에서 제외됨을 강조)
        line.opacity = 0.2 if hypo_pos.mag > boundary_radius else 1.0

        progress = cand_dir.dot(target_direction)              # 1=목표 직진, 낮을수록 옆으로
        score = TARGET_PULL * progress - risk
        if score > best_score:
            best_score = score
            best_direction = cand_dir
            best_risk = risk

    # 5-3. A안: 안전모드에 따라 실제 이동 방향 결정
    if safe_mode:
        move_direction = best_direction          # 위험도가 가장 낮은 방향
        chosen_risk = best_risk
        agent.color = color.blue
    else:
        move_direction = target_direction         # 위험을 알고도 무시하고 직진
        chosen_risk = risks[0]                     # 후보[0] = 목표 방향
        agent.color = color.red if chosen_risk > 50 else color.blue

    agent.pos = agent.pos + move_direction * STEP_SPEED

    # 실시간 위험도 로그
    if safe_mode:
        risk_log.text = f"  이번 이동 방향 위험도: {chosen_risk:.0f}/100 → 가장 안전한 길 선택 ✅\n"
    else:
        risk_log.text = f"  이번 이동 방향 위험도: {chosen_risk:.0f}/100 → 알고도 무시하고 직진 ⚠️\n"

    # 5-4. E안: 이동 경로를 따라 다리 블록 놓기
    if frame_count % BRIDGE_INTERVAL == 0 and distance(agent.pos, last_bridge_pos) > 0.3:
        if safe_mode:
            block_color = color.orange
            block_height = 0.0                     # 안정적으로 평평하게
        else:
            block_color = color.red
            block_height = random.uniform(0, 0.6)  # 불안정하게 들쭉날쭉
        bridge_blocks.append(box(pos=vector(agent.pos.x, -2.3 + block_height, agent.pos.z),
                                 size=vector(0.5, 0.15, 0.5), color=block_color))
        last_bridge_pos = vector(agent.pos.x, agent.pos.y, agent.pos.z)   # 복사본(별칭 방지)

    # 5-5. 목표 도착 시 리셋 (반복 시연)
    if distance(agent.pos, target.pos) < ARRIVAL_DISTANCE:
        agent.clear_trail()
        agent.pos = vector(AGENT_START.x, AGENT_START.y, AGENT_START.z)
        for blk in bridge_blocks:
            blk.visible = False
        bridge_blocks = []
        last_bridge_pos = vector(AGENT_START.x, AGENT_START.y, AGENT_START.z)
