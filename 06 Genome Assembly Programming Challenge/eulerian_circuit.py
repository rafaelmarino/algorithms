# uses python3


def hierholzer(v, e, adj_list):
    """Return the Eulerian Cycle (EC) of graph G. G is guaranteed to be a SCC.
     A directed graph contains an EC if it is a SCC and the in-degree
     and out-degree of each vertex are equal.
     Hierholzer's algorithm: start from any vertex u and follow a path
     until u is found again. If G has edges left but out_deg(curr_node) = 0
     then backtrack in the path until vertex with outdeg>0 is found.
     Continue on this new path, else if no such vertex, no EC."""
    current_path = [0]
    circuit = []
    current_node = 0

    in_deg = [0] * v
    out_deg = [0] * v

    edges_left = sum([1 if i else 0 for i in adj_list])
    while edges_left > 0:
        # if current node doesn't have any unused edge, then:
        # 1) current_path.pop() and append to the circuit
        # 2) check prev vertices in curr_path until out_deg > 0
        if not adj_list[current_node]:
            # backtrack in the current path until out_deg(current_node) > 0
            # if it's not possible to backtrack anymore then remaining
            # edges are incoming and not outgoing. No EC in G
            while not adj_list[current_node]:
                circuit.append(current_path.pop())
                if current_path:
                    current_node = current_path[-1]
                else:
                    return 0
        else:
            # move to the next vertex and burn the edge
            out_deg[current_node] += 1
            current_node = adj_list[current_node].pop(0)
            in_deg[current_node] += 1
            current_path.append(current_node)
        # value needs to recalculate
        edges_left = sum([1 if i else 0 for i in adj_list])

    # Eulerian Cycle must have in_deg(u) == out_deg(u) for all vertices
    for v in range(v):
        if in_deg[v] != out_deg[v]:
            return 0

    eulerian_cycle = current_path + list(reversed(circuit))
    return eulerian_cycle


def readData():
    """ Return count(V), count(E) and adj list from line-after-line input """
    v, e = map(int, input().split())
    adj_list = [[] for _ in range(v)]
    for _ in range(e):
        a, b = map(int, input().split())
        adj_list[a-1].append(b-1)
    return v, e, adj_list

if __name__ == '__main__':
    v, e, adj_list = readData()
    eulerian_cycle_nodes = hierholzer(v, e, adj_list)
    if not eulerian_cycle_nodes:
        print(0)
    else:
        eulerian_cycle_nodes = [i+1 for i in eulerian_cycle_nodes]
        print(1, ' '.join(map(str, eulerian_cycle_nodes[:-1])), sep='\n')
