n =  int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
p = list(map(int, input().split())) # если 1 - выбираю из b

days = [[0, 0, 0]] * n
for i in range(n):
    days[i] = [i+1, a[i], b[i]]
a_days = sorted(days, key=lambda x: (x[1], x[2]), reverse=True)
b_days = sorted(days, key=lambda x: (x[2], x[1]), reverse=True)

a_ptr = 0
b_ptr = 0
ans = [0] * n
used_days = set()
for i in range(n):
    if p[i] == 1:
        while b_days[b_ptr][0] in used_days:
            b_ptr += 1
        ans[i] = b_days[b_ptr][0]
        used_days.add(b_days[b_ptr][0])
        b_ptr += 1
    else:
        while a_days[a_ptr][0] in used_days:
            a_ptr += 1
        ans[i] = a_days[a_ptr][0]
        used_days.add(a_days[a_ptr][0])
        a_ptr += 1
print(" ".join(map(str, ans)))
