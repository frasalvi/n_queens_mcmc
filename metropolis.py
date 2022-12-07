import numpy as np
import math as m
from board import Board


def run_metropolis(
    N, max_moves, beta_init, beta_strategy="fixed", strategy_params=None
):
    board = Board(N)
    board.init_board()

    #  If the number of conflict is already 0, we're done.
    if board.nb_conflicts == 0:
        board.print_board()
        return 0, board.queens

    beta = beta_init
    for j in range(max_moves):

        # Update beta according to the strategy
        if beta_strategy == "fixed":
            pass
        elif beta_strategy == "annealing_quantized":
            if j % strategy_params["iterations_step"] == 0:
                beta *= strategy_params["annealing_factor"]
        else:
            raise NotImplementedError("beta_strategy not implemented.")

        # Debugging information
        if j % 500 == 0:
            print(f"Move {j} - beta: {beta} - nb_conflicts: {board.nb_conflicts}")

        # Choose a random swap and compute the energy difference
        qn1 = np.random.randint(N)
        qn2 = qn1
        while qn2 == qn1:
            qn2 = np.random.randint(N)
        de, _, _ = board.var_move(qn1, qn2)

        # Metropolis algorithm: If de <= 0, accept the move.
        # Otherwise, accept the move with probability given by e^(-de * beta)
        # (so, bigger de => less likely to accept move).
        # If we accept the move, swap queens
        # and update the total system energy.
        p = np.random.random()
        if (de <= 0) or (p < m.exp(-de * beta)):
            board.move_queen(qn1, qn2)
            # If the number of conflict is 0, we're done.
            if board.nb_conflicts == 0:
                if board.N <= 100:
                    board.print_board()
                return j, board.queens
    return -1, board.queens
