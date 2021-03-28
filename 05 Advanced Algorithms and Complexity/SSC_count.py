# Uses python3

import sys
sys.setrecursionlimit(200000)


def reverse_graph(adj):
    reverse_adj = [[] for _ in range(len(adj))]
    for vertex in range(len(adj)):
        # reverses the direction of the edges
        for i in adj[vertex]:
            reverse_adj[i].append(vertex)  # adj[i] is the list for node i
    return reverse_adj

# Taken from CSLR:
# 1 call DFS(G) to compute finishing times u:f for each vertex u
# 2 compute GT
# 3 call DFS(GT), but in the main loop of DFS, consider the vertices
# in order of decreasing u:f (as computed in line 1)
# 4 output the vertices of ea tree in the depth-first forest formed in line 3
# as a separate strongly connected component


def number_of_strongly_connected_components(adj):
    result = 0
    visited = [False] * len(adj)
    post_order = []

    def explore(v):
        visited[v] = True
        for u in adj[v]:
            if not visited[u]:
                explore(u)
        post_order.append(v)

    def explore_reverse(v):  # don't calculate postorder
        visited[v] = True
        for u in adj[v]:
            if not visited[u]:
                explore(u)

    for v in range(len(adj)):  # DFS(G) compute finishing times for ea vertex
        if not visited[v]:
            explore(v)

    adj = reverse_graph(adj)  # compute G_transpose
    visited = [False] * len(adj)

    while post_order:  # call DFS(G_transpose) on decreasing postorder(G)
        v = post_order.pop()
        if not visited[v]:
            explore_reverse(v)
            result += 1

    return result

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
    print(number_of_strongly_connected_components(adj))
