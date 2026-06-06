from z3 import *

solver = Solver()

# Declare integer variables for each cargo, representing bay numbers (1-6)
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

# All variables domain 1..6
solver.add(And(fuel >= 1, fuel <= 6))
solver.add(And(grain >= 1, grain <= 6))
solver.add(And(livestock >= 1, livestock <= 6))
solver.add(And(machinery >= 1, machinery <= 6))
solver.add(And(produce >= 1, produce <= 6))
solver.add(And(textiles >= 1, textiles <= 6))

# AllDifferent
solver.add(Distinct([fuel, grain, livestock, machinery, produce, textiles]))

# Constraints from problem
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
# textiles next to produce: absolute difference = 1
solver.add(Or(textiles == produce + 1, textiles + 1 == produce))

# Define option constraints
opt_a_constr = Or(fuel == machinery + 1, fuel + 1 == machinery)  # fuel next to machinery
opt_b_constr = Or(grain == machinery + 1, grain + 1 == machinery)  # grain next to machinery
opt_c_constr = Or(livestock == fuel + 1, livestock + 1 == fuel)   # livestock next to fuel
opt_d_constr = Or(produce == livestock + 1, produce + 1 == livestock)  # produce next to livestock
opt_e_constr = Or(textiles == fuel + 1, textiles + 1 == fuel)  # textiles next to fuel

# Skeleton for evaluating multiple choice options
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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