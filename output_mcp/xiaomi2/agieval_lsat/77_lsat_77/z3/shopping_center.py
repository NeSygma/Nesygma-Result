from z3 import *

solver = Solver()

# 7 businesses mapped to spaces 1-7
# O=Optometrist, P=Pharmacy, R1=Restaurant1, R2=Restaurant2, S=ShoeStore, T=ToyStore, V=Veterinarian
O, P, R1, R2, S, T, V = Ints('O P R1 R2 S T V')
businesses = [O, P, R1, R2, S, T, V]

# Each business in a space 1-7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different
solver.add(Distinct(businesses))

# Given: Shoe store is in space 2
solver.add(S == 2)

# Constraint 1: Pharmacy at one end, one restaurant at the other end
solver.add(Or(
    And(P == 1, Or(R1 == 7, R2 == 7)),
    And(P == 7, Or(R1 == 1, R2 == 1))
))

# Constraint 2: Two restaurants separated by at least 2 other businesses
solver.add(Abs(R1 - R2) >= 3)

# Constraint 3: Pharmacy next to optometrist or veterinarian
solver.add(Or(Abs(P - O) == 1, Abs(P - V) == 1))

# Constraint 4: Toy store cannot be next to veterinarian
solver.add(Abs(T - V) != 1)

# Now test each option
found_options = []

# (A) Optometrist is in space 5
solver.push()
solver.add(O == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Pharmacy is in space 1
solver.push()
solver.add(P == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) A restaurant is in space 3
solver.push()
solver.add(Or(R1 == 3, R2 == 3))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Toy store is in space 6
solver.push()
solver.add(T == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Veterinarian is in space 4
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