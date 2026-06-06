from z3 import *

# Declare variables for each cargo type's bay number (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

solver = Solver()

# Base constraints: each bay number between 1 and 6
solver.add(fuel >= 1, fuel <= 6)
solver.add(grain >= 1, grain <= 6)
solver.add(livestock >= 1, livestock <= 6)
solver.add(machinery >= 1, machinery <= 6)
solver.add(produce >= 1, produce <= 6)
solver.add(textiles >= 1, textiles <= 6)

# All distinct
solver.add(Distinct(fuel, grain, livestock, machinery, produce, textiles))

# Given ordering constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Abs(textiles - produce) == 1)  # next to each other

# Define each option as a constraint
opt_a = (Abs(fuel - machinery) == 1)  # fuel next to machinery
opt_b = (Abs(grain - machinery) == 1)  # grain next to machinery
opt_c = (Abs(livestock - fuel) == 1)  # livestock next to fuel
opt_d = (Abs(produce - livestock) == 1)  # produce next to livestock
opt_e = (Abs(textiles - fuel) == 1)  # textiles next to fuel

# Evaluate each option: we want the one that must be false (i.e., adding it makes unsat)
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:  # if adding the option leads to unsat, then it must be false
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