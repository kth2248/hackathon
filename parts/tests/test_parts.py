# parts/tests/test_parts.py
"""
순수 부품(vpython 불필요) 자동 테스트.
실행: parts 폴더에서  ->  pytest tests/test_parts.py -v
"""
import os
import sys
import random

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _sub in ["pathfinding", "world", "optimization", "nlp", "models", "risk", "generation", "gameai", "stats"]:
    sys.path.insert(0, os.path.join(_ROOT, _sub))

from astar import astar, path_length
from grid import GridWorld
from genetic import genetic_optimize
from allocate import proportional_allocate, greedy_allocate, satisfaction
from command_parser import extract_count, extract_keyword, extract_all_counts
from epidemic import infect_step, counts
from resource import reservoir_step, shortage
from risk import risk_score
from patterns import line_positions, spiral_positions, circle_positions, grid_positions
from fsm import FSM
from stats import pearson, minmax_scale


# --- A* 경로탐색 ---------------------------------------------------------
def test_astar_straight_line():
    passable = lambda c: 0 <= c[0] <= 5 and 0 <= c[1] <= 5
    path = astar((0, 0), (5, 0), passable)
    assert path[0] == (0, 0) and path[-1] == (5, 0)
    assert path_length(path) == 5


def test_astar_goes_around_wall():
    # x=2 열을 y=0..2로 막고, y=3에 통로 하나
    wall = {(2, 0), (2, 1), (2, 2), (2, 3)}
    passable = lambda c: 0 <= c[0] <= 5 and 0 <= c[1] <= 5 and c not in wall
    path = astar((0, 0), (4, 0), passable)
    assert path != []
    assert (2, 4) in path or any(c[0] == 2 and c[1] >= 4 for c in path)  # 벽 위로 우회


def test_astar_no_path_returns_empty():
    wall = {(2, y) for y in range(-5, 6)}   # 완전히 가로막음
    passable = lambda c: -5 <= c[0] <= 5 and -5 <= c[1] <= 5 and c not in wall
    assert astar((0, 0), (4, 0), passable) == []


# --- GridWorld -----------------------------------------------------------
def test_grid_passable_and_block():
    g = GridWorld(10, 10)
    assert g.passable((0, 0))
    g.block((0, 0))
    assert not g.passable((0, 0))
    assert not g.passable((-1, 0))     # 경계 밖


def test_grid_world_roundtrip():
    g = GridWorld(10, 10, cell_size=2.0)
    cell = (3, 7)
    wx, wy = g.cell_to_world(cell)
    assert g.world_to_cell(wx, wy) == cell


# --- 유전 알고리즘 -------------------------------------------------------
def test_genetic_finds_optimum():
    # f(x) = -(x-3)^2 를 최대화 -> x는 3 근처, fitness는 0 근처여야 함
    rng = random.Random(42)
    best, fit = genetic_optimize(
        create_individual=lambda: rng.uniform(-10, 10),
        fitness=lambda x: -(x - 3) ** 2,
        mutate=lambda x: x + rng.uniform(-0.5, 0.5),
        pop_size=30, generations=60, rng=rng,
    )
    assert abs(best - 3) < 0.5
    assert fit > -0.25


def test_genetic_on_generation_callback():
    rng = random.Random(1)
    seen = []
    genetic_optimize(
        create_individual=lambda: rng.uniform(-5, 5),
        fitness=lambda x: -(x * x),
        mutate=lambda x: x + rng.uniform(-0.3, 0.3),
        pop_size=10, generations=12, rng=rng,
        on_generation=lambda gen, best, fit: seen.append(gen),
    )
    assert len(seen) == 12          # 세대마다 콜백 호출


# --- 자원 배분 -----------------------------------------------------------
def test_proportional_allocate_sums_to_total():
    alloc = proportional_allocate(100, [1, 2, 2])
    assert abs(sum(alloc) - 100) < 1e-9
    assert alloc[1] == alloc[2]


def test_greedy_allocate_priority():
    alloc = greedy_allocate(10, [6, 6, 6])
    assert alloc == [6, 4, 0]


def test_satisfaction_ratio():
    assert satisfaction(5, 10) == 0.5
    assert satisfaction(20, 10) == 1.0


