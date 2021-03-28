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
      result.append(tree[root])
      if tree[root][2] != -1:
          inOrder_recursive(tree[root][2])
      return [i[0] for i in result]

  # in-place function call
  inOrder_recursive(0)

  check_value = True
  for i in range(1,len(result)):
    if result[i-1][0] > result[i][0]:
      check_value = False
      break

  def LC_Keys():
      lc_keys = []
      raw_left_indices = [i[1] for i in tree]
      for i in raw_left_indices:
          if i != -1:
              lc_keys.append(tree[i][0])
      return lc_keys

  if len(LC_Keys()) >=1 and max(LC_Keys()) == tree[0][0]:
      check_value = False

  return check_value
def IsBinarySearchTreeFast(tree):

    # lc_indices = [i[1] for i in tree]
    # for i in lc_indices:
    #     if i != -1:
    #         tree[i].append('lc')  # append a left child marker

    # for i in range(len(tree)):
    #     # attaching node id
    #     tree[i].append(i)
    def check_violations(last_i):
        current_node_key = result[last_i][0]
        previous_node_key = result[last_i-1][0]
        if last_i == 0:
            return
        # condition 1
        if previous_node_key > current_node_key:
            return True
        # condition 2: if any element in left subtree is equal then false

        subtree_index = result[last_i][1]
        if subtree_index != -1:
            subtree = []
            InOrderTraversal(subtree_index, subtree)
            if len(subtree) >= 1 and max(subtree) == current_node_key:
                return True

    def InOrderTraversal(root,lst):
        if tree[root][1] != -1:
            # if there is a valid left child then do a call
            InOrderTraversal(tree[root][1],lst)
        lst.append(tree[root][0])  # only append keys
        if tree[root][2] != -1:
            InOrderTraversal(tree[root][2],lst)
        return

    def inOrder_recursive(root):
        if tree[root][1] != -1:
            # if there is a valid left child then do a call
            inOrder_recursive(tree[root][1])
        result.append(tree[root])
        if check_violations(len(result)-1):
            violation.append(True)
        if tree[root][2] != -1:
            inOrder_recursive(tree[root][2])
        return

    violation = []
    result = []  # result[] is an in-place array for the whole tree
    inOrder_recursive(0)

    return True if sum(violation) == 0 else False

def main():
  nodes = int(input().strip())  # number of nodes, strip white spaces
  tree = []
  for i in range(nodes):
    tree.append(list(map(int, input().strip().split())))
  if nodes == 0 or IsBinarySearchTreeFast(tree):
    print("CORRECT")
  else:
    print("INCORRECT")

threading.Thread(target=main).start()
