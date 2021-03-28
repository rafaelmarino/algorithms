# Uses python3


def edit_distance(string1, string2):
    rows = len(string1) + 1  # the height (rows); ith entries
    cols = len(string2) + 1  # the width (cols); jth entries

    # creating the distance matrix
    d = [[0 for x in range(cols)] for y in range(rows)]  # cols by rows; don't ask
    # filling out the first column and the first row with their distance, dist=prefix
    for i in range(0, rows):
        d[i][0] = i
    for j in range(0, cols):
        d[0][j] = j

    # Outer for loop for the columns: j
    for j in range(1, j+1):
        # Inner for loop for the rows: i
        for i in range(1, i+1):
            insertion = d[i][j-1] + 1
            deletion = d[i-1][j] + 1
            match = d[i-1][j-1]
            mismatch = d[i-1][j-1] + 1  # also called substitution

            if string1[i-1] == string2[j-1]:
                d[i][j] = min(insertion, deletion, match)
            else:
                d[i][j] = min(insertion, deletion, mismatch)

    print(d[rows-1][cols-1])
    #print(d)

# INPUT
string1 = input()
string2 = input()

print(edit_distance(string1, string2))
