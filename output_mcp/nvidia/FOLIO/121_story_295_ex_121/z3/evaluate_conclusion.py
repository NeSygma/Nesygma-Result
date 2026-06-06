from z3 import *

# Finite domain of 2 individuals
N = 2
A = [Bool(f'A{i}') for i in range(N)]
L = [Bool(f'L{i}') for i in range(N)]
P = [Bool(f'P{i}') for i in range(N)]

# Premise 1: Some affection is love
premise1 = Or(And(A[0], L[0]), And(A[1], L[1]))

# Premise 2: Some love is positive
premise2 = Or(And(L[0], P[0]), And(L[1], P[1]))

# Conclusion: Some affection is positive
conclusion = Or(And(A[0], P[0]), And(A[1], P[1]))

# Check if premises can be true while conclusion is false
solver = Solver()
solver.add(premise1)
solver.add(premise2)
solver.add(Not(conclusion))

result = solver.check()

if result == sat:
    # Model exists where premises hold but conclusion does NOT hold
    print("STATUS: unknown")
    model = solver.model()
    # Print the assignment for clarity (optional but helpful)
    for i in range(N):
        print(f"A{i}={model[A[i]].as_long()}, L{i}={model[L[i]].as_long()}, P{i}={model[P[i]].as_long()}")
else:
    # This branch would be taken if the conclusion were entailed (unlikely)
    print("STATUS: proved")