# parts/stats/stats.py
"""
데이터 분석 부품: 상관계수(피어슨)와 정규화. 순수 파이썬 — vpython 불필요, 테스트 가능.
사용처: 실제 데이터의 '추세 비교'(예: CO2 vs 기온) — 주최측 예시형 데이터 분석.
"""


def pearson(xs, ys):
    """두 데이터의 피어슨 상관계수(-1~1). 1=완전한 양의 상관, 0=무상관, -1=음의 상관."""
    n = len(xs)
    if n == 0:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs) ** 0.5
    dy = sum((y - my) ** 2 for y in ys) ** 0.5
    return num / (dx * dy) if dx * dy else 0.0


def minmax_scale(xs, lo=0.0, hi=100.0):
    """값들을 lo~hi 범위로 정규화. 단위가 다른 두 지표를 겹쳐 비교할 때 사용."""
    mn, mx = min(xs), max(xs)
    if mx == mn:
        return [lo for _ in xs]
    return [lo + (x - mn) / (mx - mn) * (hi - lo) for x in xs]
