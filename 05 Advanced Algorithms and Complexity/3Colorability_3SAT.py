# python3


def readData():
    # n = # vertices
    # m = # edges
    n, m = map(int, input().split())
    edges = [list(map(int, input().split())) for i in range(m)]
    return(n, m, edges)


def satFormula(n, m, edges):
    """Compute SAT formula. Return (Clause_count, Var_count, Clause_matrix)"""
    # n = vertex count
    # m = edge count
    variables = list(range(1, 3*n + 1))
    variables = [variables[i:i+3] for i in range(0, len(variables), 3)]
    variable_count = n*3
    # (eg)variables = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    vertex_clauses = []
    for vertex in variables:
        # (A1 or A2 or A3)&(notA1 or notA2)&(notA2 or notA3)&(notA1 or notA3)
        vertex_clauses.append(vertex)
        vertex_clauses.append([-vertex[0], -vertex[1]])
        vertex_clauses.append([-vertex[1], -vertex[2]])
        vertex_clauses.append([-vertex[0], -vertex[2]])

    edge_clauses = []
    for edge in edges:
        # (notA1 or notB1)&(notA2 or notB2)(notA3 or notB3)
        u, v = edge[0] - 1, edge[1] - 1
        clauses = list(zip(variables[u], variables[v]))
        clauses = [[-x, -y] for x, y in clauses]
        for clause in clauses:
            edge_clauses.append(clause)

    final_clauses = vertex_clauses + edge_clauses
    for clause in final_clauses:
        # adding the 0 at the end required by SAT-solver
        clause.append(0)

    clause_count = len(final_clauses)
    return(clause_count, variable_count, final_clauses)

if __name__ == "__main__":
    n, m, edges = readData()
    C, V, clauses = satFormula(n, m, edges)
    print(*(C, V))
    for clause in clauses:
        print(*clause)
