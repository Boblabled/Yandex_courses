stack = []
operators = {"*", "+", "-"}
for s in input().split():
    if s not in operators:
        stack.append(int(s))
    else:
        a1 = stack.pop()
        a2 = stack.pop()
        if s == "+":
            stack.append(a1+a2)
        elif s == "-":
            stack.append(a2-a1)
        else:
            stack.append(a1*a2)
print(stack.pop())



