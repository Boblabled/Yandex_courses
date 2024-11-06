N, R = map(int, input().split(" "))
D = list(map(int, input().split(" ")))
ans = 0
l = 0
for i in range(N):
    while D[i] - D[l] > R and l < i:
        l += 1
    ans += l
print(ans)
