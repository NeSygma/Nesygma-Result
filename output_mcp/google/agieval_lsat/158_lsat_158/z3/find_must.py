from z3 import *

A = [Int(f'A_{i}') for i in range(6)]
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

solver = Solver()
for i in range(6):
    solver.add(A[i] >= 0, A[i] <= 2)

solver.add(Sum([If(A[i] == 1, 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(A[i] == 2, 1, 0) for i in range(6)]) >= 2)
solver.add(A[0] == A[2])
solver.add(Implies(And(A[4] != 0, A[5] != 0), A[4] != A[5]))
solver.add(Implies(A[1] == 1, A[4] == 2))
solver.add(Implies(A[3] != 2, And(A[2] == 2, A[5] == 2)))

# Find all photographers who MUST be assigned
must_assigned = []
for i in range(6):
    s = Solver()
    s.add(solver.assertions())
    s.add(A[i] == 0)
    if s.check() == unsat:
        must_assigned.append(names[i])

print(f"Must assigned: {must_assigned}")