#Uses python3

import sys

# BELLMAN-FORD
def negative_cycle(adj, cost):

    def initialize():
        total_cost = 0
        for vertex in cost:
            total_cost += sum(vertex)
        inf = total_cost + 1  # upper bound, unreachable distance, similar to inf
        n = len(adj)  # number of vertices
        dist = [inf] * n
        dist[0] = 0  # the start is at 0 dist from itself
        return dist, n

    dist, n = initialize()

    def relax(u,v,i):
        if dist[v] > dist[u] + cost[u][i]:
            dist[v] = dist[u] + cost[u][i]
            return True

    for x in range(n-1):
        for u,v in enumerate(adj):
            i = 0  # index of target vertex being explored in v[]
            while i < len(v):
                # while there is an element in the list of target vertices
                relax(u, v[i], i)
                i += 1

    # Final pass, if any edge is relaxed AGAIN there is a negative cycle
    for u, v in enumerate(adj):
        i = 0  # index of target vertex being explored in v[]
        while i < len(v):
            # while there is an element in the list of target vertices
            a = relax(u, v[i], i)
            i += 1
            if a is True:
                return 1

    return 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)
    print(negative_cycle(adj, cost))
