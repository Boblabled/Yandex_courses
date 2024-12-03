import sys
sys.setrecursionlimit(100000)


def read_data(filename):
    data = []
    with open(filename, "r") as in_file:
        for line in in_file:
            data.append(line.strip())
    return data


def add(tree, arg):
    if len(tree) == 0:
        tree.append(arg)
        tree.append([[], []])
        return "DONE"
    elif arg > tree[0]:
        return add(tree[1][1], arg)
    elif arg < tree[0]:
        return add(tree[1][0], arg)
    else:
        return "ALREADY"


def search(tree, arg):
    if len(tree) == 0:
        return "NO"
    if arg > tree[0]:
        return search(tree[1][1], arg)
    elif arg < tree[0]:
        return search(tree[1][0], arg)
    else:
        return "YES"


def print_tree(tree, h):
    if len(tree) != 0:
        print_tree(tree[1][0], h+1)
        print("." * h, tree[0], sep="")
        print_tree(tree[1][1], h + 1)


input_data = read_data("input.txt")
tree = []
for command in input_data:
    cmd = command.split(" ")
    if cmd[0] == "ADD":
        print(add(tree, int(cmd[1])))
    elif cmd[0] == "SEARCH":
        print(search(tree, int(cmd[1])))
    else:
        print_tree(tree, 0)
