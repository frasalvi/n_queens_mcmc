"""
Run as:
python count_solutions.py -n {YOUR_N}
"""

import os
import pickle
import numpy as np
import mpmath as mp
import argparse
from metropolis import run_metropolis

mp.mp.dps = 300


def get_ratios(N, convergence_moves, counting_moves, beta_grid, debug=True, iter=None):
    max_moves = convergence_moves + counting_moves
    ratio_arr = []

    for i in range(len(beta_grid) - 2, -1, -1):
        beta_t1 = beta_grid[i + 1]
        beta_t = beta_grid[i]

        path = f"data/{N}_beta{beta_t}"
        if iter:
            path += f"_{iter}"
        path += ".pkl"

        if os.path.exists(path):
            with open(path, "rb") as f:
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
                debug=debug,
            )
            with open(path, "wb") as f:
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
        ratio_arr.append(mp.mpmathify(ratio))

        with mp.workdps(4):
            debug and print(f"beta {beta_t}, ratio {ratio}")

    return ratio_arr


def estimate_zetab(
    N, convergence_moves, counting_moves, beta_grid, debug=True, iter=None
):
    ratio_arr = get_ratios(N, convergence_moves, counting_moves, beta_grid, debug, iter)
    T = len(ratio_arr)
    Z_arr = np.empty(T + 1, dtype=object)
    Z_arr[0] = mp.factorial(N)
    for i in range(1, T + 1):
        Z_arr[i] = Z_arr[i - 1] * ratio_arr[T - i]
    return Z_arr


def count_solutions(
    N, convergence_moves, counting_moves, beta_grid, debug=True, iter=None
):
    Z_arr = estimate_zetab(N, convergence_moves, counting_moves, beta_grid, debug, iter)
    Z = Z_arr[-1]
    return Z


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n", help="number of queens")
    args = parser.parse_args()
    N = int(args.n) if args.n else 1000
    convergence_moves = 200_000
    counting_moves = 800_000

    if N <= 20:
        beta_grid = [0, 0.01, 1, 3, 5, 10]
    else:
        beta_grid = [
            0,
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
