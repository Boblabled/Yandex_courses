n = int(input())
x1, x2 = None, None
y1, y2 = None, None
rows = []
for y in range(n):
    row = input()
    for x, s in enumerate(row):
        if s == "#":
            if x1 is not None:
                x1 = min(x1, x)
                x2 = max(x2, x + 1)
                y1 = min(y1, n - y - 1)
                y2 = max(y2, n - y)
            else:
                x1, x2 = x, x+1
                y1, y2 = n - y - 1, n - y
    rows.append(row)
inner_rects = []
inner_rows = []
if x1 is not None:
    for y in range(n - y2, n - y1):
        row = []
        for x, s in enumerate(rows[y][x1:x2]):
            if s == ".":
                if len(row) != 0:
                    row[1] = x1 + x + 1
                else:
                    row = [x1 + x, x1 + x + 1]
            else:
                if len(row) != 0:
                    inner_rows.append(row.copy())
                row = []
        if len(row) != 0:
            inner_rows.append(row.copy())
        for row in inner_rows:
            added = False
            for rect in inner_rects:
                if row[0] == rect["x"][0] and row[1] == rect["x"][1] and rect["y"][0] - (n - y - 1) <= 1:
                    rect["y"][0] = n - y - 1
                    added = True
            if not added:
                inner_rects.append({"x": row, "y": [n - y - 1, n - y]})
        inner_rows.clear()
    if len(inner_rects) == 0:
        print("I")
    elif len(inner_rects) == 1:
        x3, x4 = inner_rects[0]["x"][0], inner_rects[0]["x"][1]
        y3, y4 = inner_rects[0]["y"][0], inner_rects[0]["y"][1]
        if x1 < x3 < x4 < x2 and y1 < y3 < y4 < y2:
            print("O")
        elif x1 < x3 < x4 == x2 and y1 < y3 < y4 < y2:
            print("C")
        elif x1 < x3 < x4 == x2 and y1 < y3 < y4 == y2:
            print("L")
        else:
            print("X")
    elif len(inner_rects) == 2:
        inner_rects.sort(key=lambda r: r["y"][0])
        x3, x4 = inner_rects[0]["x"][0], inner_rects[0]["x"][1]
        y3, y4 = inner_rects[0]["y"][0], inner_rects[0]["y"][1]
        x5, x6 = inner_rects[1]["x"][0], inner_rects[1]["x"][1]
        y5, y6 = inner_rects[1]["y"][0], inner_rects[1]["y"][1]
        if x1 < x3 == x5 < x4 == x6 < x2 and y1 == y3 < y4 < y5 < y6 == y2:
            print("H")
        elif x1 < x3 == x5 < x6 < x4 == x2 and y1 == y3 < y4 < y5 < y6 < y2:
            print("P")
        else:
            print("X")
    else:
        print("X")
else:
    print("X")
