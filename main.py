"""
Run as:
python main.py -n {YOUR_N}
"""

import argparse
import csv
from time import time
from metropolis import run_metropolis

DUMP = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n", help="number of queens")
    args = parser.parse_args()
    N = int(args.n) if args.n else 4
    max_moves = 100_000_000

    t = time()
    iters, queens, _ = run_metropolis(
        N,
        max_moves,
        beta_init=0.01,
        mode="solve",
        beta_strategy="annealing_quantized",
        strategy_params={"iterations_step": 5000, "annealing_factor": 2, "annealing_max": 15},
    )

    if iters == max_moves-1:
        print(f"No solution found in {max_moves} moves.")
    else:
        print(f"Solution found in {iters} moves, {time() - t:e} seconds.")
