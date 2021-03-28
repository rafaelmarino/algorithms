# python3
from sys import stdin
# import numpy as np


def pivot(N, B, A, b, c, v, l, e):
    """Compute pivot by changing X_l to N and X_e to B"""
    # Test Case:
    # N, B, A = [0,1,2], [3,4,5], [[1.0,1.0,3.0], [2.0,2.0,5.0], [4.0,1.0,2.0]]
    # b, c, v, l, e = [30.0, 24.0, 36.0], [3.0,1.0,2.0], 0.0, 5, 0
    # 1. Compute the coefficients of the equation for new basic variable X_e
    m, n = len(A), len(A[0])
    # the leaving variable is always in B; the entering variable is always in N
    Xl_oldrow_id = B.index(l)  # row pos in old B for x_leaving
    Xe_oldcol_id = N.index(e)  # col pos in old N for x_entering
    factor = A[Xl_oldrow_id][Xe_oldcol_id]
    # new iteration sets
    N_wo_e = list(N)
    N_wo_e.remove(e)
    B_wo_l = list(B)
    B_wo_l.remove(l)
    # Determining order of elements in new B
    new_B = list(B)
    new_B.append(e)
    new_B.remove(l)
    new_B.sort()
    Xe_newrowid = new_B.index(e)  # row where eq started by X_e will be stored
    # Determining order of elements in new N
    new_N = list(N)
    new_N.remove(e)
    new_N.append(l)
    new_N.sort()
    Xl_newcolid = new_N.index(l)  # col where variable X_l will be saved
    # dividing independent term associated with leaving row by factor
    new_b = [0] * m
    new_b[Xe_newrowid] = b[Xl_oldrow_id] / factor
    # create rows with n columns m times (rows)
    new_A = [[float(0) for _ in range(n)] for _ in range(m)]
    for nonbasic in N_wo_e:
        # find col pos of nonbasic in new_N
        new_colid = new_N.index(nonbasic)
        old_colid = N.index(nonbasic)
        old_coeff = A[Xl_oldrow_id][old_colid]
        new_A[Xe_newrowid][new_colid] = old_coeff / factor
    new_A[Xe_newrowid][Xl_newcolid] = 1 / factor
    # 2. Compute the coefficients of the remaining constraints
    for basic in B_wo_l:
        # for each remaining constraint except the one with Xl
        new_rowid = new_B.index(basic)  # equation finder
        old_rowid = B.index(basic)
        Xe_const_coeff = A[old_rowid][Xe_oldcol_id]  # Xe coeff in each eq
        new_b[new_rowid] = b[old_rowid] - Xe_const_coeff * new_b[Xe_newrowid]
        for nonbasic in N_wo_e:
            # for each remaining variable except Xe
            old_colid = N.index(nonbasic)
            old_value = A[old_rowid][old_colid]
            new_colid = new_N.index(nonbasic)
            nonbasic_coeff = new_A[Xe_newrowid][new_colid]
            new_A[new_rowid][new_colid] = old_value - Xe_const_coeff * nonbasic_coeff
        new_A[new_rowid][Xl_newcolid] = -Xe_const_coeff*new_A[Xe_newrowid][Xl_newcolid]
    # 3. Compute the objective function
    new_v = v + c[Xe_oldcol_id]*new_b[Xe_newrowid]
    new_c = [0] * n
    Xe_OF_coeff = c[Xe_oldcol_id]
    for nonbasic in N_wo_e:
        old_colid = N.index(nonbasic)
        new_colid = new_N.index(nonbasic)
        new_c[new_colid] = c[old_colid] - Xe_OF_coeff * new_A[Xe_newrowid][new_colid]
    new_c[Xl_newcolid] = -Xe_OF_coeff * new_A[Xe_newrowid][Xl_newcolid]
    # 4. Compute new B and new N
    # already done before to calculate order of rows and cols
    return (new_N, new_B, new_A, new_b, new_c, new_v)


def internal_loop(N, B, A, b, c, v):
    """Compute internal simplex loop. Return optimal slack form."""
    m, n = len(A), len(A[0])

    def positive_coeff():
        for i in range(len(c)):  # N should be zero based index
            if c[i] > 0.1e-3:
                return True
        return False
    delta = [float(0)] * m  # CLRS says n. Rafa: should be m, one per restriction 
    inf = float("inf")  # generic infinity definition
    while positive_coeff():
        # choosing the variable with the max coeff. Positive coeff guaranteed
        # IMPORTANT: Bland's rule is already implemented by default
        # Python chooses leftmost index. Which means smallest variable. N,B ordered
        max_coeff = max(c)
        nonbasic_id = c.index(max_coeff)
        entering_key = N[nonbasic_id]  # ALERT: used only later to call pivot
        for basic in range(len(B)):
            # for each restriction
            leaving_coeff = A[basic][nonbasic_id]
            if leaving_coeff > 0.0:
                delta[basic] = b[basic]/leaving_coeff
            else:
                delta[basic] = inf
        tightest_increase = min(delta)
        constraint_id = delta.index(tightest_increase)  # constraint_id = basic_id
        leaving_key = B[constraint_id]
        if tightest_increase == inf:
            # print("problem is here")
            # two results are needed to be assigned to 'anst', 'answ '
            # if the tightest constraint can be increased inf. LP is unbounded
            return [1, None, None, None, None, None, None]
        else:
            N, B, A, b, c, v = pivot(N, B, A, b, c, v, leaving_key, entering_key)
    return 0, N, B, A, b, c, v


