import numpy as np
import math as m
from collections import defaultdict
from board import Board
import csv


def run_metropolis(
    N,
    max_moves,
    beta_init,
    mode="solve",
    beta_strategy="fixed",
    strategy_params=None,
    count_params=None,
    debug=True,
):
    if mode not in ["solve", "count"]:
        raise NotImplementedError("mode not implemented.")

    board = Board(N)
    board.init_board()

    beta = beta_init
    accepted_moves = 0
    conflict_dict = defaultdict(int)

    #  If the number of conflict is already 0, we're done.
    if mode=="solve" and board.nb_conflicts == 0:
        debug and board.print_board()
        return 0, board.queens, dict(conflict_dict)
    
    for j in range(max_moves):

        if j % 100_000 == 0:
            filename = f"data/solution_{N}_{board.nb_conflicts}.csv"
            with open(filename, 'w') as csv_file:
                wr = csv.writer(csv_file, delimiter=',', lineterminator='\n')
                for queen in board.queens:
                    wr.writerow(list(queen))
        # Update beta according to the strategy
        if beta_strategy == "fixed":
            pass
        elif beta_strategy == "annealing_quantized":
            if j % strategy_params["iterations_step"] == 0:
                beta *= strategy_params["annealing_factor"]
                beta = min(beta, strategy_params["annealing_max"])
        else:
            raise NotImplementedError("beta_strategy not implemented.")

        # Debugging information
        if debug and j % 500 == 0:
            print(
                f"Move {j} - beta: {beta} - nb_conflicts: {board.nb_conflicts} - accepted_moves: {accepted_moves}"
            )

        # Choose a random swap and compute the energy difference
        qn1 = np.random.randint(N)
        qn2 = np.random.randint(N)
        de, _, _ = board.var_move(qn1, qn2)

        # Metropolis algorithm: If de <= 0, accept the move.
        # Otherwise, accept the move with probability given by e^(-de * beta)
        # (so, bigger de => less likely to accept move).
        # If we accept the move, swap queens
        # and update the total system energy.
        p = np.random.random()
        if (de <= 0) or (
            p < m.exp(-de * beta) and (accepted_moves := accepted_moves + 1)
        ):
            board.move_queen(qn1, qn2)
            # If the number of conflict is 0, we're done.
            if mode == "solve" and board.nb_conflicts == 0:
                if debug and board.N <= 100:
                    board.print_board()
                break
        # If we're in count mode, we keep track of the number of conflicts
        # for each move.
        if mode == "count" and j >= count_params["convergence_moves"]:
            conflict_dict[board.nb_conflicts] += 1
    return j, board.queens, dict(conflict_dict)
