# python3
import sys

def build_trie(patterns):
    # e.g., {0: {'A': 1}, 1: {'C': 4, 'G': 3, 'T': 2}, 2: {}, 3: {}, 4: {}}
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
                # current node is an empty dictionary
                current_node[letter] = index
                # add destination node to the larger tree to also be beginning node
                tree[index] = {}
                current_node = tree[index]
                index += 1
        # ADD FOR PROBLEM3
        #it is enough to add a key to denote the end of a full pattern
        current_node['FullPattern'] = ''
    return tree

def solve(text, n, patterns):

    def prefixTrieMatching(text, tree):
        # takes the text and also a trie as input
        index = 0
        symbol = text[index]  # first letter of text
        current_node = tree[0]  # first node of the trie is the root
        # pattern = str()  # empty string, will hold spelled out word

        while True:
            # reached a leaf, previous matches/traversals led here
            if not current_node.items():
                # IMPORTANT: there's at least one pattern with at least one symbol
                # this means there's at least 1 edge connecting 2 nodes
                # first iteration will never be a leaf
                # if current node has no associated destination nodes it is a leaf
                return True

            elif 'FullPattern' in current_node.keys():
                return True

            elif symbol in current_node.keys():
                # pattern = pattern + symbol
                current_node = tree[current_node[symbol]]
                index += 1
                if index < len(text):  # if within bounds of 'text'
                    symbol = text[index]
                else:
                    # ran out of text mind-pattern, pattern larger than text
                    # force the symbol to guarantee mismatch in next iteration
                    symbol = '@'
            else:
                # important: termination of no match cases
                return ''

    result = []  # will store final positions when a match is found
    pattern_trie = build_trie(patterns)  # pattern trie

    m = len(text)
    for i in range(m):
        if prefixTrieMatching(text[i:], pattern_trie):
            result.append(i)

    return result


# NOTE: don't worry about the case where one of the patterns
# is a prefix of another pattern. That will be done in another exercise
# given that patternA (pA) is a prefix of patternB (pB), the start position
# of the first symbol of both patterns is shared

# data read
data = sys.stdin.read().split()
text = data[0]
n = int(data[1])
patterns = data[2:]

# solving calls and printing
ans = solve(text, n, patterns)
sys.stdout.write(' '.join(map(str, ans)) + '\n')
