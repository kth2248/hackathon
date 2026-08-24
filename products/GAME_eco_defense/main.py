# GAME_eco_defense/main.py — 에코 타워디펜스 (게임 + AI + SDG 통합)
#
# SDG 7·11·13(에너지·도시·기후). 게임 프로그래밍 + AI를 한 번에:
#   · 게임: 타워 설치, 웨이브, 자원(에너지 크레딧), 기지 체력, 점수, 승패, 재시작
#   · AI  : 오염 몬스터가 A* 경로탐색으로 기지까지 옴(타워를 세우면 스스로 우회) + 타워 자동 조준
#   · SDG : 재생에너지 타워로 밀려오는 '오염'을 막아 도시를 지킨다
#
# 실행: python main.py  →  화면(격자 칸)을 클릭해 타워 설치. 몬스터가 기지에 닿으면 체력 감소.

import os
import sys

_PARTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "parts"))
for _c in ("vectors", "scene", "ui", "pathfinding", "world", "steering",
           "optimization", "nlp", "models", "risk", "generation", "dataviz",
           "input", "gameai"):
    sys.path.insert(0, os.path.join(_PARTS, _c))

from vpython import canvas, box, sphere, cylinder, vector, color, rate, wtext, button
from grid import GridWorld
from astar import astar
from grid_render import cell_pos

# ============================================================
# 1. 설정
# ============================================================
COLS, ROWS = 14, 10
SPAWN = (0, 5)
BASE = (13, 5)
ENEMY_SPEED = 0.07
ENEMY_HP = 30.0
TOWER_RANGE = 2.6
TOWER_DPS = 0.5          # 프레임당 데미지
TOWER_COST = 20
KILL_REWARD = 8
START_CREDITS = 100
BASE_HP = 10
FPS = 30

world = GridWorld(COLS, ROWS)

# ============================================================
# 2. 씬 (탑다운 시점)
# ============================================================
scene = canvas(title="에코 타워디펜스 — 칸을 클릭해 재생에너지 타워 설치! 오염(빨강)을 막으세요",
               width=940, height=600, background=vector(0.05, 0.1, 0.15))
scene.center = vector(0, 0, 0)
scene.forward = vector(0, -1, 0.0001)
scene.up = vector(0, 0, -1)
scene.range = COLS * 0.55
scene.userspin = False
scene.userzoom = False

# 바닥 격자(옅은 타일)
for x in range(COLS):
    for y in range(ROWS):
        box(pos=cell_pos(world, (x, y), y=-0.1), size=vector(0.92, 0.05, 0.92),
            color=color.gray(0.2))
# 스폰(회색)·기지(초록) 표시
box(pos=cell_pos(world, SPAWN, y=0), size=vector(0.9, 0.2, 0.9), color=color.gray(0.5))
base_obj = box(pos=cell_pos(world, BASE, y=0.1), size=vector(0.9, 0.6, 0.9), color=color.green)

hud = wtext(text="")
status = wtext(text="\n")

# ============================================================
# 3. 상태
# ============================================================
towers = set()          # 타워가 놓인 칸(장애물)
tower_objs = []         # {obj, beam, cell}
enemies = []            # {obj, hp}
credits = START_CREDITS
base_hp = BASE_HP
score = 0
wave = 0
to_spawn = 0
path_version = 0
over = False


def passable(cell):
    return world.in_bounds(cell) and cell not in towers


def start_game():
    global credits, base_hp, score, wave, to_spawn, path_version, over, towers
    for t in tower_objs:
        t["obj"].visible = False
        t["beam"].visible = False
    tower_objs.clear()
    for e in enemies:
        e["obj"].visible = False
    enemies.clear()
    towers = set()
    credits = START_CREDITS
    base_hp = BASE_HP
    score = 0
    wave = 0
    to_spawn = 0
    path_version += 1
    over = False
    status.text = "\n"


button(text="다시 시작", bind=lambda b: start_game())


