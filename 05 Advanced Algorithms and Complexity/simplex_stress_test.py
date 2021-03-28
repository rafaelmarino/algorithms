import random

import numpy as np
from scipy import optimize

import simplex_method


def solve(n, m, A, b, c):
    """Compute Linprog solution"""
    # print("Solving: ", n, m, A, b, c)
    return optimize.linprog(
        -np.array(c),  # a minimization by default, turn to Max by negating c
        A_ub=np.array(A),
        b_ub=np.array(b),
        bounds=[(0, None)] * m,
        options={'tol': 1e-3},
    )


def main():
    counter = 0 
    for _ in range(1000):
        n = random.randint(2, 2)
        m = random.randint(2, 2)
        A = []
        for __ in range(n):
            A.append([random.randint(-100, 100) for ___ in range(m)])

        b = [random.randint(-10, 10) for ___ in range(n)]
        c = [random.randint(-10, 10) for i in range(m)]

        counter += 1
        LP = (n, m, A, b, c,)
        print("LP", counter, ": ", LP, sep = "")

        result = solve(n, m, A, b, c)
        if result.status == 3:  # Unbounded -> "Infinity"
            result_t = 1
        elif result.status == 0:  # "Bounded Solution"
            result_t = 0
        else:
            result_t = -1  # "No solution"

        ans_t, ans_x = simplex_method.simplex(n, m, A, b, c)
        # same value if dif from -0.0, 0.0 if equal to -0.0
        # ans_x = [x if x != -0.0 else 0.0 for x in ans_x]

        # First check that the type of solution is the same
        assert result_t == ans_t
        # Then if solution is bounded check that numbers are equal
        if result_t == 0:
            for x, y in zip(ans_x, result.x):
                assert abs(x - y) <= 1.0e-3

        print("LP passed")

if __name__ == '__main__':
    main()
