#Uses python3

import sys
import queue


def distance(adj, cost, s, t):
    total_cost = 0
    for vertex in cost:
        total_cost += sum(vertex)
    inf = total_cost + 1  # upper bound, unreachable distance, similar to inf

    n = len(adj)  # number of vertices

    dist = [inf] * n
    dist[s] = 0  # the start is at 0 dist from itself
    visited = [False] * n  # all vertices start as unvisited

    # u and v are indices of vertices
    def relax(u,v,i):
        if dist[v] > dist[u] + cost[u][i]:
            dist[v] = dist[u] + cost[u][i]

    def extract_min(inf):
        min = inf  # starting with the highest value, will decrease by the end
        index = 0  # starting with 0 index
        for i in range(len(dist)):
            if visited[i] == False and dist[i] <= min:
                # if not yet visited and if distance is less than current min
                min = dist[i]
                index = i
        return index

    while sum(visited) < n:
        u = extract_min(inf)
        visited[u] = True  # this vertex won't be checked again
        for i,v in enumerate(adj[u]):
            relax(u,v,i)

    # return dist
    return dist[t] if dist[t] < inf else -1

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
    s, t = data[0] - 1, data[1] - 1
    print(distance(adj, cost, s, t))
