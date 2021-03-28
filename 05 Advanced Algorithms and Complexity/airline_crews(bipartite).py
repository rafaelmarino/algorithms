# python3

# def read_data():
#     n, m = map(int, input().split())  # n = flights, m = crews
#     # for each flight store a binary flag of whether crew i can work it
#     adj_matrix = [list(map(int, input().split())) for i in range(n)]
#     return adj_matrix
import sys

def read_data():
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]  # flights, crews
    data = data[2:]
    # for each flight store a binary flag of whether crew i can work it
    adj_matrix = list()
    for _ in range(n):
        crew_info = data[0:m]
        data = data[m:]
        adj_matrix.append(crew_info)
    return adj_matrix

def write_response(matching):
    line = [str(-1 if x == -1 else x) for x in matching]
    print(' '.join(line))


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
        # addition for Q2
        self.u_count = 0

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


def matrix_to_flow_graph(adj_matrix):
    u_count, v_count = len(adj_matrix), len(adj_matrix[0])
    vertex_count = u_count + v_count + 2  # the 2 accounts for s+t vertices
    # calculating edge_count is a bit more complex
    # potential_departures = list()
    # for flight in range(u_count):
    #     edges_per_flight = sum(adj_matrix[flight])
    #     potential_departures.append(edges_per_flight)
    # middle_edge_count = sum(potential_departures)
    # edge_count = u_count + v_count + middle_edge_count

    # graph initialized with empty values
    graph = FlowGraph(vertex_count)
    # constructing all (u,v) pairs = (s->u) + (u->v) + (v->t)
    s_to_u = list()
    for flight in range(u_count):
        # 2 because 1 takes care of 0BI -> 1BI; 1 takes care of s being vertex_1
        # remember that flights begin at i = 0. we need it to be i = 2 (after the source = 1)
        s_to_u.append((0, flight + 1)) # source is always vertex 1
    u_to_v = list()
    for flight in range(u_count):
        for crew in range(v_count):
            if adj_matrix[flight][crew] == 1:
                u_to_v.append((1 + flight, 1 + u_count + crew))
    v_to_t = list()
    for crew in range(v_count):
        # 2 because 1 takes care of 0BI -> 1BI; 1 takes care of s being vertex_1
        v_to_t.append((1 + u_count + crew,  vertex_count - 1))  # sink is always vertex n

    all_pairs = s_to_u + u_to_v + v_to_t

    for pair in all_pairs:
        u = pair[0]
        v = pair[1]
        graph.add_edge(u, v, 1)

    graph.u_count = u_count
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


def max_matching_flow(graph, from_, to):
    flow = 0
    # added for Q2 (this is the variable that will be returned at the end)
    final_matching = [-1] * graph.u_count
    # end of addition
    path = findPathEdgeIndices(graph, from_, to)
    # ADDITION FOR Q2
    # paths_taken = list()
    if path == -1:
        return final_matching
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
        # Addition for Q2
        # paths_taken.append(path)
        # end of addition
        path = findPathEdgeIndices(graph, from_, to)

    # extracting middle_edges
    # TRICKY PART, caused 2h of debugging
    # dim = len(paths_taken)
    # last_path = paths_taken[dim-1]

    u_vertices = list(range(1, graph.u_count + 1))
    forward_from_u = list()
    for u in u_vertices:
        u_edges = graph.get_ids(u)
        for edge_id in u_edges:
            if edge_id % 2 == 0:
                forward_from_u.append(edge_id)

    used_middle_edges_ids = list()
    for edge_id in forward_from_u:
        if graph.get_edge(edge_id).flow > 0:
            used_middle_edges_ids.append(edge_id)

    u_v_pair = list()
    for edge_id in used_middle_edges_ids:
        triplet = graph.get_edge(edge_id)
        u = triplet.u
        v = triplet.v
        u_v_pair.append((u, v))

    for pair in u_v_pair:
        flight_id = pair[0] - 1  # need to slice at 0BI
        # turning crew id to 1BI
        crew_id = pair[1] - graph.u_count
        final_matching[flight_id] = crew_id

    return final_matching
    # returning (u(flights), v(crews)) matching instead of max flow


if __name__ == '__main__':
    adj_matrix = read_data()
    graph = matrix_to_flow_graph(adj_matrix)
    matching = max_matching_flow(graph, 0, graph.size() - 1)
    write_response(matching)