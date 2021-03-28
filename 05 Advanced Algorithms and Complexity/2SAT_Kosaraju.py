# python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6)  # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size
# This is to avoid stack overflow issues
sys.setrecursionlimit(200000)


def constructIG(n, m, clauses):
    # n = (positive) variable count
    # 2 internal variables per variable. x => x and ~x
    # m = clause count. 2 edges per (u,v) clause (~u, v)(~v, u)
    # Key: positive vars = var*2-1 ; negative vars = (-1)*var*2
    variable_count = n * 2
    variables = list(range(1, variable_count + 1))
    # ea original variable has its positive and negated versions
    clauses = [[2*x-1 if x > 0 else -1*x*2 for x in c] for c in clauses]
    edges = []
    for clause in clauses:
        lit1 = clause[0]
        lit2 = clause[1]
        # even vars are negations, odd vars are positives
        not_lit1 = lit1-1 if lit1 % 2 == 0 else lit1+1
        not_lit2 = lit2-1 if lit2 % 2 == 0 else lit2+1
        edge1 = [not_lit1, lit2]
        edge2 = [not_lit2, lit1]
        if edge1 not in edges:
            edges.append(edge1)
        if edge2 not in edges:
            edges.append(edge2)
    return edges


def SCC(adj):
    """Compute SCC of G using Kosaraju's algo (2 DFS passes)"""
    # Post_order stores vertex ids
    post_order = []
    visited = [False] * len(adj)

    def reverse_graph(adj):
        reverse_adj = [[] for _ in range(len(adj))]
        for vertex in range(len(adj)):
            # reverses the direction of the edges
            for i in adj[vertex]:
                reverse_adj[i].append(vertex)  # adj[i] is the list for node i
        return reverse_adj

    def DFS_pass1(v):
        """Find reachable path from node v in G. Return post_order"""
        def explore(v):
            visited[v] = True
            for u in adj[v]:
                if not visited[u]:
                    explore(u)
            post_order.append(v)
        explore(v)

    def DFS_pass2(v):
        """Find reachable path from node v in T(G). Return path"""
        path = []

        def explore(v):
            visited[v] = True
            path.append(v)
            for u in reverse_adj[v]:
                if not visited[u]:
                    explore(u)
        explore(v)
        return path

    # 1. DFS(G) to compute finishing times u.f for eah vertex u
    for vertex in range(len(adj)):
        if not visited[vertex]:
            DFS_pass1(vertex)
    # 2. Compute G_t
    reverse_adj = reverse_graph(adj)
    # 3. DFS(G_t). Consider the vertices in order of decreasing u.f from #1
    # 4. The vertices of each tree in the DFS forest constitute a SCC
    visited = [False] * len(adj)
    scc = []
    while post_order:
        # NOTE: returns SCCs in topo order because stacked is popped every run
        v = post_order.pop()
        if not visited[v]:
            scc_i = DFS_pass2(v)
            scc.append(scc_i)
    # turn result to 1BI
    for i in range(len(scc)):
        for j in range(len(scc[i])):
            scc[i][j] += 1
    return scc


def isSatisfiable(n, m, clauses):
    """Decide whether UNSAT or SAT. If SAT return CNF Formula(2SAT)"""
    # n: number of variables
    # m: number of clauses
    IG_edges = constructIG(n, m, clauses)
    # turn edges into adj list
    adj = [[] for _ in range(n*2)]
    for (a, b) in IG_edges:
        adj[a - 1].append(b - 1)
    SCCs = SCC(adj)
    revSCCs = [0] * (n * 2)
    for i, C in enumerate(SCCs):
            for var in C:
                revSCCs[var-1] = i+1
    for i in range(1, n*2, 2):
        # ex. (x, ~x) is (1,2), subtract1 to access the list
        lit = i
        not_lit = i+1
        if revSCCs[lit-1] == revSCCs[not_lit-1]:
            # "UNSATISFIABLE"
            return None
    # If not UNSAT then SAT. Return CNF Formula
    assigned = [False for _ in range(n*2)]
    result = [False for _ in range(n*2)]
    while SCCs:
        C = SCCs.pop()
        for c in C:
            if not assigned[c-1]:
                result[c-1] = 1
                assigned[c-1] = True
                not_c = c-1 if c % 2 == 0 else c+1
                result[not_c-1] = 0
                assigned[not_c-1] = True

    result = result[0::2]
    result = [i+1 if result[i] == 1 else (i+1)*-1 for i in range(len(result))]
    return result


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
