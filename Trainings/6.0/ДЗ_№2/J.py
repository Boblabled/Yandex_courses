n = int(input())
a = list(map(int, input().split()))
m, k = map(int, input().split())
x = list(map(int, input().split()))

l = 0
stops = [0] * n
count = 0
for r in range(1, n):
    if a[r - 1] > a[r]:
        l = r
        count = 0
    elif a[r-1] == a[r]:
        if count < k:
            count += 1
        else:
            while count >= k:
                if a[l] == a[l+1]:
                    count -= 1
                l += 1
            count += 1
    stops[r] = l

ans = [0] * m
for i in range(m):
    ans[i] = stops[x[i] - 1] + 1
print(" ".join(map(str, ans)))
