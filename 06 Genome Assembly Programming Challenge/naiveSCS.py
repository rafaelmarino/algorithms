# uses python3

import itertools
read_count = 1618
min_overlap_len = 70


def overlap(A, B, min_length=min_overlap_len):
    """Return length of longest suffix of A matching
    a prefix of B that is at least min_length characters long.
    If no such overlap exists, return 0."""
    start = 0  # start all the way at the left
    while True:
        # Look for B's prefix in A's suffix
        start = A.find(B[:min_length], start)  # start implies A[start:]
        if start == -1:  # no more occurrences to right
            return 0
        # found occurrence; check for full suffix/prefix match
        # already know that A contains the prefix B[:min_len]
        # Does ALL of B begin with A[start:]?
        # KEY: potential overlap counts decrease from max to 0, left to right
        if B.startswith(A[start:]):  # returns True or False
            return len(A) - start
        start += 1  # move just past previous match


def SCS(ss):
    """ Returns shortest common superstring of given strings,
        assuming no string is a strict substring of another """
    shortest_sup = None
    for ssperm in itertools.permutations(ss):
        sup = ssperm[0]
        for i in range(len(ss)-1):
            olen = overlap(ssperm[i], ssperm[i+1], min_length=1)
            sup += ssperm[i+1][olen:]
        if shortest_sup is None or len(sup) < len(shortest_sup):
            shortest_sup = sup
    return shortest_sup

# def naive_overlap_map(reads, k):
#     olaps = {}
#     for (a, b) in permutations(reads, 2):
#         olen = overlap(a, b, k)
#         if olen > 0:
#             olaps[(a, b)] = olen
#     return olaps


def readData():
    reads = []
    for _ in range(read_count):
        reads.append(input())
    return reads

if __name__ == '__main__':
    reads = readData()
    print(SCS(reads))
