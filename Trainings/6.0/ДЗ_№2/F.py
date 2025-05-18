n = int(input())
a = list(map(int, input().split(" ")))
prefix_sum = [0] * (n + 1)
for i in range(1, n+1):
    prefix_sum[i] = prefix_sum[i-1] + a[i-1]
res = 0
for i in range(1, n - 1):
    print(a[i], prefix_sum[i], prefix_sum[n],  prefix_sum[i+1])
    res += a[i] * prefix_sum[i] * (prefix_sum[n] - prefix_sum[i+1])
print(res % 1000000007)
