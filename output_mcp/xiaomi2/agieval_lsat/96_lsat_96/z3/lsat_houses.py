from z3 import *

solver = Solver()

# Houses: J, K, L, M, N, O, P
# Each house gets a position 1-7 (all different)
J, K, L, M, N, O, P = Ints('J K L M N O P')
houses = [J, K, L, M, N, O, P]

# All positions are 1-7 and distinct
for h in houses:
    solver.add(h >= 1, h <= 7)
solver.add(Distinct(houses))

# Time slots:
# Positions 1,2 = morning
# Positions 3,4,5 = afternoon
# Positions 6,7 = evening

# Constraint 1: J must be shown in the evening
solver.add(Or(J == 6, J == 7))

# Constraint 2: K cannot be shown in the morning
solver.add(K >= 3)

# Constraint 3: L must be shown after K and before M (K < L < M)
solver.add(K < L)
solver.add(L < M)

# Now check each option to see which COULD be true

found_options = []

# (A) K is shown at some time after J is shown: K > J
solver.push()
solver.add(K > J)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) L is shown at some time after J is shown: L > J
solver.push()
solver.add(L > J)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) P is shown at some time after J is shown: P > J
solver.push()
solver.add(P > J)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Both N and O are shown at some time after M: N > M AND O > M
solver.push()
solver.add(N > M)
solver.add(O > M)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Both N and P are shown at some time after K: N > K AND P > K
solver.push()
solver.add(N > K)
solver.add(P > K)
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