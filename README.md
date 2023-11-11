# Solving the N-queens problems via the Metropolis algorithm


The N-queens problem demands a way to place $N$ queens on an $N$ × $N$ chessboard so that no two queens attack each other (lie on the same row, column, or diagonal).
In this project, we implement a Metropolis–Hastings algorithm for sampling a solution to the problem, for any board size. Moreover, we use this algorithm to estimate the number of solutions, by sequentially approximating the partition function. Our method finds a solution for $N \leq 1000$ in less than $20 s$ and approximates correctly the number of solutions for all the exact values up to $N = 26$. For large $N$, instead, our estimates scale as $N!/e^N$, coherently with previous literature.


Read more about the project in our [report](documents/Report.pdf).


This work is part of the course "Markov Chains and Algorithmic Applications" at EPFL, and is the joint effort of [Francesco Salvi](https://github.com/frasalvi), [Neta Singer](https://github.com/netabobeta) and [Perrine Vantalon](https://github.com/vantalon).
