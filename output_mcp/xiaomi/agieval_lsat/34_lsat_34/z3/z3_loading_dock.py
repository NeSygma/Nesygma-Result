from z3 import *

solver = Solver()

# Variables: bay position for each cargo type (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Each cargo is in a bay 1-6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different bays
solver.add(Distinct(cargos))

# Constraint 1: grain > livestock
solver.add(grain > livestock)

# Constraint 2: livestock > textiles
solver.add(livestock > textiles)

# Constraint 3: produce > fuel
solver.add(produce > fuel)

# Constraint 4: textiles is next to produce (|textiles - produce| == 1)
solver.add(Or(textiles - produce == 1, produce - textiles == 1))

# Now evaluate each option to see which MUST be false
# An option "must be false" means it is NEVER true in any valid arrangement
# So we check: is there a valid arrangement where the option IS true?
# If NO valid arrangement makes it true, then it MUST be false.

# Option A: fuel is next to machinery
opt_a = Or(fuel - machinery == 1, machinery - fuel == 1)

# Option B: grain is next to machinery
opt_b = Or(grain - machinery == 1, machinery - grain == 1)

# Option C: livestock is next to fuel
opt_c = Or(livestock - fuel == 1, fuel - livestock == 1)

# Option D: produce is next to livestock
opt_d = Or(produce - livestock == 1, livestock - produce == 1)

# Option E: textiles is next to fuel
opt_e = Or(textiles - fuel == 1, fuel - textiles == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

# For each option, check if there EXISTS a valid arrangement where it's true
# If sat: the option CAN be true (so it does NOT "must be false")
# If unsat: the option CANNOT be true (so it MUST be false)
must_be_false_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        must_be_false_options.append(letter)
    solver.pop()

if len(must_be_false_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_false_options[0]}")
elif len(must_be_false_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be false {must_be_false_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be false")