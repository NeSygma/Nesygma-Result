from z3 import *

solver = Solver()
# Variables for positions 1..7
opt = Int('opt')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')

vars = [opt, pharm, rest1, rest2, shoe, toy, vet]
# Domain constraints
for v in vars:
    solver.add(v >= 1, v <= 7)
# All distinct
solver.add(Distinct(vars))
# Given: vet in space5
solver.add(vet == 5)
# Pharmacy at an end
solver.add(Or(pharm == 1, pharm == 7))
# One restaurant at the other end (exactly one)
solver.add(Or(
    And(pharm == 1, rest1 == 7, rest2 != 7),
    And(pharm == 1, rest2 == 7, rest1 != 7),
    And(pharm == 7, rest1 == 1, rest2 != 1),
    And(pharm == 7, rest2 == 1, rest1 != 1)
))
# Restaurants separated by at least two other businesses: distance >=3
solver.add(Abs(rest1 - rest2) >= 3)
# Pharmacy next to either optometrist or veterinarian
solver.add(Or(Abs(pharm - opt) == 1, Abs(pharm - vet) == 1))
# Toy store cannot be next to veterinarian
solver.add(Abs(toy - vet) != 1)

# Define option constraints
opt_a = opt == 2
opt_b = pharm == 7
opt_c = Or(rest1 == 4, rest2 == 4)
opt_d = shoe == 6
opt_e = toy == 3

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
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