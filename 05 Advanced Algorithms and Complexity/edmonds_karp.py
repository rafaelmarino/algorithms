# python3

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0  # all vertices are initialized with the trivial flow

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

        # Visualizing edges
        # result = list()
        # for i in range(7 * 2):
        #     thing = input.edges[i]
        #     result.append((thing.u, thing.v, thing.capacity, thing.flow))
        # print(result)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        # returns
        return self.graph[from_]

    def get_edge(self, id):
        # returns the edge object (u,v,c,f) for edge i
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow
        # Rafa added:
        self.edges[id].capacity -= flow
        self.edges[id ^ 1].capacity += flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    # graph initialized with empty values
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def findPathEdgeIndices(input, u, v):
    # Input: graph OBJECT (it has graph.graph, graph.edges, etc)
    # Output: edge indices for BFS path from u to v
    vertex_count = input.size()
    adj_edges = [[] for i in range(vertex_count)]  # one list per vertex
    for vertex in range(vertex_count):
        for edge_index in input.get_ids(vertex):
            # edge is an object (u,v,c,f). v is the variable of interest
            destination_vertex = input.get_edge(edge_index).v
            edge_capacity = input.get_edge(edge_index).capacity
            # KEY: store in each vertex i, the destination vertex and the id of the edge used
            adj_edges[vertex].append((destination_vertex, edge_index, edge_capacity))

    n_nodes = len(adj_edges)
    dist = [-1] * n_nodes   # initialize all nodes as unvisited (-1)
    dist[u] = 0  # the start node has 0 distance from itself
    pred = [() for i in range(n_nodes)]
    # pred stores where vertex i came from and through which edge, (u, edge i)
    pred[u] = (-1, -1)  #
    Q = list()  # queue of vertex indices to process
    Q.append(u)  # process the start node first

    def BFS(target):
        while Q:
            current = Q.pop(0)  # de-queue the first node then process it
            # IMPORTANT: only nodes with distances can be en-queued and de-queued
            if current == target:  # current is the start node in first iteration
                break
            for v_edge_triplet in adj_edges[current]:
                # each v_edge_pair (v, edge i)
                v_ = v_edge_triplet[0]
                edge_id = v_edge_triplet[1]
                edge_cap = v_edge_triplet[2]
                if dist[v_] == -1 and edge_cap > 0:  # (-1) = hasn't been visited before
                    dist[v_] = dist[current] + 1
                    pred[v_] = (current, edge_id)
                    Q.append(v_)

        # extracting edge path from the predecessor list (pred)
        # pred: (predecessor, edge index) per vertex visited
        # deconstruct from v to u and then flip
        if dist[target] != -1:  # the target was reached
            edge_indices_reverse = list()
            previous_vertex = pred[target][0]
            used_edge_id = pred[target][1]
            edge_indices_reverse.append(used_edge_id)
            if pred[previous_vertex][0] == -1:
                # ALGORITHM FINALLY PASSED AFTER 3 WEEKS OF RESEARCH AND ADDING THIS LINE
                # i.e. stop if source is reached
                return edge_indices_reverse
            while previous_vertex != -1:
                edge = pred[previous_vertex][1]
                edge_indices_reverse.append(edge)
                previous_vertex = pred[previous_vertex][0]
                if pred[previous_vertex][0] == -1:
                    # i.e. stop if source is reached
                    break
            return list(reversed(edge_indices_reverse))
        else:
            return -1
    return BFS(v)


def max_flow(graph, from_, to):
    flow = 0
    path = findPathEdgeIndices(graph, from_, to)
    if path == -1:
            return flow
    while path != -1:
        # caps will store the caps of edges in the path to extract the min
        caps = list()
        for edge_id in path:
            cap = graph.get_edge(edge_id).capacity
            caps.append(cap)
        min_cap = min(caps)
        for edge in path:
            graph.add_flow(edge, min_cap)
        flow += min_cap
        path = findPathEdgeIndices(graph, from_, to)
    return flow


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))