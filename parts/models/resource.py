# parts/models/resource.py
"""
자원/저수지 모델: 시간에 따라 자원(물·전력 등)이 들어오고 나가는 변화를 한 스텝씩 계산.
순수 파이썬 — vpython 불필요.

사용처: C 물 나눠 쓰기(저수지 수위), E 에너지(전력 수급).
"""


def reservoir_step(level, inflow, outflow, capacity=None):
    """저수지 수위 한 스텝 갱신. level + 유입 - 유출, 0 아래로는 안 내려감.
    capacity를 주면 그 위로도 안 넘침(넘치는 물은 방류).
    """
    lvl = level + inflow - outflow
    lvl = max(0.0, lvl)
    if capacity is not None:
        lvl = min(lvl, capacity)
    return lvl


def shortage(demand, supplied):
    """부족량 = max(0, 필요 - 공급). 0이면 충분히 공급된 것."""
    return max(0.0, demand - supplied)
