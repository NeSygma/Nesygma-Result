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
# Base constraints
# Pharmacy at an end
pharm_end = Or(pharm == 1, pharm == 7)
solver.add(pharm_end)
# One restaurant at the other end
other_end_rest = Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
)
solver.add(other_end_rest)
# Restaurants separated by at least two other businesses: distance >=3
rest_dist = If(rest1 > rest2, rest1 - rest2, rest2 - rest1) >= 3
solver.add(rest_dist)
# Pharmacy next to either optometrist or veterinarian
pharm_next_opt = If(pharm > opt, pharm - opt, opt - pharm) == 1
pharm_next_vet = If(pharm > vet, pharm - vet, vet - pharm) == 1
solver.add(Or(pharm_next_opt, pharm_next_vet))
# Toy store cannot be next to veterinarian
toy_not_next_vet = If(toy > vet, toy - vet, vet - toy) != 1
solver.add(toy_not_next_vet)
# Shoe store is in space 4
solver.add(shoe == 4)

# Define option constraints
# A: opt next to a restaurant
opt_next_rest = Or(
    If(opt > rest1, opt - rest1, rest1 - opt) == 1,
    If(opt > rest2, opt - rest2, rest2 - opt) == 1
)
# B: pharmacy next to veterinarian
pharm_next_vet_opt = If(pharm > vet, pharm - vet, vet - pharm) == 1
# C: a restaurant next to toy store
rest_next_toy = Or(
    If(toy > rest1, toy - rest1, rest1 - toy) == 1,
    If(toy > rest2, toy - rest2, rest2 - toy) == 1
)
# D: shoe next to toy store
shoe_next_toy = If(shoe > toy, shoe - toy, toy - shoe) == 1
# E: shoe next to veterinarian
shoe_next_vet = If(shoe > vet, shoe - vet, vet - shoe) == 1

options = [
    ("A", opt_next_rest),
    ("B", pharm_next_vet_opt),
    ("C", rest_next_toy),
    ("D", shoe_next_toy),
    ("E", shoe_next_vet)
]

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