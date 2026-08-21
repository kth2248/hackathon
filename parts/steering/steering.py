# parts/steering/steering.py
"""
조향(Steering) & 군집(Flocking): 에이전트가 목표로 가고, 무리 짓고, 서로 안 부딪히게 하는
'게임 AI'의 핵심 행동 부품. VPython의 vector를 사용한다.

사용처: A 대피(군중 흐름), D 로봇 함대(군집 협력), G 전염병(사람 이동).

각 함수는 '어느 방향으로 밀지'를 나타내는 단위 벡터(또는 힘)를 돌려준다.
여러 개를 가중치로 더해 최종 이동 방향을 만든다 (hackathon_kit의 blend/clamp와 함께 쓰면 좋다).
"""
from vpython import vector


def seek(pos, target, max_speed=1.0):
    """목표를 향하는 속도 벡터."""
    d = target - pos
    if d.mag == 0:
        return vector(0, 0, 0)
    return d.norm() * max_speed


def arrive(pos, target, max_speed=1.0, slow_radius=2.0):
    """목표에 가까워지면 속도를 줄이며 '부드럽게 도착'하는 속도 벡터."""
    d = target - pos
    dist = d.mag
    if dist == 0:
        return vector(0, 0, 0)
    speed = max_speed * min(1.0, dist / slow_radius) if slow_radius > 0 else max_speed
    return d.norm() * speed


def separation(pos, neighbor_positions, radius=1.5):
    """너무 가까운 이웃들에게서 멀어지는 방향(충돌 회피)."""
    steer = vector(0, 0, 0)
    count = 0
    for n in neighbor_positions:
        diff = pos - n
        dd = diff.mag
        if 0 < dd < radius:
            steer = steer + diff.norm() / dd     # 가까울수록 강하게
            count += 1
    if count > 0:
        steer = steer / count
    return steer.norm() if steer.mag > 0 else vector(0, 0, 0)


def alignment(neighbor_velocities):
    """이웃들의 평균 진행 방향(무리와 방향 맞추기)."""
    if not neighbor_velocities:
        return vector(0, 0, 0)
    avg = vector(0, 0, 0)
    for v in neighbor_velocities:
        avg = avg + v
    avg = avg / len(neighbor_velocities)
    return avg.norm() if avg.mag > 0 else vector(0, 0, 0)


def cohesion(pos, neighbor_positions):
    """이웃들의 중심으로 향하는 방향(무리 뭉치기)."""
    if not neighbor_positions:
        return vector(0, 0, 0)
    center = vector(0, 0, 0)
    for p in neighbor_positions:
        center = center + p
    center = center / len(neighbor_positions)
    d = center - pos
    return d.norm() if d.mag > 0 else vector(0, 0, 0)


def flock(pos, neighbor_positions, neighbor_velocities, sep_radius=1.5, weights=(1.5, 1.0, 1.0)):
    """분리+정렬+응집을 가중치로 합친 군집 방향(단위 벡터).
    weights=(분리, 정렬, 응집). 분리를 크게 하면 덜 뭉치고, 응집을 크게 하면 더 뭉친다.
    """
    ws, wa, wc = weights
    total = (separation(pos, neighbor_positions, sep_radius) * ws
             + alignment(neighbor_velocities) * wa
             + cohesion(pos, neighbor_positions) * wc)
    return total.norm() if total.mag > 0 else vector(0, 0, 0)


def flee(pos, threat, max_speed=1.0):
    """위협(threat)에서 멀어지는 속도 벡터 — 게임 AI '도주' 행동."""
    d = pos - threat
    if d.mag == 0:
        return vector(0, 0, 0)
    return d.norm() * max_speed


def pursue(pos, target_pos, target_vel, max_speed=1.0, lead=1.0):
    """목표의 미래 위치를 예측해 앞질러 쫓는 속도 벡터 — 게임 AI '추격' 행동."""
    future = target_pos + target_vel * lead
    d = future - pos
    return d.norm() * max_speed if d.mag > 0 else vector(0, 0, 0)
