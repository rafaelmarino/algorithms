#Uses python3

import sys


def bipartite(adj):
    n_nodes = len(adj)
    dist = [-1] * n_nodes   # initialize all nodes as unvisited (-1)
    dist[0] = 0  # the start node has 0 distance from itself
    colors = [None] * n_nodes
    colors[0] = True
    Q = list()  # queue of vertex indices to process
    Q.append(0)  # process the start node first
    bipartite.bi_part = True

    def BFS():
        while Q:
            current = Q.pop(0)  # de-queue the first node then process it
            # IMPORTANT: only nodes with distances can be en-queued and de-queued
            # if current == target:  # current is the start node in first iteration
            #     return dist[current]
            for v in adj[current]:
                if colors[current] == colors[v]:
                    bipartite.bi_part = False
                    break
                if dist[v] == -1:  # (-1) = hasn't been visited before
                    dist[v] = dist[current] + 1
                    colors[v] = not colors[current]
                    Q.append(v)

    # for i in range(len(adj)):  # for each node
    #     if dist[i] is -1:
    #         BFS(i)
    BFS()
    return 1 if bipartite.bi_part is True else 0

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
    print(bipartite(adj))
