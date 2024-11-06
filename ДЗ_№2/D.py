# N^2
# n, k = map(int, input().split(" "))
# a = sorted(list(map(int, input().split(" "))))
# ans = 0
# while len(a) != 0:
#     l, r = 0, 0
#     while r < len(a):
#         if a[r] - a[l] > k:
#             a.pop(l)
#             l = r - 1
#         else:
#             r += 1
#     a.pop(l)
#     ans += 1
# print(ans)

n, k = map(int, input().split())
a = sorted(list(map(int, input().split())))
l = 0
max_dist = 1
for r in range(1, n):
    while a[r] - a[l] > k:
        l += 1
    max_dist = max(max_dist, r - l + 1)
print(max_dist)
