# python3

import sys, threading
sys.setrecursionlimit(10**6)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class TreeOrders:
    def read(self):
        self.n = int(int(input()))
        self.key = [0 for i in range(self.n)]
        self.left = [0 for i in range(self.n)]
        self.right = [0 for i in range(self.n)]
        for i in range(self.n):
            [a, b, c] = map(int, input().split())
            self.key[i] = a
            self.left[i] = b
            self.right[i] = c

    def inOrder(self):
        # LEFT CHILDREN CALLS, PRINT, RIGHT CHILDREN CALLS
        self.result = []
        # inOrder traversal returns an ordered list on a BST
        # IOT is equivalent to printing the Next(x) element recursively
        def inOrder_recursive(root):
            if self.left[root] != -1:
                # if there is a valid left child then do a call
                inOrder_recursive(self.left[root])
            self.result.append(self.key[root])
            if self.right[root] != -1:
                inOrder_recursive(self.right[root])

            return self.result

        return inOrder_recursive(0)

    def preOrder(self):
        # PRINT, LEFT CHILDREN CALLS, RIGHT CHILDREN CALLS
        self.result = []
        # Finish the implementation
        # You may need to add a new recursive method to do that
        def preOrder_recursive(root):
            self.result.append(self.key[root])
            if self.left[root] != -1:
                preOrder_recursive(self.left[root])
            if self.right[root] != -1:
                preOrder_recursive(self.right[root])

            return self.result

        return preOrder_recursive(0)

    def postOrder(self):
        self.result = []

        def postOrder_recursive(root):
            if self.left[root] != -1:
                postOrder_recursive(self.left[root])
            if self.right[root] != -1:
                postOrder_recursive(self.right[root])
            self.result.append(self.key[root])

            return self.result

        return postOrder_recursive(0)

def main():
    # the original exercise prints all three types of traversals
    tree = TreeOrders()
    tree.read()
    print(" ".join(str(x) for x in tree.inOrder()))
    # print(" ".join(str(x) for x in tree.preOrder()))
    # print(" ".join(str(x) for x in tree.postOrder()))

threading.Thread(target=main).start()
