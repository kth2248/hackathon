# parts/risk/risk.py
"""
위험도 점수(Risk Score): 특정 위치가 장애물/경계 대비 얼마나 위험한지 0~100으로 계산.
순수 파이썬 — vpython 불필요, 테스트 가능. (combined_adef의 compute_risk_score를 부품화)

사용처: A 대피, D 로봇 함대, 통합안 — "AI가 위험을 인식·판단"하는 부분.

좌표는 (x, y) 또는 (x, y, z) 튜플. vpython 앱에서는 (agent.pos.x, agent.pos.y, agent.pos.z)처럼 넘긴다.
"""
import math


def _dist(a, b):
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


def _mag(a):
    return math.sqrt(sum(ai * ai for ai in a))


def risk_score(pos, obstacles, boundary_radius, avoid_distance):
    """pos의 위험도(0~100).
    - 원점 기준 boundary_radius 경계 밖이면 100(최대)
    - 장애물에 가까울수록 위험 ↑ (연속값, 포화 없음)
    - avoid_distance가 클수록 같은 거리에서 위험이 더 커짐(더 멀리 피하게 됨)
    """
    if _mag(pos) > boundary_radius:
        return 100.0
    if not obstacles:
        return 0.0
    nearest = min(_dist(pos, o) for o in obstacles)
    influence = avoid_distance + 3.0            # 위험 감지 시작 거리
    if nearest >= influence:
        return 0.0
    proximity = (influence - nearest) / influence   # 0(멀다)~1(접촉)
    return round((proximity ** 2) * 100, 1)
