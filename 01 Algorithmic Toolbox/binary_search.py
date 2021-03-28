# Uses python3
# BINARY SEARCH
# Cuts the list in half to look for a key in an ordered list
# PEMDAS: Parenthesis, Exponents, Multiplication & Division, Addition & Subtraction


def binary_search(my_list, low_index, high_index, key):

        if high_index < low_index:
            return -1
        mid_index = low_index + (high_index - low_index) // 2  #

        if key == my_list[mid_index]:
            return mid_index
        elif key < my_list[mid_index]:
            return binary_search(my_list, low_index, mid_index - 1, key)
        # the new high is mid_index - 1 because mid was already checked
        else:
            return binary_search(my_list, mid_index + 1, high_index, key)

# # INPUT
# n, the first element of the list is the length of the rest of the list
a = [int(x) for x in input().split()]
my_list = a[1:]
# remember to transform from natural indices to Python indices, subtracting 1
low_index, high_index = 0, len(my_list) - 1

# k, the first element of the list is the length of the rest of the list
keys = [int(x) for x in input().split()]

key_positions = []
result = 0
for i in range(1, len(keys)):  # range works like this: [), no need to subtract 1
    key = keys[i]
    result = binary_search(my_list, low_index, high_index, key)
    key_positions.append(result)

print(' '.join(str(x) for x in key_positions))
