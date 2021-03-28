#!/usr/bin/python3

import sys, threading

sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


def IsBinarySearchTree(tree):
  # Implement correct algorithm here
  # inOrder traversal returns an ordered list on a BST
  # check after every append if n > n+1 return False

  result = []
  def inOrder_recursive(root):
      if tree[root][1] != -1:
          # if there is a valid left child then do a call
          inOrder_recursive(tree[root][1])
      result.append(tree[root][0])
      if tree[root][2] != -1:
          inOrder_recursive(tree[root][2])
      return result

  # in-place function call
  inOrder_recursive(0)

  check_value = True
  for i in range(len(result)-1):
    if result[i] > result[i+1]:
      check_value = False
      break

  return check_value

def main():
  nodes = int(input().strip())  # number of nodes, strip white spaces
  tree = []
  for i in range(nodes):
    tree.append(list(map(int, input().strip().split())))
  if nodes == 0 or IsBinarySearchTree(tree):
    print("CORRECT")
  else:
    print("INCORRECT")

threading.Thread(target=main).start()
