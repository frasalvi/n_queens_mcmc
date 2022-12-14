import numpy as np
from collections import defaultdict


def choose2(n):
    return (n * (n - 1)) // 2


class Queen:
    def __init__(self, x, y):
        self.x = x
        self.move(y)

    def move(self, y):
        self.y = y
        self.incresing_diag = self.x + self.y
        self.decreasing_diag = self.x - self.y

    def get_diagonals(self):
        return self.incresing_diag, self.decreasing_diag

    def __repr__(self):
        return f"Queen({self.x}, {self.y})"


class Board:
    def __init__(self, N):
        self.N = N
        self.queens = []
        self.nb_conflicts = 0

    def count_conflicts(self):
        conflicts = 0
        self.increasing_diag_counter = defaultdict(int)
        self.decreasing_diag_counter = defaultdict(int)
        for i in range(self.N):
            increasing_diag, decreasing_diag = self.queens[i].get_diagonals()
            self.increasing_diag_counter[increasing_diag] += 1
            self.decreasing_diag_counter[decreasing_diag] += 1

        # There are n_diag choose 2 conflicts over the diagonal
        for n_diag in self.increasing_diag_counter.values():
            conflicts += choose2(n_diag)
        for n_diag in self.decreasing_diag_counter.values():
            conflicts += choose2(n_diag)
        self.nb_conflicts = conflicts

    def init_board(self):
        P = np.random.permutation(self.N)
        for x, y in enumerate(P):
            self.queens.append(Queen(x, y))
        self.count_conflicts()

    def print_board(self):
        T = np.zeros((self.N, self.N), dtype=int)
        for queen in self.queens:
            T[queen.x][queen.y] += 1
        print("╔═", end="")
        for _ in range(self.N - 1):
            print("╤═", end="")
        print("╗")

        for i in range(self.N):
            print(f"║{ ' ' if T[i][0] == 0 else 'x'}", end="")
            for j in range(1, self.N):
                print(f"│{ ' ' if T[i][j] == 0 else 'x'}", end="")
            print("║")
            if i != self.N - 1:
                print("╟─", end="")
                for _ in range(self.N - 1):
                    print("┼─", end="")
                print("╢")

        print("╚═", end="")
        for _ in range(self.N - 1):
            print("╧═", end="")
        print("╝")
        self.count_conflicts()
        print(f"Number of conflicts {self.nb_conflicts}")

    def var_move(self, i, j):
        if i == j:
            return 0, self.increasing_diag_counter, self.decreasing_diag_counter
        new_queen1 = Queen(self.queens[i].x, self.queens[j].y)
        new_queen2 = Queen(self.queens[j].x, self.queens[i].y)

        var = 0
        tmp_increasing_counter, tmp_decreasing_counter = (
            self.increasing_diag_counter.copy(),
            self.decreasing_diag_counter.copy(),
        )
        conflicts = int(self.nb_conflicts)
        increasing_diags_to_update = set()
        decreasing_diags_to_update = set()

        # Remove old conflicts
        old_increasing_diag1, old_decreasing_diag1 = self.queens[i].get_diagonals()
        old_increasing_diag2, old_decreasing_diag2 = self.queens[j].get_diagonals()
        tmp_increasing_counter[old_increasing_diag1] -= 1
        tmp_decreasing_counter[old_decreasing_diag1] -= 1
        tmp_increasing_counter[old_increasing_diag2] -= 1
        tmp_decreasing_counter[old_decreasing_diag2] -= 1
        increasing_diags_to_update.add(old_increasing_diag1)
        increasing_diags_to_update.add(old_increasing_diag2)
        decreasing_diags_to_update.add(old_decreasing_diag1)
        decreasing_diags_to_update.add(old_decreasing_diag2)

        # Add new conflicts
        new_increasing_diag1, new_decreasing_diag1 = new_queen1.get_diagonals()
        new_increasing_diag2, new_decreasing_diag2 = new_queen2.get_diagonals()
        tmp_increasing_counter[new_increasing_diag1] += 1
        tmp_decreasing_counter[new_decreasing_diag1] += 1
        tmp_increasing_counter[new_increasing_diag2] += 1
        tmp_decreasing_counter[new_decreasing_diag2] += 1
        increasing_diags_to_update.add(new_increasing_diag1)
        increasing_diags_to_update.add(new_increasing_diag2)
        decreasing_diags_to_update.add(new_decreasing_diag1)
        decreasing_diags_to_update.add(new_decreasing_diag2)

        for diag in increasing_diags_to_update:
            conflicts -= choose2(self.increasing_diag_counter[diag]) - choose2(
                tmp_increasing_counter[diag]
            )

        for diag in decreasing_diags_to_update:
            conflicts -= choose2(self.decreasing_diag_counter[diag]) - choose2(
                tmp_decreasing_counter[diag]
            )

        var = conflicts - self.nb_conflicts
        return var, tmp_increasing_counter, tmp_decreasing_counter

    def move_queen(self, i, j):
        if i == j:
            return

        # update number of conflict
        var, tmp_increasing_counter, tmp_decreasing_counter = self.var_move(i, j)
        self.nb_conflicts += var
        self.increasing_diag_counter = tmp_increasing_counter
        self.decreasing_diag_counter = tmp_decreasing_counter

        # update board
        y1, y2 = self.queens[i].y, self.queens[j].y
        self.queens[i].move(y2)
        self.queens[j].move(y1)
