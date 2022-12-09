"""
Run as:
python main.py -n {YOUR_N} -beta {YOUR_BETA}
"""

import argparse
from time import time
from metropolis import run_metropolis


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n", help="number of queens")
    parser.add_argument("-beta", "--beta", help="initial beta")
    args = parser.parse_args()
    N = int(args.n) if args.n else 4
    beta = float(args.beta) if args.beta else 0.01
    max_moves = 1000000

    t = time()
    iters, queens, _ = run_metropolis(
        N,
        max_moves,
        beta,
        mode="solve",
        beta_strategy="annealing_quantized",
        strategy_params={"iterations_step": 1000, "annealing_factor": 2},
    )

    if iters == -1:
        print(f"No solution found in {max_moves} moves.")
    else:
        print(f"Solution found in {iters} moves, {time() - t:e} seconds.")
