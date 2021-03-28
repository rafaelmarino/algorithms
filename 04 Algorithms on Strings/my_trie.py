#Uses python3
import sys

# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.
def build_trie(patterns):
    tree = dict()
    tree[0] = {}  # we create key=0 as another empty dictionary
    index = 1  # this will be the second node

    for pattern in patterns:
        current_node = tree[0]  # current node is a dictionary/node object
        for letter in pattern:
            if letter in current_node.keys():  # 1st iteration always false
                # when true, simply move to destination node and do nothing else
                destination_node = current_node[letter]  # a node index
                current_node = tree[destination_node]
            else:
                # create the edge label: destination node in existing tree[0]
                current_node[letter] = index
                # add destination node to the larger tree to also be beginning node
                tree[index] = {}
                current_node = tree[index]
                index += 1

    return tree


if __name__ == '__main__':
    # split by whitespaces and remove first line
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        # for each node in the tree
        for c in tree[node]:  # no quotes needed, keys are numbers not strings
            # for each node at the end of every outgoing edge from the prev node
            print("{}->{}:{}".format(node, tree[node][c], c))
