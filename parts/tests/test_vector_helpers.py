# test_vector_helpers.py
"""
vector_helpers.py의 순수 수학 함수 단위 테스트.
VPython의 vector 클래스만 있으면 되므로, 무거운 3D 렌더링 없이 실행 가능.

실행 방법:
    pytest test_vector_helpers.py -v
"""
import math
import pytest
from vpython import vector

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vectors"))
from vector_helpers import (
    direction_to,
    distance,
    avoid_vector,
    clamp_speed,
    blend_vectors,
    steer_around,
)


def approx_vec(v, x, y, z, tol=1e-9):
    """벡터 성분이 기대값과 tol 오차 안에서 같은지 확인하는 헬퍼."""
    return (
        math.isclose(v.x, x, abs_tol=tol)
        and math.isclose(v.y, y, abs_tol=tol)
        and math.isclose(v.z, z, abs_tol=tol)
    )


# --- direction_to ---------------------------------------------------------

def test_direction_to_basic():
    d = direction_to(vector(0, 0, 0), vector(5, 0, 0))
    assert approx_vec(d, 1, 0, 0)


def test_direction_to_is_unit_length():
    d = direction_to(vector(1, 2, 3), vector(-4, 5, 6))
    assert math.isclose(d.mag, 1.0, abs_tol=1e-9)


def test_direction_to_diagonal():
    d = direction_to(vector(0, 0, 0), vector(3, 4, 0))
    assert approx_vec(d, 0.6, 0.8, 0)


# --- distance -------------------------------------------------------------

def test_distance_basic():
    assert math.isclose(distance(vector(0, 0, 0), vector(3, 4, 0)), 5.0)


def test_distance_is_symmetric():
    a, b = vector(1, 2, 3), vector(-2, 0, 4)
    assert math.isclose(distance(a, b), distance(b, a))


def test_distance_zero_when_same_point():
    p = vector(7, -3, 2)
    assert math.isclose(distance(p, p), 0.0)


# --- avoid_vector ---------------------------------------------------------

def test_avoid_vector_triggers_when_close():
    # 거리 1.0 < threshold 1.5 → 회피 벡터 반환
    result = avoid_vector(vector(1, 0, 0), vector(0, 0, 0), threshold=1.5)
    assert result is not None
    assert approx_vec(result, 1, 0, 0)  # 장애물 반대 방향


def test_avoid_vector_none_when_far():
    # 거리 3.0 > threshold 1.5 → None
    result = avoid_vector(vector(3, 0, 0), vector(0, 0, 0), threshold=1.5)
    assert result is None


def test_avoid_vector_result_is_unit_length():
    result = avoid_vector(vector(0.5, 0.5, 0.5), vector(0, 0, 0), threshold=2.0)
    assert result is not None
    assert math.isclose(result.mag, 1.0, abs_tol=1e-9)


# --- clamp_speed ----------------------------------------------------------

def test_clamp_speed_limits_fast_vector():
    v = clamp_speed(vector(10, 0, 0), max_speed=3.0)
    assert math.isclose(v.mag, 3.0, abs_tol=1e-9)
    assert approx_vec(v, 3, 0, 0)


def test_clamp_speed_leaves_slow_vector_unchanged():
    original = vector(1, 0, 0)
    v = clamp_speed(original, max_speed=5.0)
    assert approx_vec(v, 1, 0, 0)


def test_clamp_speed_exactly_at_max():
    v = clamp_speed(vector(0, 4, 0), max_speed=4.0)
    assert math.isclose(v.mag, 4.0, abs_tol=1e-9)


# --- blend_vectors --------------------------------------------------------

def test_blend_vectors_is_unit_length():
    b = blend_vectors(vector(1, 0, 0), vector(0, 1, 0), weight=0.5)
    assert math.isclose(b.mag, 1.0, abs_tol=1e-9)


def test_blend_vectors_full_weight_to_v1():
    # weight=1.0 → v1 방향만 반영
    b = blend_vectors(vector(1, 0, 0), vector(0, 1, 0), weight=1.0)
    assert approx_vec(b, 1, 0, 0)


def test_blend_vectors_full_weight_to_v2():
    # weight=0.0 → v2 방향만 반영
    b = blend_vectors(vector(1, 0, 0), vector(0, 1, 0), weight=0.0)
    assert approx_vec(b, 0, 1, 0)


def test_blend_vectors_equal_mix_points_diagonally():
    b = blend_vectors(vector(1, 0, 0), vector(0, 1, 0), weight=0.5)
    # 45도 대각선 → 각 성분 √2/2
    half = math.sqrt(2) / 2
    assert approx_vec(b, half, half, 0)


# --- steer_around ---------------------------------------------------------

def test_steer_around_none_when_far():
    # 거리 3.0 > threshold 1.5 → None
    result = steer_around(vector(3, 0, 0), vector(0, 0, 0), 1.5, vector(1, 0, 0))
    assert result is None


def test_steer_around_returns_unit_when_close():
    result = steer_around(vector(1, 0, 0), vector(0, 0, 0), 1.8, vector(1, 0, 0))
    assert result is not None
    assert math.isclose(result.mag, 1.0, abs_tol=1e-9)


def test_steer_around_head_on_pushes_sideways_not_backward():
    # 에이전트·장애물·목표가 일직선(head-on)일 때:
    # 뒤(-x)로만 밀면 진동한다 → 옆(y) 성분이 반드시 생겨야 함.
    travel = vector(1, 0, 0)  # 목표는 +x 방향
    result = steer_around(vector(-1, 0, 0), vector(0, 0, 0), 1.8, travel)
    assert result is not None
    assert abs(result.y) > 0.1  # 옆으로 비껴가는 성분 존재


def test_steer_around_progresses_toward_target_when_offset():
    # 장애물보다 살짝 위에 있으면, 목표(+x) 쪽으로 진행하는 접선을 골라야 함.
    travel = vector(1, 0, 0)
    result = steer_around(vector(-0.5, 0.3, 0), vector(0, 0, 0), 1.8, travel)
    assert result is not None
    # 목표 방향과 완전히 반대(뒤로만)가 아니어야 한다
    assert result.dot(travel) > -0.9


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
