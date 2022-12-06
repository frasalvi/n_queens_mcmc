from metropolis import run_metropolis
from time import time


if __name__ == "__main__":
    N = 8
    MAX_MOVES = 1000000
    beta = 0.01

    b = time()
    L = set()
    for _ in range(10):
        v, l_q = run_metropolis(N, MAX_MOVES, beta)
    print(time() - b)