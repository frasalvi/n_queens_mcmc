import numpy as np
import math as m
from time import time


class Queen:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def attack(self, queen) -> bool:
        # same increasing diag
        if self.x + self.y == queen.x + queen.y:
            return True
        # same decreasing diag
        elif self.x - self.y == queen.x - queen.y:
            return True
        else:
            return False


class Board:
    def __init__(self, N):
        self.size = N
        self.queens = []
        self.nb_conflict = 0

    def count_conflicts(self):
        conflicts = 0
        for i in range(len(self.queens)):
            for j in range(i):
                if self.queens[i].attack(self.queens[j]):
                    conflicts += 1
        self.nb_conflict = conflicts

    def put_random_queens(self):
        P = np.random.permutation(self.size)
        for i in range(len(P)):
            self.queens.append(Queen(i, P[i]))
        self.count_conflicts()

    def print_board(self):
        T = np.zeros((self.size, self.size), dtype=int)
        for queen in self.queens:
            T[queen.x][queen.y] += 1
        print("╔═", end="")
        for _ in range(self.size - 1):
            print("╤═", end="")
        print("╗")

        for i in range(self.size):
            print(f"║{ ' ' if T[i][0] == 0 else 'x'}", end="")
            for j in range(1, self.size):
                print(f"│{ ' ' if T[i][j] == 0 else 'x'}", end="")
            print("║")
            if i != self.size - 1:
                print("╟─", end="")
                for _ in range(self.size - 1):
                    print("┼─", end="")
                print("╢")

        print("╚═", end="")
        for _ in range(self.size - 1):
            print("╧═", end="")
        print("╝")
        self.count_conflicts()
        print(f"Number of conflicts {self.nb_conflict}")

    def var_move(self, i, j):
        if i == j:
            return 0
        var = 0
        new_queen1 = Queen(self.queens[i].x, self.queens[j].y)
        new_queen2 = Queen(self.queens[j].x, self.queens[i].y)
        for k in range(self.size):
            if k == i or k == j:
                continue
            if self.queens[k].attack(self.queens[i]):
                var -= 1
            if self.queens[k].attack(self.queens[j]):
                var -= 1
            if self.queens[k].attack(new_queen1):
                var += 1
            if self.queens[k].attack(new_queen2):
                var += 1
        if self.queens[i].attack(self.queens[j]):
            var -= 1
        if new_queen1.attack(new_queen2):
            var += 1
        return var

    def move_queen(self, i, j):
        if i == j:
            return
        new_queen1 = Queen(self.queens[i].x, self.queens[j].y)
        new_queen2 = Queen(self.queens[j].x, self.queens[i].y)
        # update number of conflict
        self.nb_conflict += self.var_move(i, j)
        self.queens[i] = new_queen1
        self.queens[j] = new_queen2


def run(N, MAX_MOVES, b):

    beta = b

    board = Board(N)
    board.put_random_queens()
    if board.nb_conflict == 0:
        board.print_board()
        print(0)
        return True, board.queens

    for j in range(MAX_MOVES):

        if j % 1000 == 0:
            beta *= 2
            print(j, m.exp(-1 * beta), board.nb_conflict)

        qn1 = np.random.randint(N)
        qn2 = np.random.randint(N)
        de = board.var_move(qn1, qn2)

        # Metropolis algorithm. If de <= 0, accept the move.
        # Otherwise, accept the move with probability given by e^(-dE/kT)
        # (so, bigger de => less likely to accept move).
        # If we accept the move, swap queens
        # and update the total system energy.
        p = np.random.random()
        if (de <= 0) or (p < m.exp(-de * beta)):
            board.move_queen(qn1, qn2)
            # If the number of conflict is 0, we're done.
            if board.nb_conflict == 0:
                if board.size <= 100:
                    board.print_board()
                print(j)
                return True, board.queens
    return False, board.queens


N = 8
MAX_MOVES = 1000000
beta = 0.01

b = time()
L = set()
for _ in range(10):
    v, l_q = run(N, MAX_MOVES, beta)
print(time() - b)
