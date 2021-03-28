# uses python3

import itertools
read_count = 5  # passing parameter problem1: 1618
min_overlap_len = 1  # passing parameter problem1: 70
# read_length(phiX174) = 100


def spell_genome(reads, k):
    """Return the genome (Shortest Common Superstring) from reads.
    Greedy implementation: starting from read0, follow the path
    spelled by the next read with max overlap, until no more reads left.
    This script is designed for larger problems that guarantee the
    existence of another read v while standing in read u.
    If there are no reads to travel to, it will crash"""

    def overlap(a, b, min_length=3):
        """ Return length of longest suffix of 'a' matching
            a prefix of 'b' that is at least 'min_length'
            If no such overlap exists, return 0. """
        start = 0  # start all the way at the left
        while True:
            # only one check needed to detect if min overlap len met
            start = a.find(b[:min_length], start)  # look for b's prefix in a
            if start == -1:  # no more occurrences to right
                return 0
            # found occurrence; check for full suffix/prefix match
            if b.startswith(a[start:]):
                return len(a)-start
            start += 1  # move just past previous match

    def max_overlap(read_i):
        max_olap = 0
        for read in reads:
            if read_i != read:
                olap = overlap(read_i, read, k)
                if olap > max_olap:
                    max_olap = olap
                    v = read
        reads.remove(read_i)
        return v, max_olap

    # removing duplicates
    reads = list(set(reads))
    beginning = reads[0]
    current_read = reads[0]
    genome = current_read
    for _ in range(len(reads)-1):
        # print(current_read, genome)
        current_read, olen = max_overlap(current_read)
        genome += current_read[olen:]

    # cutting off the overlap from genome and the start to make full circle
    return genome[:-overlap(genome, beginning, 1)]


def readData():
    # reads = ['AAC', 'ACG', 'GAA', 'GTT', 'TCG']
    reads = []
    for _ in range(read_count):
        reads.append(input())
    return reads

if __name__ == '__main__':
    reads = readData()
    print(spell_genome(reads, min_overlap_len))
