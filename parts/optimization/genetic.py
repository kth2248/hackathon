# parts/optimization/genetic.py
"""
유전 알고리즘(Genetic Algorithm): 사람이 직접 못 푸는 조합 문제의 좋은 해를
'세대를 거치며 진화'시켜 자동으로 탐색. 순수 파이썬 — vpython 불필요.

사용처: B 탄소 숲(나무 최적 배치), E 재생에너지(발전소 최적 입지).

개념: 후보 해(individual) 여러 개(population)를 만들고, 점수(fitness) 높은 것들을
살아남게 해 교배(crossover)·돌연변이(mutate)로 다음 세대를 만든다. 반복하면 좋은 해로 수렴.
"""
import random as _random


def genetic_optimize(create_individual, fitness, mutate,
                     crossover=None, pop_size=30, generations=40, elite=2, rng=None):
    """최적 해(individual)와 그 점수를 (best, best_fitness)로 반환.

    create_individual() -> individual        : 무작위 후보 해 생성
    fitness(individual) -> float             : 클수록 좋은 점수
    mutate(individual) -> individual         : 살짝 변형된 해
    crossover(a, b) -> individual (선택)      : 두 부모를 섞은 자식 (없으면 한 부모 복제)
    pop_size, generations, elite             : 개체수 / 세대수 / 매 세대 그대로 살릴 상위 개체수
    """
    rng = rng or _random
    pop = [create_individual() for _ in range(pop_size)]
    best, best_fit = None, float("-inf")

    for _ in range(generations):
        scored = sorted(((fitness(ind), ind) for ind in pop),
                        key=lambda t: t[0], reverse=True)
        if scored[0][0] > best_fit:
            best_fit, best = scored[0][0], scored[0][1]

        survivors = [ind for _, ind in scored[:max(elite, pop_size // 2)]]
        new_pop = [ind for _, ind in scored[:elite]]          # 엘리트 보존

        while len(new_pop) < pop_size:
            if crossover is not None:
                child = crossover(rng.choice(survivors), rng.choice(survivors))
            else:
                child = rng.choice(survivors)
            new_pop.append(mutate(child))
        pop = new_pop

    return best, best_fit
