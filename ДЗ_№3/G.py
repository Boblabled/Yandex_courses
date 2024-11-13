n, b = map(int, input().split())
a = list(map(int, input().split()))

queue = []
time = 0

for i in range(n):
    queue.append([i, a[i]])
    current_b = b
    while current_b != 0 and len(queue) != 0:
        if queue[0][1] <= current_b:
            minute, count = queue.pop(0)
            current_b -= count
            time += count * (i - minute + 1)
        else:
            time += current_b * (i - queue[0][0] + 1)
            queue[0][1] -= current_b
            current_b = 0

while len(queue) != 0:
    minute, count = queue.pop(0)
    time += count * (n - minute + 1)

print(time)
