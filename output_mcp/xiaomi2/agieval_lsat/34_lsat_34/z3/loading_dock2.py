from z3 import *

solver = Solver()

# Each cargo type gets a bay number (1-6), all different
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# All bays are 1-6
for c in cargos:
    solver.add(And(c >= 1, c <= 6))

# All different
solver.add(Distinct(cargos))

# Constraint 1: grain > livestock
solver.add(grain > livestock)

# Constraint 2: livestock > textiles
solver.add(livestock > textiles)

# Constraint 3: produce > fuel
solver.add(produce > fuel)

# Constraint 4: textiles is next to produce
solver.add(Abs(textiles - produce) == 1)

# Answer choices - each one claims a "next to" relationship
# Question: which one MUST be false (is impossible)?
# We test each: if adding the constraint makes it UNSAT, that option must be false.

opt_a = Abs(fuel - machinery) == 1        # fuel next to machinery
opt_b = Abs(grain - machinery) == 1       # grain next to machinery
opt_c = Abs(livestock - fuel) == 1        # livestock next to fuel
opt_d = Abs(produce - livestock) == 1     # produce next to livestock
opt_e = Abs(textiles - fuel) == 1         # textiles next to fuel

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

impossible_options = []
possible_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        possible_options.append(letter)
    else:
        impossible_options.append(letter)
    solver.pop()

print(f"Possible options: {possible_options}")
print(f"Impossible options: {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")