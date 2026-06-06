from z3 import *

# Photographers: 0:F, 1:G, 2:H, 3:K, 4:L, 5:M
# Assignment: 0:None, 1:Silva, 2:Thorne
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

all_models = []
s = Solver()
s.add(solver.assertions())

while s.check() == sat:
    m = s.model()
    model_assignment = [m.evaluate(A[i]).as_long() for i in range(6)]
    all_models.append(model_assignment)
    s.add(Or([A[i] != model_assignment[i] for i in range(6)]))

print(f"Number of models: {len(all_models)}")
for m in all_models:
    print(m)

must_assigned = []
for i in range(6):
    is_always_assigned = True
    for m in all_models:
        if m[i] == 0:
            is_always_assigned = False
            break
    if is_always_assigned:
        must_assigned.append(names[i])

print(f"Must assigned: {must_assigned}")