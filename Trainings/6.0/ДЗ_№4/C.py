import sys
sys.setrecursionlimit(100000)

def generate_tree(child, root, nodes, tree, h):
    tree[child] = (root, h)
    if child in nodes:
        for node in nodes[child]:
            generate_tree(node, child, nodes, tree, h+1)

def find_lca(el1, el2, tree):
    a1, h1 = tree[el1]
    a2, h2 = tree[el2]
    if el1 == el2:
        return el1
    elif el1 == a2:
        return el1
    elif el2 == a1:
        return el2
    if h1 == h2:
        if a1 == a2:
            return a1
        else:
            return find_lca(a1, a2, tree)
    elif h1 > h2:
        return find_lca(a1, el2, tree)
    else:
        return find_lca(el1, a2, tree)


input_data = []
with open("input.txt", "r") as in_file:
    for line in in_file:
        input_data.append(line.strip())
N = int(input_data[0])
nodes = {}
parents = set()
children = set()
for i in range(1, N):
    child, parent = input_data[i].split(" ")
    parents.add(parent)
    children.add(child)
    if parent not in nodes:
        nodes[parent] = []
    nodes[parent].append(child)
root = parents.difference(children).pop()
tree = {}
generate_tree(root, None, nodes, tree, 0)

for i in range(N, len(input_data)):
    element_1, element_2 = input_data[i].split(" ")
    print(find_lca(element_1, element_2, tree))
  
