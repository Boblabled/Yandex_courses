import sys
sys.setrecursionlimit(100000)

def generate_tree(root, nodes, root_set, ans):
    ans[root-1] = 1
    root_set.add(root)
    if root in nodes:
        for node in nodes[root]:
            if node not in root_set:
                ans[root-1] += generate_tree(node, nodes, root_set, ans)
    return ans[root-1]


v = int(input())
nodes = {}
for i in range(v-1):
    a, b = map(int, input().split())
    if a not in nodes:
        nodes[a] = []
    if b not in nodes:
        nodes[b] = []
    nodes[a].append(b)
    nodes[b].append(a)
ans = [1] * v
root_set = {1}
generate_tree(1, nodes, root_set, ans)
print(*ans)
