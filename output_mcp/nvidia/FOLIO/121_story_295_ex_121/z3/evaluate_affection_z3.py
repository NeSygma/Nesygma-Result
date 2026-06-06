from z3 import *

solver = Solver()

# Declare boolean variables for two individuals
A = [Bool(f'A{i}') for i in range(2)]
L = [Bool(f'L{i}') for i in range(2)]
P = [Bool(f'P{i}') for i in range(2)]

# Some affection is love: exists i (A_i ∧ L_i)
solver.add(Or(And(A[0], L[0]), And(A[1], L[1])))

# Some love is positive: exists i (L_i ∧ P_i)
solver.add(Or(And(L[0], P[0]), And(L[1], P[1])))

# No affection is positive: forall i, not (A_i ∧ P_i)
solver.add(And(Not(And(A[0], P[0])), Not(And(A[1], P[1]))))

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: unknown")
    # Print the values of A, L, P for each individual
    for i in range(2):
        print(f"A{i}={model[A[i]].as_long()}, L{i}={model[L[i]].as_long()}, P{i}={model[P[i]].as_long()}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")