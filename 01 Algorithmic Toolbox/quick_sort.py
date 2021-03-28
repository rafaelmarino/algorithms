# Uses python3
import random
import numpy

def partition3(a, l, r):
    x = a[l]
    j = l
    w = 0  # this counter should be reset for each loop
    for i in range(l + 1, r + 1):  # remember that range(x,y) = [x,y)
        if a[i] == x:
            j += 1
            w += 1
            a[i], a[j] = a[j], a[i]

        elif a[i] < x:
            j += 1
            a[i], a[j] = a[j], a[i]  # swaps the jth for the ith
            a[j], a[j-w] = a[j-w], a[j]

    a[l], a[j-w] = a[j-w], a[l]
    return [j-w, j]
# def partition2(a, l, r):
#     x = a[l]
#     j = l
#     for i in range(l + 1, r + 1):  # remember that range(x,y) = [x,y)
#         if a[i] <= x:
#             j += 1
#             a[i], a[j] = a[j], a[i]
#     a[l], a[j] = a[j], a[l]  # the final step is to swap the pivot for the final <=x element
#     return j

def randomized_quick_sort(a, l, r):
    # a = list; l = leftmost index; r = rightmost index
    if l >= r:
        return
    k = random.randint(l, r)
    a[l], a[k] = a[k], a[l]
    # use partition3
    m = partition3(a, l, r)  # partition3() returns two indices for m1 and m2 (m1==m2)
    randomized_quick_sort(a, l, m[0] - 1)  # m is left out of the interval
    randomized_quick_sort(a, m[1] + 1, r)  # m is left out of the interval

# INPUT
n = int(input())

# a = random.sample(range(50), n)  # ONLY UNIQUES
a = numpy.random.choice(50, n)  # UNIQUES AND DUPLICATES
# a = list(map(int, input().split()))  # KEEP FOR SUBMISSION

print(a)

randomized_quick_sort(a, 0, n - 1)
for x in a:
    print(x, end=' ')
