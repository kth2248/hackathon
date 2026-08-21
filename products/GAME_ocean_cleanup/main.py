# GAME_ocean_cleanup/main.py — 바다 청소 게임 (플레이어 조작 + AI 도주 + 점수)
#
# SDG 14(해양). 게임 프로그래밍: ① 플레이어 입력(WASD) ② 적 AI 도주(flee) ③ 점수·타이머·승패.
# WASD로 청소 로봇을 움직여 제한시간 안에 플라스틱(주황)을 최대한 수거. 물고기는 도망친다.
#
# 실행: python main.py   →  화면을 한 번 클릭한 뒤 WASD(또는 화살표)로 조작.

import os
import sys
import random

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz",
           "input", "gameai"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import (canvas, box, sphere, cone, vector, color, rate, wtext, button)
from steering import flee
from keyboard import Keyboard

# ============================================================
# 1. 설정 + 씬
# ============================================================
AREA = 10.0
NUM_FISH = 10
NUM_PLASTIC = 25
PLAYER_SPEED = 0.22
FISH_SPEED = 0.14
FLEE_RADIUS = 3.0
COLLECT_R = 0.8
GAME_TIME = 45.0

scene = canvas(title="바다 청소 게임 — WASD로 로봇 조작, 제한시간 내 플라스틱 수거!",
               width=900, height=560, background=vector(0.05, 0.15, 0.28))
# 위에서 내려다보는 시점(탑다운)
scene.forward = vector(0, -1, 0.001)
scene.up = vector(0, 0, -1)
scene.range = AREA * 1.1
scene.userspin = False
scene.userzoom = False

box(pos=vector(0, -0.5, 0), size=vector(2 * AREA, 0.2, 2 * AREA), color=vector(0.08, 0.25, 0.4))

hud = wtext(text="")
msg = wtext(text="")

# 플레이어(청소 로봇) — 원뿔로 방향 표시
player = cone(pos=vector(0, 0.2, 0), axis=vector(1, 0, 0), radius=0.5, color=color.yellow)

kb = Keyboard(scene)

fish = []
plastics = []
state = {"score": 0, "time": GAME_TIME, "over": False}


def rand_pos():
    return vector(random.uniform(-AREA, AREA), 0.2, random.uniform(-AREA, AREA))


def start_game():
    for f in fish:
        f["obj"].visible = False
    for p in plastics:
        p.visible = False
    fish.clear()
    plastics.clear()
    for _ in range(NUM_FISH):
        fish.append({"obj": sphere(pos=rand_pos(), radius=0.3, color=color.cyan),
                     "vel": vector(random.uniform(-1, 1), 0, random.uniform(-1, 1)).norm()})
    for _ in range(NUM_PLASTIC):
        plastics.append(sphere(pos=rand_pos(), radius=0.22, color=color.orange))
    player.pos = vector(0, 0.2, 0)
    state["score"] = 0
    state["time"] = GAME_TIME
    state["over"] = False
    msg.text = ""


button(text="다시 시작", bind=lambda b: start_game())
start_game()

# ============================================================
# 2. 게임 루프
# ============================================================
FPS = 40
while True:
    rate(FPS)
    if state["over"]:
        continue

    # ── ① 플레이어 입력(WASD) ──
    dx, dz = kb.axis()
    move = vector(dx, 0, dz)
    if move.mag > 0:
        newp = player.pos + move.norm() * PLAYER_SPEED
        newp.x = max(-AREA, min(AREA, newp.x))
        newp.z = max(-AREA, min(AREA, newp.z))
        player.pos = newp
        player.axis = move.norm() * 0.8      # 바라보는 방향 갱신

    # ── ② 적(물고기) AI: 플레이어가 가까우면 도주, 아니면 헤엄 ──
    for f in fish:
        pos = f["obj"].pos
        if (pos - player.pos).mag < FLEE_RADIUS:
            f["vel"] = flee(pos, player.pos, 1.0)          # 도주 행동
        else:
            # 가끔 방향을 살짝 틀며 헤엄
            f["vel"] = (f["vel"] + vector(random.uniform(-0.3, 0.3), 0,
                                          random.uniform(-0.3, 0.3))).norm()
        np = pos + f["vel"] * FISH_SPEED
        if abs(np.x) > AREA:
            f["vel"].x *= -1
        if abs(np.z) > AREA:
            f["vel"].z *= -1
        np.x = max(-AREA, min(AREA, np.x))
        np.z = max(-AREA, min(AREA, np.z))
        f["obj"].pos = np

    # ── 플라스틱 수거 판정 ──
    for p in list(plastics):
        if (p.pos - player.pos).mag < COLLECT_R:
            p.visible = False
            plastics.remove(p)
            state["score"] += 1

    # ── ③ 점수·타이머·승패 ──
    state["time"] -= 1.0 / FPS
    hud.text = f"  점수: {state['score']}   남은 시간: {max(0, state['time']):.1f}s   남은 쓰레기: {len(plastics)}\n"

    if not plastics:
        state["over"] = True
        msg.text = f"  🎉 클리어! 모든 플라스틱 수거! 최종 점수 {state['score']}  ('다시 시작' 클릭)\n"
    elif state["time"] <= 0:
        state["over"] = True
        msg.text = f"  ⏰ 시간 종료! 점수 {state['score']} (쓰레기 {len(plastics)}개 남음)  ('다시 시작' 클릭)\n"
