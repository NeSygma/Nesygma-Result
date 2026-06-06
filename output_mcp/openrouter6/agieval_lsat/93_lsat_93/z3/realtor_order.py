from z3 import *

solver = Solver()

# Declare position variables for each house
pos_J = Int('pos_J')
pos_K = Int('pos_K')
pos_L = Int('pos_L')
pos_M = Int('pos_M')
pos_N = Int('pos_N')
pos_O = Int('pos_O')
pos_P = Int('pos_P')

# Base constraints: positions between 1 and 7
houses = [pos_J, pos_K, pos_L, pos_M, pos_N, pos_O, pos_P]
for h in houses:
    solver.add(h >= 1, h <= 7)

# All positions distinct
solver.add(Distinct(houses))

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(pos_J == 6, pos_J == 7))

# K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(pos_K == 1, pos_K == 2)))

# L must be shown after K and before M
solver.add(pos_L > pos_K)
solver.add(pos_L < pos_M)

# Now test each option
found_options = []

# Option A: K, O, L, M, N, J, P
opt_a_constr = And(
    pos_K == 1,
    pos_O == 2,
    pos_L == 3,
    pos_M == 4,
    pos_N == 5,
    pos_J == 6,
    pos_P == 7
)

# Option B: N, L, P, K, M, O, J
opt_b_constr = And(
    pos_N == 1,
    pos_L == 2,
    pos_P == 3,
    pos_K == 4,
    pos_M == 5,
    pos_O == 6,
    pos_J == 7
)

# Option C: O, P, K, L, N, M, J
opt_c_constr = And(
    pos_O == 1,
    pos_P == 2,
    pos_K == 3,
    pos_L == 4,
    pos_N == 5,
    pos_M == 6,
    pos_J == 7
)

# Option D: O, P, M, N, K, L, J
opt_d_constr = And(
    pos_O == 1,
    pos_P == 2,
    pos_M == 3,
    pos_N == 4,
    pos_K == 5,
    pos_L == 6,
    pos_J == 7
)

# Option E: P, O, K, J, L, N, M
opt_e_constr = And(
    pos_P == 1,
    pos_O == 2,
    pos_K == 3,
    pos_J == 4,
    pos_L == 5,
    pos_N == 6,
    pos_M == 7
)

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