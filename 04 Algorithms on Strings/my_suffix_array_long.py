# python3
import sys


def build_suffix_array(S):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    # Function definitions
    def sort_characters(S):
        # order is indexed by character/letter
        # value(i=0) represents the position of the smallest letter in S
        order = [None]*len(S)
        count = dict()
        alphabet = '$ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            count[letter] = 0
        for i in range(0, len(S)):
            count[S[i]] += 1
        for j in range(1, len(alphabet)):
            previous = alphabet[j-1]
            current = alphabet[j]
            count[current] = count[current] + count[previous]
        for w in range(len(S)-1, -1, -1):
            c = S[w]
            count[c] -= 1
            # slice order in the count of the current letter (w)
            order[count[c]] = w
        return order

    def compute_char_classes(S, order):
        # class is indexed by suffix id
        # [,,,,,,0] <--> suffix_6 has class 0
        clas = [None]*len(S)
        clas[order[0]] = 0
        for i in range(1, len(S)):
            if S[order[i]] != S[order[i-1]]:
                clas[order[i]] = clas[order[i-1]] + 1
            else:
                clas[order[i]] = clas[order[i-1]]
        return clas

    def sort_doubled(S, L, order, clas):
        # count is indexed by class id
        count = [0]*len(S)
        new_order = [None]*len(S)
        for i in range(0, len(S)):
            count[clas[i]] += 1
        for j in range(1, len(S)):
            count[j] = count[j] + count[j-1]
        for i in range(len(S)-1, -1, -1):
            start = (order[i] - L + len(S)) % len(S)
            cl = clas[start]
            count[cl] -= 1
            new_order[count[cl]] = start
        return new_order

    def update_classes(new_order, clas, L):
        n = len(new_order)
        new_clas = [None]*n
        new_clas[new_order[0]] = 0
        for i in range(1, n):
            cur = new_order[i]
            prev = new_order[i-1]
            mid = cur+L
            mid_prev = (prev + L) % n
            if clas[cur] != clas[prev] or clas[mid] != clas[mid_prev]:
                new_clas[cur] = new_clas[prev] + 1
            else:
                new_clas[cur] = new_clas[prev]
        return new_clas

    # Function calls
    order = sort_characters(S)
    clas = compute_char_classes(S, order)
    L = 1
    while L < len(S):
        order = sort_doubled(S, L, order, clas)
        clas = update_classes(order, clas, L)
        L = 2*L
    return order


if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))
