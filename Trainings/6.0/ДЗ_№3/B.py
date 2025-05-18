n = int(input())
a = list(map(int, input().split()))
stack = [(0, a[0])]
ans =[-1] * n
for i in range(1, n):
    while len(stack) != 0 and stack[-1][1] > a[i]:
        ans[(stack.pop())[0]] = i
    stack.append((i, a[i]))
print(*ans)
