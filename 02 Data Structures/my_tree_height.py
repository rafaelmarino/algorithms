# python3

import sys, threading
sys.setrecursionlimit(10**7)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size

class Tree:
    def __init__(self, key):
        self.key = key
        self.children = []

    def addChildren(self, obj):
        self.children.append(obj)

    def getKey(self):
        return self.key

    def getHeight(self):
        if not self.children:
            return 1
        else:
            maxC = []
            for x in range(0, len(self.children)):
                maxC.append(self.children[x].getHeight())
            return 1 + max(maxC)

class TreeHeight:
        def read(self):
            self.n = int(sys.stdin.readline())
            self.parent = list(map(int, sys.stdin.readline().split()))

        def createTree(self):
            nodes = []
            for i in range(0, self.n):
                t = Tree(i)
                nodes.append(t)
            for j in range(0, self.n):
                if self.parent[j] == -1:
                    root = nodes[j]
                else:
                    nodes[self.parent[j]].addChildren(nodes[j])

            print(root.getHeight())

def main():
  tree = TreeHeight()
  tree.read()
  tree.createTree()

threading.Thread(target=main).start()