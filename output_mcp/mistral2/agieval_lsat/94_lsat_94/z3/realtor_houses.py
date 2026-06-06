from z3 import *

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

# Base constraints are set. Now evaluate each option for consecutive showing.
# We need to check if any pair in the options can appear consecutively in either order.

# Helper function to check if two houses can be consecutive
def can_be_consecutive(a, b):
    # Check if a and b are adjacent in the sequence
    solver.push()
    solver.add(Or(
        And(a == houses[i], b == houses[i+1]) for i in range(6)
    ))
    res = solver.check()
    solver.pop()
    return res == sat

# Evaluate each option
found_options = []

# Option A: J and K cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], K == houses[i+1]) for i in range(6)
), Or(
    And(K == houses[i], J == houses[i+1]) for i in range(6)
))
if solver.check() == sat:
    found_options.append("A")
else:
    print("Option A is invalid (J and K cannot be consecutive)")
solver.pop()

# Option B: J and M cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], M == houses[i+1]) for i in range(6)
), Or(
    And(M == houses[i], J == houses[i+1]) for i in range(6)
))
if solver.check() == sat:
    found_options.append("B")
else:
    print("Option B is invalid (J and M cannot be consecutive)")
solver.pop()

# Option C: J and O cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], O == houses[i+1]) for i in range(6)
), Or(
    And(O == houses[i], J == houses[i+1]) for i in range(6)
))
if solver.check() == sat:
    found_options.append("C")
else:
    print("Option C is invalid (J and O cannot be consecutive)")
solver.pop()

# Option D: J and P cannot be consecutive
solver.push()
solver.add(Or(
    And(J == houses[i], P == houses[i+1]) for i in range(6)
), Or(
    And(P == houses[i], J == houses[i+1]) for i in range(6)
))
if solver.check() == sat:
    found_options.append("D")
else:
    print("Option D is invalid (J and P cannot be consecutive)")
solver.pop()

# Option E: M and P cannot be consecutive
solver.push()
solver.add(Or(
    And(M == houses[i], P == houses[i+1]) for i in range(6)
), Or(
    And(P == houses[i], M == houses[i+1]) for i in range(6)
))
if solver.check() == sat:
    found_options.append("E")
else:
    print("Option E is invalid (M and P cannot be consecutive)")
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