# ============================================================
# 4. 타워 설치 (마우스 클릭)
# ============================================================
def on_click(evt=None):
    global credits, path_version
    if over:
        return
    p = scene.mouse.pos
    cell = world.world_to_cell(p.x, p.z)
    if not world.in_bounds(cell) or cell in (SPAWN, BASE) or cell in towers:
        return
    if credits < TOWER_COST:
        status.text = "  에너지 크레딧이 부족합니다.\n"
        return
    # 이 칸을 막아도 스폰→기지 길이 남아 있어야 설치 가능(완전 봉쇄 금지)
    towers.add(cell)
    if not astar(SPAWN, BASE, passable):
        towers.discard(cell)
        status.text = "  여기 지으면 길이 완전히 막혀요! (다른 칸에)\n"
        return
    credits -= TOWER_COST
    obj = cylinder(pos=cell_pos(world, cell, y=0), axis=vector(0, 0.7, 0),
                   radius=0.32, color=color.cyan)
    beam = cylinder(pos=cell_pos(world, cell, y=0.4), axis=vector(0, 0, 0),
                    radius=0.05, color=color.yellow, visible=False)
    tower_objs.append({"obj": obj, "beam": beam, "cell": cell})
    path_version += 1          # 몬스터들이 새 지형으로 우회 재탐색
    status.text = "\n"


scene.bind("click", on_click)

start_game()


# ============================================================
# 5. 게임 루프
# ============================================================
def spawn_enemy():
    e = sphere(pos=cell_pos(world, SPAWN, y=0.3), radius=0.3, color=color.red)
    enemies.append({"obj": e, "hp": ENEMY_HP, "path": [], "ver": -1})


frame = 0
while True:
    rate(FPS)
    if over:
        continue
    frame += 1

    # 5-1. 웨이브: 남은 소환이 있으면 주기적으로, 없고 적도 없으면 다음 웨이브
    if to_spawn > 0:
        if frame % 25 == 0:
            spawn_enemy()
            to_spawn -= 1
    elif not enemies:
        wave += 1
        to_spawn = 3 + wave

    # 5-2. 몬스터 이동 (A* 경로 따라 기지로)
    for e in list(enemies):
        # 타워가 바뀌었으면 현재 칸에서 경로 재탐색(= AI 우회)
        if e["ver"] != path_version or not e["path"]:
            cur = world.world_to_cell(e["obj"].pos.x, e["obj"].pos.z)
            p = astar(cur, BASE, passable)
            e["path"] = p[1:] if p and len(p) > 1 else []
            e["ver"] = path_version
        if e["path"]:
            target = cell_pos(world, e["path"][0], y=0.3)
            d = target - e["obj"].pos
            if d.mag < 0.12:
                e["obj"].pos = target
                e["path"].pop(0)
            else:
                e["obj"].pos = e["obj"].pos + d.norm() * ENEMY_SPEED
        # 기지 도달?
        if (e["obj"].pos - cell_pos(world, BASE, y=0.3)).mag < 0.6:
            e["obj"].visible = False
            enemies.remove(e)
            globals()["base_hp"] = base_hp - 1

    # 5-3. 타워 자동 조준·공격
    for t in tower_objs:
        nearest, nd = None, TOWER_RANGE
        for e in enemies:
            dd = (e["obj"].pos - t["obj"].pos).mag
            if dd < nd:
                nd, nearest = dd, e
        if nearest is not None:
            nearest["hp"] -= TOWER_DPS
            t["beam"].visible = True
            t["beam"].pos = t["obj"].pos + vector(0, 0.4, 0)
            t["beam"].axis = nearest["obj"].pos - t["beam"].pos
        else:
            t["beam"].visible = False

    # 5-4. 처치 판정
    for e in list(enemies):
        if e["hp"] <= 0:
            e["obj"].visible = False
            enemies.remove(e)
            globals()["credits"] = credits + KILL_REWARD
            globals()["score"] = score + 1
        else:
            # 체력에 따라 색(빨강→어두워짐)
            f = max(0.0, e["hp"] / ENEMY_HP)
            e["obj"].color = vector(0.5 + 0.5 * f, 0.1, 0.1)

    # 5-5. HUD / 승패
    hud.text = (f"  💠크레딧 {credits}   🏙️기지체력 {base_hp}   🌊웨이브 {wave}   ⭐점수 {score}"
                f"   (타워 비용 {TOWER_COST})\n")
    base_obj.color = vector(1 - base_hp / BASE_HP, base_hp / BASE_HP, 0.1)
    if base_hp <= 0:
        over = True
        status.text = f"  ☠️ 도시 오염! 게임 오버 — 최종 점수 {score}, 웨이브 {wave}  ('다시 시작')\n"
