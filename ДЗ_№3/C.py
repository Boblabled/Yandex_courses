n, k = map(int, input().split())
a = list(map(int, input().split()))
ans = [0] * (n - k + 1)
stack = []
r = 0
for l in range(n - k + 1):
    while r - l < k:
        while len(stack) != 0 and stack[-1][1] > a[r]:
            stack.pop()
        stack.append((r, a[r]))
        r += 1
    while len(stack) != 0 and stack[0][0] < l:
        stack.pop(0)
    ans[l] = stack[0][1]
print(*ans)
