# uses python3

import sys


def toposort(adj):
    visited = [False] * len(adj)
    postorder = []
    toposort.count = 0

    def DFS(x):
        visited[x] = True
        for w in adj[x]:
            if visited[w] is False:
                DFS(w)
        postorder.append(x)

    # not enough to run DFS(0). DFS needs to be run on every unvisited vertex
    for i in range(len(adj)):
        if visited[i] is False:
            DFS(i)

    # for topoSort the greatest postorder goes first (final element in stack)
    # meaning they represent foundational dependencies for many vertices

    return list(reversed(postorder))

if __name__ == '__main__':
    input = sys.stdin.read()
    # split() defaults to white spaces but also adjusts for a new line ('\n')
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)  # Transition from 1BI to 0BI
    order = toposort(adj)
    for x in order:
        print(x + 1, end=' ')
