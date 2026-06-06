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

# Check each option
# Option is a list of photographers who MUST be assigned.
# This means:
# 1. For all models, these photographers are assigned (A[i] != 0).
# 2. For all other photographers, there exists a model where they are NOT assigned (A[i] == 0).

def check_option(must_list):
    # 1. All in must_list must be assigned in all models
    for p_idx in must_list:
        s = Solver()
        s.add(solver.assertions())
        s.add(A[p_idx] == 0)
        if s.check() == sat:
            return False
    
    # 2. All NOT in must_list must NOT be assigned in at least one model
    not_must_list = [i for i in range(6) if i not in must_list]
    for p_idx in not_must_list:
        s = Solver()
        s.add(solver.assertions())
        s.add(A[p_idx] != 0)
        # We need to check if there is a model where A[p_idx] == 0
        # Wait, this is not quite right.
        # The condition is: "there exists a model where A[p_idx] == 0"
        # Let's rephrase:
        # For each p_idx not in must_list, is it possible that A[p_idx] == 0?
        # Yes, if there exists a model where A[p_idx] == 0.
        s = Solver()
        s.add(solver.assertions())
        s.add(A[p_idx] != 0)
        # If this is UNSAT, then A[p_idx] MUST be assigned.
        if s.check() == unsat:
            return False
    return True

# Indices: 0:F, 1:G, 2:H, 3:K, 4:L, 5:M
options = {
    "A": [0, 2],
    "B": [0, 2, 3],
    "C": [0, 2, 3, 4],
    "D": [0, 1, 2],
    "E": [0, 1, 2, 5]
}

for letter, must_list in options.items():
    if check_option(must_list):
        print(f"Option {letter} is valid.")
    else:
        print(f"Option {letter} is invalid.")