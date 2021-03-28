# Uses python3
# KNAPSACK
# Returns the minimum number of coins to change
# an amount of money X into coins of 1,5,10


def knapsack(n, W, v, w):
    # n: number of items; W: capacity of the knapsack
    # v: vector of item values, w: vector of item weights
    unit_values = []  #
    knapsack_value = 0  # total value inside the knapsack (output)
    knapsack_weights = []  # list, stores the weights of every added item

    # 1st for loop to create the values
    for i in range(0, n):
        ith_value = v[i]/w[i]
        unit_values.append(ith_value)
    # 2nd for loop to fill the knapsack
    for j in range(0, n):
        if W == 0:
            return knapsack_value
        # locating the index of the maximum value, defined as v[i]/w[i]
        max_value = max(unit_values)
        index = unit_values.index(max_value)

        if w[index] > 0:
            # if w[index] is smallest then take all
            # if W is smallest then cut a to fit in exactly W's capacity
            a = min(w[index], W)

            # consequences of filling out the knapsack
            knapsack_value += a * max_value
            knapsack_weights.append(a)
            w[index] -= a
            W -= a  # knapsack capacity reduced by amount put in

        else:
            unit_values[index] = 0

    return knapsack_value

# INPUT
n, W = map(int, input().split())
v = []  # Vector of values
w = []  # Vector of weights

for k in range(0, n):  # remember that range(0,10) is equal to [0,10 - 1 = 9]
    x, y = map(int, input().split())
    v.append(x)
    w.append(y)

print(knapsack(n, W, v, w))
