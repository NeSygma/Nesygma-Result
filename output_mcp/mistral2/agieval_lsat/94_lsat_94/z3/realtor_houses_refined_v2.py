from z3 import *

# Base constraints
solver = Solver()

# Declare the houses as symbolic integers representing their positions (1 to 7)
houses = [Int(f'house_{i}') for i in range(7)]
# Each house is assigned a unique position from 1 to 7
solver.add(Distinct(houses))
for h in houses:
    solver.add(h >= 1, h <= 7)

# Assign letters to houses for clarity
J, K, L, M, N, O, P = houses

# Morning: positions 1 and 2
morning = [houses[0], houses[1]]
# Afternoon: positions 3, 4, 5
afternoon = [houses[2], houses[3], houses[4]]
# Evening: positions 6 and 7
evening = [houses[5], houses[6]]

# Rules:
# 1. J must be shown in the evening
solver.add(Or(J == 6, J == 7))

# 2. K cannot be shown in the morning
solver.add(Not(Or(K == 1, K == 2)))

# 3. L must be shown after K and before M
# This means K < L < M in terms of positions
solver.add(K < L)
solver.add(L < M)

# Now evaluate each option to see if the pair can be consecutive in any valid ordering
found_options = []

# Option A: J and K cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], K == houses[i+1]) for i in range(6)
), Or(
    And(K == houses[i], J == houses[i+1]) for i in range(6)
))
res_A = solver.check()
solver.pop()

# Option B: J and M cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], M == houses[i+1]) for i in range(6)
), Or(
    And(M == houses[i], J == houses[i+1]) for i in range(6)
))
res_B = solver.check()
solver.pop()

# Option C: J and O cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], O == houses[i+1]) for i in range(6)
), Or(
    And(O == houses[i], J == houses[i+1]) for i in range(6)
))
res_C = solver.check()
solver.pop()

# Option D: J and P cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], P == houses[i+1]) for i in range(6)
), Or(
    And(P == houses[i], J == houses[i+1]) for i in range(6)
))
res_D = solver.check()
solver.pop()

# Option E: M and P cannot be consecutive
solver.push()
solver.add(Or(
    And(M == houses[i], P == houses[i+1]) for i in range(6)
), Or(
    And(P == houses[i], M == houses[i+1]) for i in range(6)
))
res_E = solver.check()
solver.pop()

# The correct answer is the option where the pair CANNOT be consecutive (res == unsat)
if res_A == unsat:
    found_options.append("A")
if res_B == unsat:
    found_options.append("B")
if res_C == unsat:
    found_options.append("C")
if res_D == unsat:
    found_options.append("D")
if res_E == unsat:
    found_options.append("E")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")