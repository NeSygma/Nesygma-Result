from z3 import *

solver = Solver()

# Declare variables for each cargo's bay number
grain = Int('grain')
livestock = Int('livestock')
textiles = Int('textiles')
produce = Int('produce')
fuel = Int('fuel')
machinery = Int('machinery')

# All bays are between 1 and 6
solver.add(grain >= 1, grain <= 6)
solver.add(livestock >= 1, livestock <= 6)
solver.add(textiles >= 1, textiles <= 6)
solver.add(produce >= 1, produce <= 6)
solver.add(fuel >= 1, fuel <= 6)
solver.add(machinery >= 1, machinery <= 6)

# All bays are distinct
solver.add(Distinct([grain, livestock, textiles, produce, fuel, machinery]))

# Base constraints
solver.add(grain > livestock)
solver.add(livestock > textiles)
solver.add(produce > fuel)
solver.add(Abs(textiles - produce) == 1)  # adjacent

# Extra condition: produce is next to livestock
solver.add(Abs(produce - livestock) == 1)

# Define option constraints
opt_a_constr = (fuel == 2)
opt_b_constr = (produce == 4)
opt_c_constr = (textiles == 4)
opt_d_constr = (grain == 5)
opt_e_constr = (machinery == 5)

# Evaluate each option: collect unsat options (cannot be true)
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() != sat:  # if unsatisfiable, then this option cannot be true
        found_options.append(letter)
    solver.pop()

# According to the problem, exactly one option cannot be true (EXCEPT)
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")