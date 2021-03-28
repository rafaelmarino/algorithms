# python3


class HeapBuilder:
    def __init__(self):
        self._swaps = []
        self._data = []

    def ReadData(self):
        self.n = int(input())
        self._data = [int(s) for s in input().split()]
        assert self.n == len(self._data)  # if True continues, if Error stops, 1BI

    def WriteResponse(self):
        print(len(self._swaps))
        for swap in self._swaps:
          print(swap[0], swap[1])  # the two elements of the tuple
        # print(self._data)

    def GenerateSwaps(self):
        m = (self.n - 1) // 2  # parent of last node in 0BI, int
        for i in range(m, -1, -1):
            self.siftDown(i)

    def siftDown(self, i):
        # Implementing SiftDown(i) from the lectures:
        min_index = i
        l = 2*i + 1  # left child 0BI
        if l <= self.n - 1 and self._data[l] < self._data[min_index]:
            min_index = l
        r = 2*i + 2  # right child 0BI
        if r <= self.n - 1 and self._data[r] < self._data[min_index]:
            min_index = r
        if i != min_index:
            self._swaps.append((i, min_index))  # storing swap in a tuple
            self._data[i], self._data[min_index] = self._data[min_index], self._data[i]
            # if swapped, the key of interest is now located at min_index
            # so we call siftDown again in min_index recursively
            self.siftDown(min_index)

    def Solve(self):
        self.ReadData()
        self.GenerateSwaps()
        self.WriteResponse()

if __name__ == '__main__':
    heap_builder = HeapBuilder()
    heap_builder.Solve()
