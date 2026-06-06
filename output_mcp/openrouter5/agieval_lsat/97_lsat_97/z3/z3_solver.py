from z3 import *

# Houses: J, K, L, M, N, O, P (7 houses)
# Positions: 1-7 (1=morning1, 2=morning2, 3=afternoon1, 4=afternoon2, 5=afternoon3, 6=evening1, 7=evening2)
# Morning: positions 1,2
# Afternoon: positions 3,4,5
# Evening: positions 6,7

solver = Solver()

# Create position variables for each house (1-indexed)
J = Int('J')
K = Int('K')
L = Int('L')
M = Int('M')
N = Int('N')
O = Int('O')
P = Int('P')

houses = [J, K, L, M, N, O, P]

# Domain: each house shown at a distinct position 1-7
for h in houses:
    solver.add(h >= 1, h <= 7)
solver.add(Distinct(houses))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(J == 6, J == 7))

# Rule 2: K cannot be shown in the morning (positions 1 or 2)
solver.add(Not(Or(K == 1, K == 2)))

# Rule 3: L must be shown at some time after K and before M
solver.add(K < L)
solver.add(L < M)

# Additional constraint from Q: P is shown in the afternoon (positions 3, 4, or 5)
solver.add(Or(P == 3, P == 4, P == 5))

# Now use the LSAT Multiple Choice Skeleton
# For each option, we check if it MUST be true.
# An option "must be true" if in EVERY valid model, that option holds.
# So we check: is there a model where the option is FALSE?
# If Not(option) is unsat, then option must be true (entailed).

# Option A: J is shown seventh
opt_a_constr = (J == 7)

# Option B: K is shown third
opt_b_constr = (K == 3)

# Option C: N is shown first
opt_c_constr = (N == 1)

# Option D: M is shown in the afternoon
opt_d_constr = Or(M == 3, M == 4, M == 5)

# Option E: O is shown in the morning
opt_e_constr = Or(O == 1, O == 2)

# For "must be true" (entailment), we check if Not(option) is unsat with premises.
# If Not(option) is unsat, then option is entailed (must be true).
# If Not(option) is sat, then option is NOT necessarily true.

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))  # Check if option can be FALSE
    if solver.check() == unsat:
        # Option must be true (its negation is impossible)
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