# parts/generation/patterns.py
"""
절차적 배치 패턴(Procedural Placement): N개 객체를 줄/나선/원으로 놓을 좌표를 생성.
순수 파이썬 — vpython 불필요, 테스트 가능. (B_nl3d의 make_position을 부품화)

사용처: F 말로 짓는 도시, B 탄소 숲 등 '여러 개를 규칙적으로 배치'하는 모든 곳.
반환: (x, y, z) 튜플 리스트. vpython에서는 vector(*p)로 바로 쓸 수 있다.
"""
import math


def line_positions(n, spacing=1.2, z=0.0):
    """가로 일렬 배치 (중앙 정렬)."""
    return [(i * spacing - n * spacing / 2, 0.0, z) for i in range(n)]


def spiral_positions(n, growth=0.4, angle_step=1.2, z_step=0.3):
    """나선 배치 (밖으로·위로 퍼짐)."""
    out = []
    for i in range(n):
        a = i * angle_step
        r = 1 + i * growth
        out.append((math.cos(a) * r, math.sin(a) * r, i * z_step))
    return out


def circle_positions(n, radius=None):
    """원형 배치 (일정 반지름에 균등 분포)."""
    if n <= 0:
        return []
    r = radius if radius is not None else 1 + n * 0.15
    return [(math.cos(2 * math.pi * i / n) * r,
             math.sin(2 * math.pi * i / n) * r, 0.0) for i in range(n)]


def grid_positions(n, cols=None, spacing=1.2):
    """격자(그리드) 배치. cols를 안 주면 정사각형에 가깝게 자동 계산."""
    if n <= 0:
        return []
    if cols is None:
        cols = max(1, int(math.ceil(math.sqrt(n))))
    out = []
    for i in range(n):
        c, r = i % cols, i // cols
        out.append((c * spacing - (cols - 1) * spacing / 2,
                    r * spacing, 0.0))
    return out
