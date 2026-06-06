from z3 import *

solver = Solver()

# Variables for positions (1st through 7th)
J = Int('J')
K = Int('K')
L = Int('L')
M = Int('M')
N = Int('N')
O = Int('O')
P = Int('P')

houses = [J, K, L, M, N, O, P]

# Domain: positions 1-7
for h in houses:
    solver.add(h >= 1, h <= 7)

# All distinct positions
solver.add(Distinct(houses))

# Rule 1: J must be shown in the evening (positions 6 or 7)
solver.add(Or(J == 6, J == 7))

# Rule 2: K cannot be shown in the morning (not positions 1 or 2)
solver.add(Not(Or(K == 1, K == 2)))

# Rule 3: L must be after K and before M
solver.add(K < L)
solver.add(L < M)

# Given: P is shown in the afternoon (positions 3, 4, or 5)
solver.add(Or(P == 3, P == 4, P == 5))

# Now test each option using the "must be true" (entailment) pattern:
# An option MUST be true if premises + NOT(option) is unsatisfiable.
found_options = []

# Option A: J is shown seventh
opt_a = (J == 7)
solver.push()
solver.add(Not(opt_a))
if solver.check() == unsat:
    found_options.append("A")
solver.pop()

# Option B: K is shown third
opt_b = (K == 3)
solver.push()
solver.add(Not(opt_b))
if solver.check() == unsat:
    found_options.append("B")
solver.pop()

# Option C: N is shown first
opt_c = (N == 1)
solver.push()
solver.add(Not(opt_c))
if solver.check() == unsat:
    found_options.append("C")
solver.pop()

# Option D: M is shown in the afternoon
opt_d = Or(M == 3, M == 4, M == 5)
solver.push()
solver.add(Not(opt_d))
if solver.check() == unsat:
    found_options.append("D")
solver.pop()

# Option E: O is shown in the morning
opt_e = Or(O == 1, O == 2)
solver.push()
solver.add(Not(opt_e))
if solver.check() == unsat:
    found_options.append("E")
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