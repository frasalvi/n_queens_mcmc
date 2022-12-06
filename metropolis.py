import numpy as np
import math as m
from board import Board


def run_metropolis(N, MAX_MOVES, b):

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
