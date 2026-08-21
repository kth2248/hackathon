# parts/models/epidemic.py
"""
전염병 확산 모델(에이전트 기반 SIR): 각 사람을 S(취약)/I(감염)/R(회복) 상태로 두고,
접촉으로 감염이 퍼지는 과정을 한 스텝씩 갱신. 순수 파이썬 — vpython 불필요.

사용처: G 전염병 확산·방역.

개념(SIR):
  S(Susceptible)=아직 안 걸림, I(Infected)=감염 중, R(Recovered)=회복(면역).
  감염자와 접촉한 취약자는 확률적으로 감염되고, 감염자는 확률적으로 회복한다.
"""
import random as _random


def infect_step(states, neighbors_of, p_infect, p_recover, rng=None):
    """한 스텝 갱신한 새 상태 리스트를 반환.

    states        : ['S','I','R', ...] 각 개체의 현재 상태
    neighbors_of(i) -> [j, ...] : i번 개체와 '접촉 중'인 개체들의 인덱스
    p_infect      : 감염자와 접촉 시 감염될 확률(0~1)
    p_recover     : 감염자가 이번 스텝에 회복할 확률(0~1)
    """
    rng = rng or _random
    new = list(states)
    for i, s in enumerate(states):
        if s == "I":
            if rng.random() < p_recover:
                new[i] = "R"
        elif s == "S":
            for j in neighbors_of(i):
                if states[j] == "I" and rng.random() < p_infect:
                    new[i] = "I"
                    break
    return new


def counts(states):
    """(S, I, R) 개수 튜플. 감염 곡선 그래프에 그대로 쓴다."""
    return (states.count("S"), states.count("I"), states.count("R"))
