import numpy as np
import math as m
from board import Board

def simplest(
    b="fixed", a=True
):
    return -1, -2, -3, -4


def run_metropolis_w_sampling(
    N, max_moves, beta_init, sample_size, beta_strategy="fixed", strategy_params=None, debug=True
):
    board = Board(N)
    board.init_board()
    conflict_ratios = []
    seen_zeros = 0
    sampling = "off"
    samples = []
    delta = 100000
    prev_ratio = 0

    beta = beta_init
    for j in range(1, max_moves):

        # Update beta according to the strategy
        if beta_strategy == "fixed":
            pass
        elif beta_strategy == "annealing_quantized":
            if j % strategy_params["iterations_step"] == 0:
                beta *= strategy_params["annealing_factor"]
        else:
            raise NotImplementedError("beta_strategy not implemented.")

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
                seen_zeros += 1
            
            

        ## add ratio of zero conflict to non-zero conflict to understand convergence
        if seen_zeros != 0:
            curr_confs = board.nb_conflicts
            curr_ratio = (seen_zeros / j)
            conflict_ratios.append(curr_ratio)
            delta = curr_ratio - prev_ratio
            prev_ratio = curr_ratio
            
        if delta <= 1.0050502518947624e-07 or j > 10000:
            sampling = "on"
            
            
        ## once converged, sample M outcomes from the pi_beta distribution and return the outcomes    
        if sampling == "on":
            if len(samples) < sample_size:
                samples.append(board.nb_conflicts)
            else: 
                return j, conflict_ratios, samples
            
        
            
            
    return j, conflict_ratios, samples
