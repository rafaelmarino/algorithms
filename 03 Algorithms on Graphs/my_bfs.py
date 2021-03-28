#Uses python3

import sys


def distance(adj, u, v):
    n_nodes = len(adj)
    dist = [-1] * n_nodes   # initialize all nodes as unvisited (-1)
    dist[u] = 0  # the start node has 0 distance from itself
    Q = list()  # queue of vertex indices to process
    Q.append(u)  # process the start node first

    def BFS(target):
        while Q:
            current = Q.pop(0)  # de-queue the first node then process it
            # IMPORTANT: only nodes with distances can be en-queued and de-queued
            if current == target:  # current is the start node in first iteration
                return dist[current]
            for v in adj[current]:  # each adjacent node to current node (st, u to v)
                if dist[v] == -1:  # (-1) = hasn't been visited before
                    dist[v] = dist[current] + 1
                    Q.append(v)

    BFS(v)
    return dist[v] if dist[v] is not -1 else -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))  # 2*m = len(data)
    adj = [[] for node in range(n)]
    for (a, b) in edges:  # for each tuple of (origin_vertex, dest_vertex)
        adj[a - 1].append(b - 1)
        adj[b - 1].append(a - 1)
    s, t = data[2 * m] - 1, data[2 * m + 1] - 1  # u and v
    print(distance(adj, s, t))
