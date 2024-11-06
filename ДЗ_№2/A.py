n = int(input())
a = list(map(int, input().split(" ")))
prefix = [0] * n
for i in range(n):
    if i == 0:
        prefix[i] = a[0]
    else:
        prefix[i] = prefix[i-1] + a[i]
print(" ".join(map(str, prefix)))
