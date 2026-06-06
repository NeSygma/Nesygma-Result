from z3 import *

solver = Solver()

# Seven houses: J, K, L, M, N, O, P
# Positions 1-7 (1-indexed)
J, K, L, M, N, O, P = Ints('J K L M N O P')
houses = [J, K, L, M, N, O, P]

# Each house gets a unique position from 1 to 7
for h in houses:
    solver.add(h >= 1, h <= 7)
solver.add(Distinct(houses))

# Time slots:
# Morning: positions 1, 2
# Afternoon: positions 3, 4, 5
# Evening: positions 6, 7

# J must be shown in the evening (positions 6 or 7)
solver.add(Or(J == 6, J == 7))

# K cannot be shown in the morning (not positions 1 or 2)
solver.add(K != 1, K != 2)

# L must be shown at some time after K is shown and at some time before M is shown
solver.add(L > K)
solver.add(L < M)

# Now evaluate each option
found_options = []

# (A) K is shown at some time after J is shown.
opt_a_constr = (K > J)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) L is shown at some time after J is shown.
opt_b_constr = (L > J)
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) P is shown at some time after J is shown.
opt_c_constr = (P > J)
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Both N and O are shown at some time after M is shown.
opt_d_constr = And(N > M, O > M)
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Both N and P are shown at some time after K is shown.
opt_e_constr = And(N > K, P > K)
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
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