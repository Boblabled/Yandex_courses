n = int(input())
w = {k: v for v, k in enumerate(input())}
pairs = {"(": ")", "[": "]"}
stack = []
ans = input()
for s in ans:
    if s in pairs:
        stack.append(s)
    else:
        stack.pop()

extra_length = (n - len(ans) - len(stack)) // 2

while len(stack) != 0 or extra_length != 0:
    if len(stack) != 0 and (w[pairs[stack[-1]]] < w["("] and w[pairs[stack[-1]]] < w["["] or extra_length == 0):
        ans += pairs[stack.pop()]
    elif w["("] < w["["]:
        stack.append("(")
        ans += "("
        extra_length -= 1
    else:
        stack.append("[")
        ans += "["
        extra_length -= 1

print(ans)
