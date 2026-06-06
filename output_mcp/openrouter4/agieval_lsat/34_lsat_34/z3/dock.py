from z3 import *

solver = Solver()

# Cargo positions: 1 to 6, all distinct
pos_fuel, pos_grain, pos_livestock = Ints('pos_fuel pos_grain pos_livestock')
pos_machinery, pos_produce, pos_textiles = Ints('pos_machinery pos_produce pos_textiles')

cargo_vars = [pos_fuel, pos_grain, pos_livestock, pos_machinery, pos_produce, pos_textiles]

# Domain: each position between 1 and 6
for v in cargo_vars:
    solver.add(v >= 1, v <= 6)

# All distinct
solver.add(Distinct(cargo_vars))

# Constraints from problem
solver.add(pos_grain > pos_livestock)
solver.add(pos_livestock > pos_textiles)
solver.add(pos_produce > pos_fuel)
# textiles is next to produce: |pos_textiles - pos_produce| == 1
solver.add(Or(pos_textiles - pos_produce == 1, pos_produce - pos_textiles == 1))

# Options:
# A: fuel next to machinery
opt_a = Or(pos_fuel - pos_machinery == 1, pos_machinery - pos_fuel == 1)
# B: grain next to machinery
opt_b = Or(pos_grain - pos_machinery == 1, pos_machinery - pos_grain == 1)
# C: livestock next to fuel
opt_c = Or(pos_livestock - pos_fuel == 1, pos_fuel - pos_livestock == 1)
# D: produce next to livestock
opt_d = Or(pos_produce - pos_livestock == 1, pos_livestock - pos_produce == 1)
# E: textiles next to fuel
opt_e = Or(pos_textiles - pos_fuel == 1, pos_fuel - pos_textiles == 1)

# Find which option is unsat (must be false)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        impossible_options.append(letter)
    solver.pop()

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found (all are possible)")