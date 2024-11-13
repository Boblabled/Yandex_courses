def get_right(d: int):
    return (d + 3) % 5 + (d + 3) // 5


def get_left(d: int):
    return (d + 1) % 5 + (d + 1) // 5


n = int(input())
a, b = map(int, input().split())

d_priors = []
if abs(a-b) == 2:
    d_priors.append((a, b))
    d_priors.append((get_right(a), get_right(b)))
else:
    if b == get_right(a):
        main_d = b
    else:
        main_d = a
    d_priors = [(main_d,)]
    for i in range(1, 4):
        d_priors.append((get_left(d_priors[i - 1][0]),))

rovers = []
for i in range(n):
    d, t = map(int, input().split())
    rovers.append((i, d, t))

rovers.sort(key=lambda x: x[2])

stack = {i: [] for i in range(1, 5)}
for i, d, t in rovers:
    stack[d].append((i, t))

ans = [0] * n
time = 1
while n != 0:
    for ds in d_priors:
        time_changed = False
        for d in ds:
            if len(stack[d]) != 0 and stack[d][0][1] <= time:
                ans[stack[d].pop(0)[0]] = time
                n -= 1
                time_changed = True
        if time_changed:
            break
    time += 1

for a in ans:
    print(a)
