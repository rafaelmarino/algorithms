# python3
import itertools


def readData():
    # n = # vertices
    # m = # edges
    n, m = map(int, input().split())
    edges = [list(map(int, input().split())) for i in range(m)]
    return(n, m, edges)


def satFormula(n, m, edges):
    """Compute SAT formula. Return (Clause_count, Var_count, Clause_matrix)"""
    # n = # vertices
    # m = # edges
    vertexIds = list(range(1, n+1))
    variable_count = n**2
    variables = list(range(1, variable_count + 1))
    variables = [variables[i:i+n] for i in range(0, variable_count, n)]
    # (Feb/06/2018: Spent 3hours debugging a hardcoded 5 instead of n in 20:33)
    # NOTE: rows are positions in HP, columns are vertices/nodes
    # 5 Clauses(C) required
    # C1: each node j must appear in the path

    def transpose(matrix):
        return [list(row) for row in zip(*matrix)]
    clause1 = transpose(variables)
    # C2: no node j appears twice in the path
    clause2 = []
    for vertex in clause1:
        combinations = list(itertools.combinations(vertex, 2))
        for combination in combinations:
            clause2.append(combination)
    clause2 = [[-x, -y] for x, y in clause2]
    # C3: every position i in HP must be ocuppied. C3 == variables
    # C4: no two nodes occupy the same position (no pos holds more than 1 node)
    clause4 = []
    for row in variables:
        combinations = list(itertools.combinations(row, 2))
        for combination in combinations:
            clause4.append(combination)
    clause4 = [[-x, -y] for x, y in clause4]
    # C5: Vertices with no edges between them cannot be adjacent in HP
    clause5 = []
    all_combinations = []
    for u in range(1, n+1):
        remainder = list(vertexIds)
        remainder.remove(u)
        for v in remainder:
            all_combinations.append([u, v])
    reversed_edges = [[y, x] for (x, y) in edges]
    full_edges = edges + reversed_edges
    # full edges stores the original edges plus reversed direction
    non_edges = []
    # non_edges will become indices
    for edge in all_combinations:
        if edge not in full_edges:
            non_edges.append(edge)
    # transforming to zero-based index
    non_edges = [[x-1, y-1] for (x, y) in non_edges]
    # selecting variables of contiguous HP positions with non_edge in G
    for position in range(n-1):
        # don't acess the final position (would cause index error)
        for non_E in non_edges:
            u_variable = variables[position][non_E[0]]
            v_variable = variables[position + 1][non_E[1]]
            literal = [u_variable, v_variable]
            clause5.append(literal)
    clause5 = [[-x, -y] for x, y in clause5]
    final_clauses = clause1 + clause2 + variables + clause4 + clause5
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
