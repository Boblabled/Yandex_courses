n, c = map(int, input().split(" "))
s = input()
max_length = 0
r = 0
count_a = 0
count_b = 0
error = 0
for l in range(n):
    while error <= c and r < n:
        if s[r] == 'a':
            count_a += 1
        elif s[r] == 'b':
            count_b += 1
            error += count_a
        if error <= c:
            max_length = max(max_length, r - l + 1)
        r += 1

    if s[l] == 'a':
        count_a -= 1
        error -= count_b
    elif s[l] == 'b':
        count_b -= 1
print(max_length)
