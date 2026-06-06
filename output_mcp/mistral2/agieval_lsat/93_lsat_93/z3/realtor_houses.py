from z3 import *

solver = Solver()

# Declare the houses as symbolic integers representing their positions (1 to 7)
houses = [Int(f'house_{i}') for i in range(7)]

# Each house must be assigned a unique position from 1 to 7
solver.add(Distinct(houses))
for i in range(7):
    solver.add(houses[i] >= 1, houses[i] <= 7)

# Assign letters to houses for clarity
J, K, L, M, N, O, P = houses

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(J == 6, J == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(K == 1, K == 2)))

# Rule 3: L must be shown after K and before M
# This means K < L < M in terms of positions
solver.add(K < L, L < M)

# Morning: positions 1 and 2
morning = [houses[0], houses[1]]
# Afternoon: positions 3, 4, 5
afternoon = [houses[2], houses[3], houses[4]]
# Evening: positions 6 and 7

# Base constraints are now set. Now evaluate each option.

# Define the options as constraints on the order of houses
# Option A: K, O, L, M, N, J, P
opt_a_constr = And(
    K == 1, O == 2, L == 3, M == 4, N == 5, J == 6, P == 7
)

# Option B: N, L, P, K, M, O, J
opt_b_constr = And(
    N == 1, L == 2, P == 3, K == 4, M == 5, O == 6, J == 7
)

# Option C: O, P, K, L, N, M, J
opt_c_constr = And(
    O == 1, P == 2, K == 3, L == 4, N == 5, M == 6, J == 7
)

# Option D: O, P, M, N, K, L, J
opt_d_constr = And(
    O == 1, P == 2, M == 3, N == 4, K == 5, L == 6, J == 7
)

# Option E: P, O, K, J, L, N, M
opt_e_constr = And(
    P == 1, O == 2, K == 3, J == 4, L == 5, N == 6, M == 7
)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")