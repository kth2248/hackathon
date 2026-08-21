# parts/pathfinding/astar.py
"""
A* 최단경로 탐색 (게임 AI의 표준 길찾기 알고리즘).
순수 파이썬 — vpython 불필요, 오프라인/테스트 가능.

사용처: A 대피 시뮬레이터, D 로봇 함대 (에이전트가 목표까지 스스로 최단경로 탐색).

핵심 개념: 각 칸까지의 '실제 비용(g)' + '목표까지 예상 비용(h, 휴리스틱)'의 합이
가장 작은 칸부터 탐색해, 최단경로를 효율적으로 찾는다.
"""
import heapq


def astar(start, goal, passable, diagonal=False):
    """start에서 goal까지의 최단경로를 칸 리스트로 반환. 못 찾으면 [].

    start, goal : (x, y) 정수 튜플 (격자 좌표)
    passable(cell)->bool : 그 칸을 지나갈 수 있는지 (경계 밖/장애물이면 False)
    diagonal : True면 대각선 이동 허용(8방향), False면 상하좌우(4방향)

    반환: [start, ..., goal] 형태의 경로. start==goal이면 [start].
    """
    if not passable(start) or not passable(goal):
        return []

    if diagonal:
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1),
                 (1, 1), (1, -1), (-1, 1), (-1, -1)]

        def h(a, b):
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))     # 체비셰프
    else:
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        def h(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])         # 맨해튼

    open_heap = [(h(start, goal), 0.0, start)]
    came_from = {start: None}
    gscore = {start: 0.0}

    while open_heap:
        _, g, current = heapq.heappop(open_heap)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        if g > gscore.get(current, float("inf")):
            continue   # 이미 더 좋은 경로로 방문한 칸

        for dx, dy in steps:
            nxt = (current[0] + dx, current[1] + dy)
            if not passable(nxt):
                continue
            step_cost = 1.4 if (dx != 0 and dy != 0) else 1.0
            ng = g + step_cost
            if ng < gscore.get(nxt, float("inf")):
                gscore[nxt] = ng
                came_from[nxt] = current
                heapq.heappush(open_heap, (ng + h(nxt, goal), ng, nxt))

    return []   # 경로 없음


def path_length(path):
    """경로의 칸 개수(이동 스텝 수 = len-1)를 세는 보조 함수."""
    return max(0, len(path) - 1)
