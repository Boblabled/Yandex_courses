n = int(input())
a = sorted(list(map(int, input().split(" "))))
ans = [0] * n
test = list()
l, r = n // 2, n // 2
if l == r:
    l -= 1
for i in range(n):
    if (n - l - 1) <= r:
        test.append(l)
        ans[i] = a[l]
        l -= 1
    else:
        test.append(r)
        ans[i] = a[r]
        r += 1
print(" ".join(map(str, ans)))
