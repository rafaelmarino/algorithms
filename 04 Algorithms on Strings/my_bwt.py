# python3
import sys

def BWT(text):

    # create all rotations using mirror technique
    n = len(text)
    new_text = text * 2
    # lists slice differently, overflowing doesn't create an access error
    # when slicing a list, closing interval number is excluded
    # n from range(n) goes into i;
    rotations = [new_text[i:i + n] for i in range(n)]

    # lexicographical sort
    rotations = sorted(rotations)

    # taking the last column direct accessing is always 0BI
    final_column = [rotations[row][n-1] for row in range(n)]

    # pasting all symbols together right at return
    return ''.join(final_column)

if __name__ == '__main__':
    text = sys.stdin.readline().strip()
    # print() automatically removes the quotes from a string object
    print(BWT(text))