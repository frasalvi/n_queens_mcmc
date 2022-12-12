import os
import pickle
import numpy as np
import mpmath as mp
from metropolis import run_metropolis

mp.mp.dps = 300


def count_solutions(N, convergence_moves, counting_moves, beta_grid):
    max_moves = convergence_moves + counting_moves
    ratio_sum = 0

    for i in range(len(beta_grid) - 2, -1, -1):
        beta_t1 = beta_grid[i + 1]
        beta_t = beta_grid[i]

        if os.path.exists(f"data/{N}_beta{beta_t}.pkl"):
            with open(f"data/{N}_beta{beta_t}.pkl", "rb") as f:
                conflict_dict = pickle.load(f)
        else:
            _, _, conflict_dict = run_metropolis(
                N,
                max_moves,
                beta_t,
                mode="count",
                beta_strategy="fixed",
                strategy_params=None,
                count_params={"convergence_moves": convergence_moves},
            )
            with open(f"data/{N}_beta{beta_t}.pkl", "wb") as f:
                pickle.dump(conflict_dict, f)

        delta_beta = beta_t1 - beta_t
        ratio = (
            sum(
                [
                    count * mp.exp(-delta_beta * conflict)
                    for conflict, count in conflict_dict.items()
                ]
            )
            / counting_moves
        )
        ratio_sum += mp.log(ratio)

        with mp.workdps(4):
            print(f"beta {beta_t}, ratio {ratio}")

    with mp.workdps(4):
        print(f"ratio_sum = {ratio_sum}")
    Z0 = mp.factorial(N)
    Z = Z0 * mp.exp(ratio_sum)
    return Z


if __name__ == "__main__":
    np.random.seed(42)
    N = 1000
    convergence_moves = 200_000
    counting_moves = 800_000
    beta_grid = [
        0.0001,
        0.01,
        0.1,
        0.25,
        0.375,
        0.5,
        0.625,
        0.75,
        1,
        1.25,
        1.5,
        1.75,
        2,
        2.5,
        3,
        4,
        5,
        10,
        20,
    ]

    Z = count_solutions(N, convergence_moves, counting_moves, beta_grid)

    with mp.workdps(4):
        print(f"Z = {Z}")
