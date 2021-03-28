# Uses python3

import sys
sys.setrecursionlimit(200000)


def SCC(adj):
    """Compute SCC of G using Kosaraju's algo (2 DFS passes)"""
    # Post_order stores vertex ids
    # Takes as input an adjacency list
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
        # the node in the far right always has the max finishing time
        v = post_order.pop()
        if not visited[v]:
            scc_i = DFS_pass2(v)
            scc.append(scc_i)
    # turn result to 1BI
    for i in range(len(scc)):
        for j in range(len(scc[i])):
            scc[i][j] += 1

    return scc


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(SCC(adj))
