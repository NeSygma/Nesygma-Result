from z3 import *

solver = Solver()

# Seven businesses: optometrist(0), pharmacy(1), restaurant1(2), restaurant2(3), shoe_store(4), toy_store(5), veterinarian(6)
# Spaces: 1 through 7
# We assign each business to a space

opt, pharm, rest1, rest2, shoe, toy, vet = Ints('opt pharm rest1 rest2 shoe toy vet')
businesses = [opt, pharm, rest1, rest2, shoe, toy, vet]

# Each business is in a space 1-7
for b in businesses:
    solver.add(b >= 1, b <= 7)

# All different
solver.add(Distinct(businesses))

# Shoe store is in space 2
solver.add(shoe == 2)

# Constraint 1: Pharmacy must be at one end and one restaurant at the other
# Ends are space 1 and space 7
solver.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))

# Constraint 2: Two restaurants must be separated by at least two other businesses
# |rest1 - rest2| >= 3
solver.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))

# Constraint 3: Pharmacy must be next to either optometrist or veterinarian
solver.add(Or(
    Or(pharm - opt == 1, opt - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))

# Constraint 4: Toy store cannot be next to veterinarian
solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))

# Now test each option
found_options = []

# (A) The optometrist is in space 5
solver.push()
solver.add(opt == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) The pharmacy is in space 1
solver.push()
solver.add(pharm == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) A restaurant is in space 3
solver.push()
solver.add(Or(rest1 == 3, rest2 == 3))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) The toy store is in space 6
solver.push()
solver.add(toy == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) The veterinarian is in space 4
solver.push()
solver.add(vet == 4)
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