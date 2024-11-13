stack = []
pairs = {")": "(", "]": "[", "}": "{"}
ans = "yes"
for s in input():
    if s not in pairs:
        stack.append(s)
    else:
        if len(stack) == 0 or pairs[s] != stack.pop():
            ans = "no"
            break
if len(stack) != 0:
    ans = "no"
print(ans)
