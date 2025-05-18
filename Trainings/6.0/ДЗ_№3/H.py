def add(x: int):
    global stack
    global prefix_sum
    stack.append(x)
    prefix_sum.append(x + prefix_sum[-1])


def pop():
    global stack
    prefix_sum.pop()
    print(stack.pop())


def count_sum(k: int):
    global stack
    print(prefix_sum[-1] - prefix_sum[-(k + 1)])


stack = []
prefix_sum = [0]
for i in range(int(input())):
    operation = input()
    if operation[0] == "+":
        add(int(operation[1:]))
    elif operation[0] == "-":
        pop()
    elif operation[0] == "?":
        count_sum(int(operation[1:]))
