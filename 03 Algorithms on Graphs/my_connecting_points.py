#Uses python3
import sys
import math

# Disjoint-Set Data Structure Operations
def MakeSet(x):
    x.parent = x  # input is node object, therefore parent is node object
    x.rank = 0

def Find(x):
    # returns the rep node, whose parent is itself
    if x.parent == x:
        return x
    else:
        x.parent = Find(x.parent)
        return x.parent

# Union by rank
def Union(x, y):
    # inputs are node objects
    xRoot = Find(x)
    yRoot = Find(y)
    # Case1: if xRoot = yRoot, same set, do nothing
    # Case2: if equal ranks but xRoot != yRoot, diff sets
    # nodes in the same set have equal rank
    if xRoot.rank > yRoot.rank:
        yRoot.parent = xRoot
    elif xRoot.rank < yRoot.rank:
        xRoot.parent = yRoot
        # if we get this far, ranks are equal
    elif xRoot != yRoot:  # Case2, arbitrary merge
        yRoot.parent = xRoot
        xRoot.rank = xRoot.rank + 1

class Node:  # Node = Vertex
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = False  # must be initialized before MakeSet changes it
        self.rank = 0  # must be initialized before MakeSet changes it

    def __str__(self):
        return "[%d, %d] parent: %d, rank: %d" % (self.x, self.y, (self.parent and True), self.rank)

class Edge:
    # an edge is a union of nodes
    def __init__(self, x_node, y_node):
        self.x_node = x_node  # x_node is a node object
        self.y_node = y_node
        # an attribute that executes a function when called
        self.distance = self.calculate_distance()

    def __str__(self):
        return "[%d,%d] - [%d,%d]: %f" % (self.x_node.x, self.x_node.y, self.y_node.x, self.y_node.y, self.distance)

    def calculate_distance(self):
        a = (self.x_node.x - self.y_node.x)**2  # Node1 x_coord - Node2 x_coord
        b = (self.x_node.y - self.y_node.y )**2  # Node2
        return math.sqrt(a + b)


def construct_edges(nodes):
    edges = []
    for x_node in nodes:
        for y_node in nodes:
            if x_node != y_node:
                edges.append(Edge(x_node, y_node))

    # lambda: often used in functions that take a callable as a parameter
    # an edge has 3 attributes (x,y_nodes,dist) one must be chosen to sort by
    # sorted(sort this object, by this attribute)
    return sorted(edges, key=lambda edge: edge.distance)

def minimum_distance(x, y):
    result = 0.
    #write your code here
    result_edges = []
    nodes = [Node(x_coord, y[index]) for index, x_coord in enumerate(x)]
    [MakeSet(node) for node in nodes]  # in-place manipulation?

    # input provided no edges, they must be constructed
    edges = construct_edges(nodes)
    for edge in edges:
        if Find(edge.x_node) != Find(edge.y_node):
            # i.e. if the edge's nodes belong to different sets
            result_edges.append(edge)
            Union(edge.x_node, edge.y_node)

    for edge in result_edges:
        result += edge.distance

    return result

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]  # start at 1 and count 2 to the right until the end
    y = data[2::2]
    print("{:.9f}".format(minimum_distance(x, y)))
