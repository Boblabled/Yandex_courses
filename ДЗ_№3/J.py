n, H = map(int, input().split())
h = list(map(int, input().split()))
w = list(map(int, input().split()))
chairs = []

for i in range(n):
    chairs.append((h[i], w[i]))
chairs.sort(key=lambda x: x[0], reverse=True)

ans = 10**9
current_w = 0
deque = []
r = 0
for l in range(n):
    while current_w < H and r < n:
        current_w += chairs[r][1]
        if l != r:
            dist = chairs[r-1][0] - chairs[r][0]
            while len(deque) != 0 and deque[-1][1] <= dist:
                deque.pop()
            deque.append((r-1, dist))
        else:
            deque.append((r, 0))
        r += 1
    if len(deque) != 0 and current_w >= H:
        ans = min(ans, deque[0][1])
    else:
        break

    while len(deque) != 0 and deque[0][0] == l:
        deque.pop(0)
    current_w -= chairs[l][1]

print(ans)
