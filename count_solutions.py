import os
import pickle
import math
import numpy as np
from metropolis import run_metropolis


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
                    count * math.exp(-delta_beta * conflict)
                    for conflict, count in conflict_dict.items()
                ]
            )
            / counting_moves
        )
        ratio_sum += math.log(ratio)

        print(f"beta {beta_t}, ratio {ratio}")

    Z0 = math.factorial(N)
    Z = Z0 * math.exp(ratio_sum)
    return Z


if __name__ == "__main__":
    np.random.seed(42)
    N = 20
    convergence_moves = 200000
    counting_moves = 800000
    # beta_grid = [0.00001, 0.0001, 0.01, 0.05, 0.1, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20]
    beta_grid = [0.0001, 0.01, 0.1, 0.5, 1, 3, 5, 10, 20]

    Z = count_solutions(N, convergence_moves, counting_moves, beta_grid)
    print(f"Z = {Z:e}")