def initialize_simplex(A, b, c):
    """Determine whether LP has feasible solution. If so return feasible slack form """
    original_c = list(c)  # will be used later to turn basics in final LP_aux to nonbasics
    m, n = len(A), len(A[0])  # rows x columns
    k = b.index(min(b))  # index of the smallest b_i
    # is the initial basic solution feasible?
    if b[k] >= 0:  
        N = list(range(1, n+1))  # each original variable constitutes a non-basic variable
        B = list(range(n+1, n+m+1))  # one basic variable per constraint
        return [0, N, B, A, b, c, 0.0]
    # If not feasible: 
    # resulting slack form for L_aux
    N = list(range(n+1))  # final number isn't included
    B = list(range(n+1, n+m+1))  # initial number IS included
    # add -X_0 to each constraint
    for row in range(m):
        A[row].insert(0, -1.0)
    # b doesn't change
    c = [float(0)] * n
    c.insert(0, -1)  # insert creates one position, for a total 1+n vars in OF
    # b doesn't change
    v = 0.0
    l = n + 1 + k  # +1 to account for the new variable, X_0
    # L_aux has n+1 NB variables and m basic variables
    # remember l, e must be integers. They are variable indices
    N, B, A, b, c, v = pivot(N, B, A, b, c, v, l, 0)
    # the basic solution is now feasible for L_aux
    # ITERATE lines 3-12 of Simplex()
    solution_type, N, B, A, b, c, v = internal_loop(N, B, A, b, c, v)
    if solution_type == 1:
        return 1, None, None, None, None, None, None
    # ITERATION has ended
    if 0 in B:
        # X_0 may be 0 but still in B, we'll check and get it out later
        X_0 = b[0]
    else:
        # if it's in N, basic solution will set it to 0
        X_0 = 0

    def choose_e():
        # this method will only be called if X_0 = 0 and X_0 is still basic
        for colid, key in enumerate(N):
            coeff = A[0][colid]
            if coeff != 0:
                return key
    # if X_0 == 0:  # feasible
    # Exercise passed using < 0.1e-10
    if abs(X_0) < 0.1e-3:
        # tolerance needed to be added to pass test case 92/196
        if 0 in B:  # only point of this if is to get X_0 out of the basics
            # perform one (degenerate) PIVOT() to make it nonbasic
            entering_var = choose_e()
            N, B, A, b, c, v = pivot(N, B, A, b, c, v, 0, entering_var)
        # from L_aux, remove X_0, restore original OF, replacing each basic
        # by the RHS of its associated constraint
        # original nonbasics will always be indexed 1,2,...,n
        N.remove(0)
        for row in range(m):
            A[row] = A[row][1:]
        for var_index, coeff in enumerate(original_c):
            # update OF for all originals ending up as basics
            if var_index + 1 in B:
                # update v
                row_index = B.index(var_index+1)  # row index
                v = v + coeff * b[row_index]
        # variables in original OF will always be indexed from 1 to n
        originalOFvariables = list(range(1, n+1))
        substituted = []
        for i in originalOFvariables:
            if i in B:
                substituted.append(i)
        # not_substituted = list(originalOFvariables)
        # for i in substituted:
        #     not_substituted.remove(i)
        initial_setting = []
        for i, key in enumerate(N):
            if key in originalOFvariables:
                initial_setting.append(original_c[key-1])
            else:
                initial_setting.append(0.0)
        for var in substituted:
            row_index = B.index(var)
            OFcoeff = original_c[var-1]
            for col in range(n):
                initial_setting[col] = initial_setting[col] + OFcoeff*(-1*A[row_index][col])
        return 0, N, B, A, b, initial_setting, v
        # there is a finite optimal sol to be calculated -> feasible
    else:
        # the -1 below represents "No Solution"
        return -1, N, B, A, b, c, v


def simplex(m, n, A, b, c):  
    # N, B, A = [0,1,2], [3,4,5], [[1.0,1.0,3.0], [2.0,2.0,5.0], [4.0,1.0,2.0]]
    # b, c, v = [30.0, 24.0, 36.0], [3.0,1.0,2.0], 0.0
    type_from_initialize, N, B, A, b, c, v = initialize_simplex(A, b, c)
    if type_from_initialize == 1:
        return [1, None]
    elif type_from_initialize == -1:
        return [-1, None]

    type_from_intloop, N, B, A, b, c, v = internal_loop(N, B, A, b, c, v)
    if type_from_intloop == 1:
        return [1, None]
    # only B and b are needed from the internal loop to compute final result
    max_setting = [0] * n  # there should be one result per original variable
    for nonbasic in range(1, n+1):
        # IMPORTANT: original nonbasics will always be (0, n-1)
        if nonbasic in B:
            pos_in_B = B.index(nonbasic)
            # variables are 1BI but vector must be 0B1. Subtract -1 (30 mins debugging). 
            max_setting[nonbasic-1] = b[pos_in_B]
    return [0, max_setting]


def readData():
    m, n = list(map(int, stdin.readline().split()))
    # m: number of constraints/rows
    # n: number of dishes/variables
    A = []
    # A: matrix of coefficients
    for i in range(m):
        A += [list(map(int, stdin.readline().split()))]
    # b: m-vector if independent variables
    b = list(map(int, stdin.readline().split()))
    # c: objective function (OF) coefficients
    c = list(map(int, stdin.readline().split()))
    # Exploring how to turn into a numpy implementation
    # A = np.array(A)
    # b = np.array(b)
    # c = np.array(c)
    return m, n, A, b, c

# CALLS
if __name__ == "__main__":
    m, n, A, b, c = readData()
    anst, ansx = simplex(m, n, A, b, c)
    if anst == -1:
        print("No solution")
    if anst == 0:  
        print("Bounded solution")
        print(' '.join(list(map(lambda x: '%.18f' % x, ansx))))
    if anst == 1:
        print("Infinity")
