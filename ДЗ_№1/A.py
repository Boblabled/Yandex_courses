x1, y1, x2, y2, x, y = [int(input()) for _ in range(6)]
ans = ""
if y < y1:
    ans = "S"
elif y > y2:
    ans = "N"
if x < x1:
    ans += "W"
elif x > x2:
    ans += "E"
print(ans)
