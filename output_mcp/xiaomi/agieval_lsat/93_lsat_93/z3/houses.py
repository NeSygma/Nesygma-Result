from z3 import *

solver = Solver()

# Seven houses: J, K, L, M, N, O, P
# Position variables: 1..7 (first through seventh)
J, K, L, M, N, O, P = Ints('J K L M N O P')
houses = [J, K, L, M, N, O, P]

# All positions are between 1 and 7, all distinct
for h in houses:
    solver.add(h >= 1, h <= 7)
solver.add(Distinct(houses))

# Time slots:
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# Rule 1: J must be shown in the evening (position 6 or 7)
solver.add(Or(J == 6, J == 7))

# Rule 2: K cannot be shown in the morning (not position 1 or 2)
solver.add(K != 1, K != 2)

# Rule 3: L must be shown after K and before M
solver.add(K < L)
solver.add(L < M)

# Now test each answer choice
# (A) K, O, L, M, N, J, P
opt_a = And(K == 1, O == 2, L == 3, M == 4, N == 5, J == 6, P == 7)
# (B) N, L, P, K, M, O, J
opt_b = And(N == 1, L == 2, P == 3, K == 4, M == 5, O == 6, J == 7)
# (C) O, P, K, L, N, M, J
opt_c = And(O == 1, P == 2, K == 3, L == 4, N == 5, M == 6, J == 7)
# (D) O, P, M, N, K, L, J
opt_d = And(O == 1, P == 2, M == 3, N == 4, K == 5, L == 6, J == 7)
# (E) P, O, K, J, L, N, M
opt_e = And(P == 1, O == 2, K == 3, J == 4, L == 5, N == 6, M == 7)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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