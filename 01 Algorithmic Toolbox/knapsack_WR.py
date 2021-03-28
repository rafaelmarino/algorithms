# Uses python3


def knapsack_WR(W, weights):

    n = len(weights)  # number of items/rows
    # Initializing the max value matrix
    # i+1 rows by W+1 cols (+1 because of the zero row and column)
    matrix = [[0 for x in range(W+1)] for y in range(n+1)]  # cols by rows; don't ask

    # Outer loop: scanning every item
    for i in range(1, n+1):  # current item; rows
        # Inner loop: scanning every possible knapsack
        for j in range(1, W+1):  # current knapsack; columns
            matrix[i][j] = matrix[i-1][j]
            if weights[i-1] <= j:
                # val = item's weight + max weight w/o the item
                val = weights[i-1] + matrix[i-1][j-weights[i-1]]
                if matrix[i][j] < val:
                    matrix[i][j] = val

    return matrix[n][W]


# INPUT

W, n = map(int, input().split())
weights = list(map(int, input().split()))

print(knapsack_WR(W, weights))
