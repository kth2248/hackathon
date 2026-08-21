# parts/gameai/fsm.py
"""
유한상태기계(FSM, Finite State Machine): 게임 NPC의 행동 상태(순찰/추격/도주 등)를
'조건이 맞으면 다음 상태로' 규칙으로 전환한다. 게임 AI의 가장 기본 패턴. 순수 파이썬.

사용 예:
    ai = FSM("patrol")
    ai.add("patrol", lambda c: c["dist"] < 3, "chase")   # 가까우면 추격
    ai.add("chase",  lambda c: c["dist"] > 6, "patrol")  # 멀어지면 순찰
    state = ai.update({"dist": d})
"""


class FSM:
    def __init__(self, initial, transitions=None):
        self.state = initial
        self.transitions = transitions or {}   # {state: [(cond_fn, next_state), ...]}

    def add(self, state, cond, next_state):
        """state에 있을 때 cond(ctx)가 참이면 next_state로 전환하는 규칙 추가."""
        self.transitions.setdefault(state, []).append((cond, next_state))
        return self

    def update(self, ctx=None):
        """현재 상태의 전환 규칙을 검사해 상태를 갱신하고 현재 상태를 반환."""
        for cond, next_state in self.transitions.get(self.state, []):
            if cond(ctx):
                self.state = next_state
                break
        return self.state
