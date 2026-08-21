# vector_helpers.py
"""
VPython vector 객체를 다루는 순수 수학 함수 모음.
특정 시나리오(A/B/C안) 로직을 포함하지 않는다 — 어떤 아이디어를 선택해도 100% 재사용 가능.
"""
from vpython import vector


def direction_to(from_pos: vector, to_pos: vector) -> vector:
    """from_pos에서 to_pos로 향하는 단위 벡터.
    물리적 의미: 목표 지점을 향한 '이동 방향' 계산에 사용.
    """
    return (to_pos - from_pos).norm()


def distance(pos_a: vector, pos_b: vector) -> float:
    """두 점 사이 유클리드 거리. 충돌 판정, 회피 트리거 조건 등에 공통 사용."""
    return (pos_a - pos_b).mag


def avoid_vector(agent_pos: vector, obstacle_pos: vector, threshold: float = 1.5):
    """장애물이 threshold보다 가까우면 회피 방향(단위 벡터) 반환, 아니면 None.
    A안(무해한 AI 회피)뿐 아니라 C안(군집 충돌 회피)에도 그대로 사용 가능.
    """
    d = distance(agent_pos, obstacle_pos)
    if d < threshold:
        return (agent_pos - obstacle_pos).norm()
    return None


def clamp_speed(velocity: vector, max_speed: float) -> vector:
    """속도 벡터가 max_speed를 넘지 않도록 제한. 물리 시뮬레이션 안정성에 필수."""
    if velocity.mag > max_speed:
        return velocity.norm() * max_speed
    return velocity


def blend_vectors(v1: vector, v2: vector, weight: float = 0.5) -> vector:
    """두 방향 벡터를 weight 비율로 혼합 후 정규화.
    예: '목표로 가는 방향' + '장애물 회피 방향'을 함께 반영할 때 사용 (A안 핵심 로직).
    """
    blended = v1 * weight + v2 * (1 - weight)
    return blended.norm()


def steer_around(agent_pos: vector, obstacle_pos: vector, threshold: float, travel_dir: vector):
    """장애물이 threshold보다 가까우면 '옆으로 돌아가는(접선) 방향'(단위 벡터)을 반환, 아니면 None.

    왜 avoid_vector(정반대로 밀기)로는 부족한가:
      장애물이 목표와 일직선에 있으면 '뒤로 밀기'가 목표 방향과 정반대라
      앞으로 갔다 뒤로 갔다 무한 반복(진동)한다.
    이 함수는 진행 방향(travel_dir)에 대해 '옆으로 비껴' 장애물을 감싸고 지나가도록
    접선 방향을 만들어 그 문제를 없앤다.
    """
    d = distance(agent_pos, obstacle_pos)
    if d >= threshold:
        return None
    away = (agent_pos - obstacle_pos).norm()      # 장애물에서 멀어지는(반경) 방향
    tangent = vector(-away.y, away.x, 0)          # away에 수직 = 옆으로 도는 방향
    if tangent.dot(travel_dir) < 0:               # 목표 쪽으로 진행하는 쪽을 선택
        tangent = -tangent
    # 접선(옆으로) 위주 + 약간 바깥으로(away) → 장애물을 감싸며 통과
    return blend_vectors(tangent, away, weight=0.75)
