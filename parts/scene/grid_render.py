# parts/scene/grid_render.py
"""
격자(GridWorld)를 3D 화면에 그리는 헬퍼. VPython 필요.
parts/world/grid.py의 GridWorld와 짝으로 쓴다 — 격자는 바닥(x-z 평면)에 깔고 y는 높이로 본다.

사용처: 공용 뼈대 및 A 대피·D 로봇·인프라 등 '격자 위 시뮬' 전부.
"""
from vpython import box, vector, color


def cell_pos(world, cell, y=0.0):
    """격자 칸 (col, row) -> VPython 3D 위치 벡터. 바닥은 x-z 평면, y는 높이."""
    wx, wy = world.cell_to_world(cell)
    return vector(wx, y, wy)


def render_floor(world, floor_color=None, y=-0.25, thickness=0.4):
    """격자 전체를 덮는 바닥판 하나 생성."""
    w = world.cols * world.cell_size
    d = world.rows * world.cell_size
    return box(pos=vector(world.ox, y - thickness / 2, world.oy),
               size=vector(w, thickness, d),
               color=floor_color if floor_color is not None else color.gray(0.3))


def render_obstacles(world, tile=0.9, height=0.6, obstacle_color=None, y=0.0):
    """장애물 칸들을 3D 박스로 그린다. 생성된 box 리스트 반환."""
    c = obstacle_color if obstacle_color is not None else color.red
    size = vector(world.cell_size * tile, height, world.cell_size * tile)
    boxes = []
    for cell in world.obstacles:
        boxes.append(box(pos=cell_pos(world, cell, y=y + height / 2), size=size, color=c))
    return boxes
