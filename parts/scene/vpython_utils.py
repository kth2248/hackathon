# vpython_utils.py
"""
VPython 3D 객체를 생성하는 공통 헬퍼.
'무엇을 위해 쓰는 구슬인지'는 여기서 정하지 않는다 (A/B/C안 조립 단계에서 결정).
"""
from vpython import sphere, box, vector, color, canvas


def make_scene(title: str = "3D 시뮬레이터", width: int = 800, height: int = 500):
    """공통 캔버스 생성. 매번 반복되는 canvas() 호출을 줄임.
    width/height는 필요 시 조정 가능(기본 800x500)."""
    return canvas(title=title, width=width, height=height)


def make_agent(pos=vector(0, 0, 0), radius=0.3, agent_color=color.blue, trail=True, trail_radius=None):
    """이동 주체(에이전트) 구 생성. make_trail로 경로 시각화 지원.
    trail_radius를 주면 경로 선의 굵기를 지정(가늘고 선명한 궤적용)."""
    kwargs = dict(pos=pos, radius=radius, color=agent_color, make_trail=trail)
    if trail_radius is not None:
        kwargs["trail_radius"] = trail_radius
    return sphere(**kwargs)


def make_obstacle(pos=vector(0, 0, 0), radius=0.5, obstacle_color=color.red):
    """장애물 구 생성. A안에서는 '사람' 역할, C안에서는 '다른 개체' 역할로 재사용."""
    return sphere(pos=pos, radius=radius, color=obstacle_color)


def make_floor(length=10, width=10, floor_color=color.green, pos=None, height=0.2):
    """바닥 생성. 공간 기준점 제공용 (선택 사용).
    pos/height로 위치와 두께 조정 가능(기본 y=-2)."""
    if pos is None:
        pos = vector(0, -2, 0)
    return box(pos=pos, length=length, height=height, width=width, color=floor_color)


def make_multiple_agents(count: int, spacing: float = 2.0, agent_color=color.blue):
    """N개의 에이전트를 일렬로 배치. C안(군집)에서 바로 사용 가능.
    주의: C안 대비용이므로 A안만 확정되면 우선순위 낮음 — 시간 없으면 생략 가능.
    """
    agents = []
    for i in range(count):
        pos = vector(-spacing * count / 2 + i * spacing, 0, 0)
        agents.append(make_agent(pos=pos, agent_color=agent_color))
    return agents
