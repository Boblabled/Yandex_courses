A, B, C, D = [int(input()) for _ in range(4)]
M = [B+1, A+1, max(A, B) + 1, 1]
N = [D+1, C+1, 1, max(C, D) + 1]

if A == 0 or C == 0:
    print(M[1], N[1])
elif B == 0 or D == 0:
    print(M[0], N[0])
else:
    k = 0
    min_sum = M[k] + N[k]
    for i in range(k+1, len(M)):
        if M[i] + N[i] < min_sum:
            min_sum = M[i] + N[i]
            k = i
    print(M[k], N[k])
