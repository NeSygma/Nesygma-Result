from z3 import *

solver = Solver()

# Booleans for each position
is_A = [Bool(f"is_A_{i}") for i in range(6)]
is_B = [Bool(f"is_B_{i}") for i in range(6)]
is_C = [Bool(f"is_C_{i}") for i in range(6)]

# Exactly one type per position
for i in range(6):
    solver.add(is_A[i] + is_B[i] + is_C[i] == 1)

# Global counts
solver.add(Sum(is_A) == 1)
solver.add(Sum(is_B) == 2)
solver.add(Sum(is_C) == 3)

# Option presence Booleans
has_opt1 = [Bool(f"has_opt1_{i}") for i in range(6)]
for i in range(6):
    solver.add(has_opt1[i] == Or(is_A[i], is_C[i]))

# Sliding windows of size 3 for option 1
for i in range(0, 4):  # 0..3
    solver.add(Sum([has_opt1[i], has_opt1[i+1], has_opt1[i+2]]) <= 2)

# Sliding windows of size 2 for option 2
for i in range(0, 5):  # 0..4
    solver.add(Sum([is_A[i], is_A[i+1]]) <= 1)

# Sliding windows of size 2 for option 3
for i in range(0, 5):
    solver.add(Sum([is_B[i], is_B[i+1]]) <= 1)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    seq = []
    for i in range(6):
        if model[is_A[i]]: seq.append("A")
        elif model[is_B[i]]: seq.append("B")
        elif model[is_C[i]]: seq.append("C")
    print("STATUS: sat")
    print("sequence:", " ".join(seq))
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")