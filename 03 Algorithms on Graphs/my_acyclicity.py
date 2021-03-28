#Uses python3

import sys

def acyclic(adj):
    # create a list with a sublist for each node
    visited = [False for i in range(len(adj))]
    previsit = [[] for i in range(len(adj))]
    postvisit = [[] for i in range(len(adj))]
    acyclic.pre_count = 0
    acyclic.post_count = 0

    def DFS(x):
        visited[x] = True
        previsit[x] = acyclic.pre_count
        acyclic.pre_count += 1
        for w in adj[x]:
            if visited[w] is False:
                DFS(w)
        postvisit[x] = acyclic.post_count
        acyclic.post_count += 1

    for i in range(len(adj)):
        if visited[i] is False:
            DFS(i)

    # breaking a double for, one break per for loop
    cycle = False
    for i in range(len(adj)):
        for j in adj[i]:
            if postvisit[i] < postvisit[j]:
                cycle = True
                break
        if cycle is True:
            break
    # return postvisit, (i,j)
    return 1 if cycle is True else 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n)]
    for (a, b) in edges:
        adj[a - 1].append(b - 1)
        # adj = adjacency list: node i connects to nodes [(a,b,c)]
    print(acyclic(adj))
