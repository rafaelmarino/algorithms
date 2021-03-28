# python3
import sys


def find_pattern(pattern, text):
    """
    Find all the occurrences of the pattern in the text
    and return a list of all positions in the text
    where the pattern starts in the text.
    """

    def compute_prefix_function(P):
        m = len(P)
        s = [None]*m  # you can't access uninitialized list positions
        s[0] = 0  # a single character can't have a border
        border = 0
        for i in range(1, m):
            while border > 0 and P[i] != P[border]:
                border = s[border-1]  # transform from length to index
            if P[i] == P[border]:
                border += 1
            else:
                border = 0
            s[i] = border
        return s

    S = pattern + '$' + text
    s = compute_prefix_function(S)
    result = []  # empty list, will store starts of matching positions
    m = len(pattern)
    n = len(S)

    for i in range(m+1, n):
        if s[i] == m:
            result.append(i - 2*m)

    return result


if __name__ == '__main__':
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    result = find_pattern(pattern, text)
    print(" ".join(map(str, result)))
