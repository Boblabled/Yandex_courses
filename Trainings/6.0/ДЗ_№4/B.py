import sys
sys.setrecursionlimit(100000)


def generate_tree(ans, root, nodes, h):
    children = 0
    if root in nodes:
        for node in nodes[root]:
            children += generate_tree(ans, node, nodes, h+1) + 1
    ans[root] = children
    return children

N = int(input())
nodes = {}
parents = set()
children = set()
for i in range(N-1):
    child, parent = input().split(" ")
    parents.add(parent)
    children.add(child)
    if parent not in nodes:
        nodes[parent] = []
    nodes[parent].append(child)
root = parents.difference(children).pop()

ans = {}
generate_tree(ans, root, nodes, 0)
for key in sorted(ans):
    print(key, ans[key])
  
