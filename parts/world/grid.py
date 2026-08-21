# parts/world/grid.py
"""
격자 세계(GridWorld): 맵 크기, 장애물, 격자<->실좌표 변환.
순수 파이썬 — vpython 불필요.

사용처: A 대피(도시 격자), D 로봇 함대(바다 격자). astar.py와 짝으로 쓴다.
- 격자 좌표 (col, row): A* 경로탐색에 사용 (정수)
- 실좌표 (x, y): VPython 3D 배치에 사용 (실수)
"""


class GridWorld:
    def __init__(self, cols, rows, cell_size=1.0, origin=(0.0, 0.0)):
        """cols x rows 격자. cell_size=한 칸의 실제 크기, origin=격자 중심의 실좌표."""
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.ox, self.oy = origin
        self.obstacles = set()

    def in_bounds(self, cell):
        x, y = cell
        return 0 <= x < self.cols and 0 <= y < self.rows

    def block(self, cell):
        """장애물(못 지나가는 칸) 추가."""
        self.obstacles.add(tuple(cell))

    def unblock(self, cell):
        self.obstacles.discard(tuple(cell))

    def passable(self, cell):
        """astar에 넘길 함수: 경계 안이고 장애물이 아니면 True."""
        return self.in_bounds(cell) and tuple(cell) not in self.obstacles

    def cell_to_world(self, cell):
        """격자 좌표 -> 실좌표 (VPython 배치용). 격자 중심이 origin이 되도록 정렬."""
        x, y = cell
        wx = self.ox + (x - self.cols / 2 + 0.5) * self.cell_size
        wy = self.oy + (y - self.rows / 2 + 0.5) * self.cell_size
        return (wx, wy)

    def world_to_cell(self, wx, wy):
        """실좌표 -> 가장 가까운 격자 좌표."""
        cx = int(round((wx - self.ox) / self.cell_size + self.cols / 2 - 0.5))
        cy = int(round((wy - self.oy) / self.cell_size + self.rows / 2 - 0.5))
        return (cx, cy)
