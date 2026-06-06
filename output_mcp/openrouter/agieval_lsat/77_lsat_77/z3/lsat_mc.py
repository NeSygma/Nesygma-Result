from z3 import *

solver = Solver()
# Variables
opt = Int('opt')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')
vars = [opt, pharm, rest1, rest2, shoe, toy, vet]
# Domains
for v in vars:
    solver.add(v >= 1, v <= 7)
# Distinct
solver.add(Distinct(vars))
# Shoe store in space 2
solver.add(shoe == 2)
# Pharmacy at an end
solver.add(Or(pharm == 1, pharm == 7))
# One restaurant at the other end
end_rest = Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
)
solver.add(end_rest)
# Restaurants separated by at least two other businesses
solver.add(Abs(rest1 - rest2) >= 3)
# Pharmacy adjacent to opt or vet
solver.add(Or(Abs(pharm - opt) == 1, Abs(pharm - vet) == 1))
# Toy not next to vet
solver.add(Abs(toy - vet) != 1)

# Option constraints
opt_a = opt == 5
opt_b = pharm == 1
opt_c = Or(rest1 == 3, rest2 == 3)
opt_d = toy == 6
opt_e = vet == 4

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
found = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")