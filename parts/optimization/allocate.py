# parts/optimization/allocate.py
"""
자원 배분(Allocation): 제한된 자원을 여러 수요처에 어떻게 나눌지 계산.
순수 파이썬 — vpython 불필요.

사용처: C 물 나눠 쓰기(농업/식수/공업 분배), E 에너지 배분.
"""


def proportional_allocate(total, demands):
    """수요 비율대로 total을 나눠준다. 반환: 각 수요처의 배분량 리스트."""
    s = sum(demands)
    if s <= 0:
        return [0.0 for _ in demands]
    return [total * d / s for d in demands]


def greedy_allocate(total, demands):
    """앞에서부터(우선순위 순) 수요를 최대한 채운다. 뒤쪽은 남는 만큼만."""
    alloc = []
    for d in demands:
        give = min(d, total)
        alloc.append(give)
        total -= give
    return alloc


def satisfaction(allocated, demand):
    """만족도(0~1): 필요량 대비 받은 양의 비율. 수요가 0이면 1."""
    if demand <= 0:
        return 1.0
    return min(1.0, allocated / demand)
