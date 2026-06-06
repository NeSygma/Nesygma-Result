from z3 import *

solver = Solver()

# Declare variables for positions (1-7)
P = Int('P')   # Pharmacy
O = Int('O')   # Optometrist
S = Int('S')   # Shoe store
T = Int('T')   # Toy store
V = Int('V')   # Veterinarian
R1 = Int('R1')  # Restaurant 1
R2 = Int('R2')  # Restaurant 2

all_vars = [P, O, S, T, V, R1, R2]

# Domain: each position is between 1 and 7
for v in all_vars:
    solver.add(v >= 1, v <= 7)

# All positions are distinct
solver.add(Distinct(all_vars))

# Constraint 1: Pharmacy at one end, a restaurant at the other
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: The two restaurants must be separated by at least two other businesses
# So |R1 - R2| >= 3
solver.add(Or(R1 - R2 >= 3, R2 - R1 >= 3))

# Constraint 3: Pharmacy next to optometrist or veterinarian
# Since P is at an end (1 or 7), the adjacent space is 2 (if P==1) or 6 (if P==7)
solver.add(Or(
    And(P == 1, Or(O == 2, V == 2)),
    And(P == 7, Or(O == 6, V == 6))
))

# Constraint 4: Toy store cannot be next to veterinarian
solver.add(Not(Or(T - V == 1, V - T == 1)))

# Given: Shoe store is in space 2
solver.add(S == 2)

# Now test each option
found_options = []

# Option A: Optometrist in space 5
solver.push()
solver.add(O == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Pharmacy in space 1
solver.push()
solver.add(P == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is in space 3
solver.push()
solver.add(Or(R1 == 3, R2 == 3))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Toy store in space 6
solver.push()
solver.add(T == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Veterinarian in space 4
solver.push()
solver.add(V == 4)
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