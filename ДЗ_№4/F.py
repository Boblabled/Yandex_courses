import sys
sys.setrecursionlimit(1000000)


def generate_tree(root, nodes, ans):
    if root in nodes:
        children = len(nodes[root])
        for node in nodes[root]:
            money, c = generate_tree(node, nodes, ans)
            children += c
            ans[root-1] += money
        return ans[root-1] + children + 1, children
    else:
        return 2, 0


n = int(input())
nodes = {}
for i, a in enumerate(map(int, input().split())):
    if a not in nodes:
        nodes[a] = []
    nodes[a].append(i + 2)

ans = [1] * n
generate_tree(1, nodes, ans)
print(*ans)
