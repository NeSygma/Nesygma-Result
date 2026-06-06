from z3 import *

solver = Solver()

# Define the businesses
# 0: optometrist, 1: pharmacy, 2: restaurant1, 3: restaurant2, 4: shoe store, 5: toy store, 6: veterinarian
businesses = [Int(f'biz_{i}') for i in range(7)]

# Each business occupies a unique space (1-7)
solver.add(Distinct(businesses))
for b in businesses:
    solver.add(b >= 1, b <= 7)

# Define symbolic variables for each business type's location
opt = Int('opt')
pharm = Int('pharm')
rest1 = Int('rest1')
rest2 = Int('rest2')
shoe = Int('shoe')
toy = Int('toy')
vet = Int('vet')

# Map each business to its space
solver.add(opt == businesses[0])
solver.add(pharm == businesses[1])
solver.add(rest1 == businesses[2])
solver.add(rest2 == businesses[3])
solver.add(shoe == businesses[4])
solver.add(toy == businesses[5])
solver.add(vet == businesses[6])

# Constraint 1: Pharmacy at one end, one restaurant at the other
# Ends are spaces 1 and 7
solver.add(Or(
    And(pharm == 1, Or(rest1 == 7, rest2 == 7)),
    And(pharm == 7, Or(rest1 == 1, rest2 == 1))
))

# Constraint 2: Two restaurants must be separated by at least two other businesses
# |rest1 - rest2| >= 3
solver.add(Or(rest1 - rest2 >= 3, rest2 - rest1 >= 3))

# Constraint 3: Pharmacy must be next to either optometrist or veterinarian
# |pharm - opt| == 1 OR |pharm - vet| == 1
solver.add(Or(
    Or(pharm - opt == 1, opt - pharm == 1),
    Or(pharm - vet == 1, vet - pharm == 1)
))

# Constraint 4: Toy store cannot be next to veterinarian
# |toy - vet| != 1
solver.add(Not(Or(toy - vet == 1, vet - toy == 1)))

# Constraint 5: Shoe store is in space 4
solver.add(shoe == 4)

# Define the answer options
# (A) The optometrist is next to a restaurant.
opt_a_constr = Or(
    Or(opt - rest1 == 1, rest1 - opt == 1),
    Or(opt - rest2 == 1, rest2 - opt == 1)
)

# (B) The pharmacy is next to the veterinarian.
opt_b_constr = Or(pharm - vet == 1, vet - pharm == 1)

# (C) A restaurant is next to the toy store.
opt_c_constr = Or(
    Or(rest1 - toy == 1, toy - rest1 == 1),
    Or(rest2 - toy == 1, toy - rest2 == 1)
)

# (D) The shoe store is next to the toy store.
opt_d_constr = Or(shoe - toy == 1, toy - shoe == 1)

# (E) The shoe store is next to the veterinarian.
opt_e_constr = Or(shoe - vet == 1, vet - shoe == 1)

# Test each option: check if the option MUST be true (i.e., its negation is unsatisfiable)
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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