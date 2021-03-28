# python3
import sys


def InverseBWT(bwt):
    # create tuples that hold symbol, index
    # symbol must go first as we later want to sort by symbol
    last = [(symbol, id) for (id, symbol) in enumerate(bwt)]
    first = sorted(last)
    # first_to_last = {f: l for f, l in zip(first, last)}
    first_to_last = {}
    first_to_last.update(zip(first,last))


    current_pair = first[0]  # (symbol, id)
    result = ''
    for i in range(len(bwt)):
        # 1) append the preceding symbol to result
        # 2) preceding symbol is found as a beginning coordinate
        # 3) reiterate with appending destination and using as beginning
        result += current_pair[0]  # (symbol)
        current_pair = first_to_last[current_pair]

    final = list(reversed(result))

    return ''.join(final)


if __name__ == '__main__':
    bwt = sys.stdin.readline().strip()
    print(InverseBWT(bwt))