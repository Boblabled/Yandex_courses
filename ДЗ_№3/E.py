def parse_infix_in_postfix(expr: str) -> str:
    global operators
    stack = []
    postfix = ""
    for s in expr.split():
        if s not in operators and s not in brackets:
            postfix += " " + s
        else:
            if s == "*":
                while len(stack) != 0 and stack[-1] == "*":
                    postfix += " " + stack.pop()
                stack.append(s)
            elif s == "+" or s == "-":
                while len(stack) != 0 and stack[-1] != "(":
                    postfix += " " + stack.pop()
                stack.append(s)
            elif s == ")":
                while len(stack) != 0 and stack[-1] != "(":
                    postfix += " " + stack.pop()
                stack.pop()
            else:
                stack.append(s)
    while len(stack) != 0:
        postfix += " " + stack.pop()
    return postfix


def count_postfix_expression(expr: str) -> int:
    global operators
    stack = []
    for s in expr.split():
        if s not in operators:
            stack.append(int(s))
        else:
            a1 = stack.pop()
            a2 = stack.pop()
            if s == "+":
                stack.append(a1 + a2)
            elif s == "-":
                stack.append(a2 - a1)
            else:
                stack.append(a1 * a2)
    return stack.pop()


operators = {"*", "+", "-"}
brackets = {"(", ")"}
count_brackets = 0
expression = " "
last_s = " "
res = ""
operator_last = False
for s in input():
    if s.isdigit() and last_s == " " and expression[-1].isdigit():
        res = "WRONG"
        break
    elif s == "-" and (expression[-1] in operators or expression[-1] == " "):
        operator_last = True
        expression += " 0 " + s
    elif s in operators and not expression[-1].isdigit() and expression[-1] != ")":
        res = "WRONG"
        break
    elif s not in operators and s not in brackets and not s.isdigit() and s != " ":
        res = "WRONG"
        break
    elif s == "(":
        if expression[-1].isdigit():
            res = "WRONG"
            break
        expression += " " + s
        count_brackets += 1
    elif s == ")":
        if count_brackets == 0 or expression[-1] in operators:
            res = "WRONG"
            break
        count_brackets -= 1
        expression += " " + s
    elif s == " ":
        pass
    elif expression[-1].isdigit() and s.isdigit():
        operator_last = False
        expression += s
    else:
        if s in operators:
            operator_last = True
        else:
            operator_last = False
        expression += " " + s
    last_s = s

if count_brackets != 0 or operator_last:
    res = "WRONG"

if res != "WRONG":
    postfix = parse_infix_in_postfix(expression)
    if len(postfix) == 0:
        res = "WRONG"
    else:
        res = count_postfix_expression(postfix)
print(res)
