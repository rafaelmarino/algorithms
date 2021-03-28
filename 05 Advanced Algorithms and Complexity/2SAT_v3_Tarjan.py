# python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6)  # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size
# This is to avoid stack overflow issues
# sys.setrecursionlimit(200000)


def constructIG(n, m, clauses):
    # n: # variables
    # m: # clauses
    vertices = list(range(1, n+1))
    variables = list(range(-n,0))
    for v in vertices:
        variables.append(v)

    edgeDic = dict()
    for v in vertices:
        edgeDic[v] = []
        edgeDic[-v] = []

    for clause in clauses:
        lit1, lit2 = clause[0], clause[1]
        edgeDic[-lit1].append(lit2)
        edgeDic[-lit2].append(lit1)

    return variables, edgeDic


def strongly_connected_components(graph):
    """ Find the strongly connected components in a graph using
        Tarjan's algorithm.
        graph should be a dictionary mapping node names to
        lists of successor nodes.
        """
    result = []
    stack = []
    low = {}

    def visit(node):
        if node in low: return
        num = len(low)
        low[node] = num
        stack_pos = len(stack)
        stack.append(node)

        for successor in graph[node]:
            visit(successor)
            low[node] = min(low[node], low[successor])

        if num == low[node]:
            component = tuple(stack[stack_pos:])
            del stack[stack_pos:]
            result.append(component)
            for item in component:
                low[item] = len(graph)

    for node in graph:
        visit(node)

    return result


def isSatisfiable(n, m, clauses):
    # n: number of variables
    # m: number of clauses
    vertices, IG = constructIG(n, m, clauses)
    # turn edges into adj list
    SCCs = strongly_connected_components(IG)
    # if x and ~x are in the same SCC then UNSAT
    # reverseSCC is a dictionary that maps {variable: SCC_id}
    reverseSCC = dict()
    for i, C in enumerate(SCCs):
        for variable in C:
            reverseSCC[variable] = i
    for var in range(1, n+1):
        if reverseSCC[var] == reverseSCC[-var]:
            # "UNSATISFIABLE"
            return None
    # If not UNSAT then SAT. Return a SAT assignment of original vars
    assignedDic = dict()
    for var in vertices:
        assignedDic[var] = False
    result = dict()
    for C in SCCs:
        for c in C:
            if assignedDic[c] is False:
                result[abs(c)] = c
                assignedDic[c] = True
                assignedDic[-c] = True

    final_result = [result[i] for i in range(1, n+1)]
    return final_result


def readData():
    n, m = map(int, input().split())
    clauses = [list(map(int, input().split())) for i in range(m)]
    return n, m, clauses


def main():
    n, m, clauses = readData()
    result = isSatisfiable(n, m, clauses)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(*result)

# CALLS
threading.Thread(target=main).start()
