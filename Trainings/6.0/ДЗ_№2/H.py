n = int(input())
a = list(map(int, input().split(" ")))

prefix_sum = [0] * (n+1)
total_cost = 0
for i in range(1, n+1):
    prefix_sum[i] = prefix_sum[i - 1] + a[i - 1]
    total_cost += a[i-1] * (i-1)

min_cost = total_cost
for k in range(1, n):
    total_cost += prefix_sum[k] - (prefix_sum[n] - prefix_sum[k])
    min_cost = min(min_cost, total_cost)
print(min_cost)
