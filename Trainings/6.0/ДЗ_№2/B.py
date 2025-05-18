N, K = map(int, input().split(" "))
m = list(map(int, input().split(" ")))
l, r = 0, 0
current_sum = 0
ans = 0
while l < N:
    while current_sum <= K and r < N:
        current_sum += m[r]
        if current_sum == K:
            ans += 1
        r += 1
    current_sum -= m[l]
    if current_sum == K:
        ans += 1
    l += 1
print(ans)

# Через префиксные суммы
# N, K = map(int, input().split(" "))
# m = list(map(int, input().split(" ")))
# current_sum = 0
# sum_dict = {0: 1}
# ans = 0
# for i in m:
#     current_sum += i
#     ans += sum_dict.get(current_sum - K, 0)
#     sum_dict[current_sum] = sum_dict.get(current_sum, 0) + 1
# print(ans)