# --- 자연어 파서 ---------------------------------------------------------
def test_extract_count():
    assert extract_count("빨간 구 3개") == 3
    assert extract_count("나무 20그루") == 20
    assert extract_count("공을 놔줘", default=1) == 1
    assert extract_count("999개", max_count=40) == 40


def test_extract_keyword():
    cmap = {"빨간": "red", "파란": "blue"}
    assert extract_keyword("파란 상자", cmap) == "blue"
    assert extract_keyword("초록", cmap, default="white") == "white"


def test_extract_all_counts():
    m = extract_all_counts("나무 20 태양광 5", {"나무": "tree", "태양광": "solar"})
    assert m == {"tree": 20, "solar": 5}


# --- 전염병 모델 ---------------------------------------------------------
def test_infection_spreads():
    states = ["I", "S", "S"]
    ring = lambda i: [(i - 1) % 3, (i + 1) % 3]   # 원형 접촉
    new = infect_step(states, ring, p_infect=1.0, p_recover=0.0)
    assert new.count("I") == 3     # 확률 1이면 모두 감염


def test_recovery():
    states = ["I", "I"]
    new = infect_step(states, lambda i: [], p_infect=0.0, p_recover=1.0)
    assert new == ["R", "R"]


def test_counts():
    assert counts(["S", "I", "I", "R"]) == (1, 2, 1)


# --- 자원/저수지 모델 ----------------------------------------------------
def test_reservoir_clamps_at_zero():
    assert reservoir_step(5, inflow=1, outflow=10) == 0.0


def test_reservoir_capacity():
    assert reservoir_step(9, inflow=5, outflow=0, capacity=10) == 10.0


def test_shortage():
    assert shortage(10, 7) == 3
    assert shortage(10, 12) == 0


# --- 위험도 점수 ---------------------------------------------------------
def test_risk_out_of_boundary_is_max():
    assert risk_score((10, 0), [(0, 0)], boundary_radius=5, avoid_distance=1) == 100.0


def test_risk_far_from_obstacle_is_zero():
    assert risk_score((0, 0), [(100, 0)], boundary_radius=200, avoid_distance=1) == 0.0


def test_risk_increases_when_closer():
    near = risk_score((1, 0), [(0, 0)], boundary_radius=50, avoid_distance=1)
    far = risk_score((3, 0), [(0, 0)], boundary_radius=50, avoid_distance=1)
    assert near > far


def test_risk_larger_avoid_distance_means_more_risk():
    # 같은 거리에서 avoid_distance가 크면 위험이 더 높아야 함(더 멀리 피함)
    low = risk_score((2, 0), [(0, 0)], boundary_radius=50, avoid_distance=0.6)
    high = risk_score((2, 0), [(0, 0)], boundary_radius=50, avoid_distance=2.5)
    assert high > low


# --- 절차적 배치 패턴 ----------------------------------------------------
def test_line_positions_count():
    assert len(line_positions(4)) == 4


def test_spiral_positions_count():
    assert len(spiral_positions(5)) == 5


def test_circle_positions_on_radius():
    import math
    for x, y, z in circle_positions(6, radius=2):
        assert abs(math.hypot(x, y) - 2) < 1e-9


def test_circle_positions_empty():
    assert circle_positions(0) == []


def test_grid_positions_count():
    assert len(grid_positions(9)) == 9


# --- FSM (게임 AI 상태기계) ----------------------------------------------
def test_fsm_transitions():
    ai = FSM("patrol")
    ai.add("patrol", lambda c: c["dist"] < 3, "chase")
    ai.add("chase", lambda c: c["dist"] > 6, "patrol")
    assert ai.update({"dist": 10}) == "patrol"   # 멀면 순찰 유지
    assert ai.update({"dist": 2}) == "chase"      # 가까우면 추격
    assert ai.update({"dist": 2}) == "chase"      # 계속 추격
    assert ai.update({"dist": 8}) == "patrol"     # 멀어지면 순찰 복귀


# --- 통계(데이터 분석) --------------------------------------------------
def test_pearson_perfect_positive():
    assert abs(pearson([1, 2, 3, 4], [2, 4, 6, 8]) - 1.0) < 1e-9


def test_pearson_negative():
    assert pearson([1, 2, 3], [3, 2, 1]) < -0.99


def test_minmax_scale_endpoints():
    s = minmax_scale([10, 20, 30])
    assert s[0] == 0.0 and s[-1] == 100.0


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
