# uses python3

import sys


def reach(adj, x, y):
    # solution vector
    visited = [False for i in range(n)]
    # write your code here
    path = []

    def explore(vertex_index):
        # each vertex keeps a boolean to specify if visited
        visited[vertex_index] = True
        path.append(vertex_index)
        for i in adj[vertex_index]:
            if not visited[i]:
                explore(i)

    explore(x)

    # Working but returns entire reachable path from u. Doesn't stop at v
    # convert path to 1BI before returning
    return [i+1 for i in path] if y in path else -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]  # n vertices and m edges, one line per edge
    data = data[2:]  # remove n,m from the list
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))  # ordered pairs
    x, y = data[2 * m:]  # vertex x, vertex y; from x to y
    adj = [[] for _ in range(n)]
    x, y = x - 1, y - 1  # going from 1BI to 0BI
    for (a, b) in edges:
        adj[a - 1].append(b - 1)  # going from 1BI to 0BI
        adj[b - 1].append(a - 1)  # going from 1BI to 0BI
    print(reach(adj, x, y))
