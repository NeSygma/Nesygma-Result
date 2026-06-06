from z3 import *

solver = Solver()

# Variables: each cargo type is assigned a bay number 1-6
fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargos = [fuel, grain, livestock, machinery, produce, textiles]

# Domain: each cargo is in a bay numbered 1 through 6
for c in cargos:
    solver.add(c >= 1, c <= 6)

# All different: each bay holds exactly one type of cargo
solver.add(Distinct(cargos))

# Constraints
solver.add(grain > livestock)       # grain has higher number than livestock
solver.add(livestock > textiles)    # livestock has higher number than textiles
solver.add(produce > fuel)          # produce has higher number than fuel
solver.add(Or(textiles == produce + 1, textiles == produce - 1))  # textiles is next to produce

# Option constraints: each option defines what cargo is in bay 1, bay 2, bay 3
# We encode: for each bay position, the cargo variable equals that bay number.
# E.g., option A: bay1=fuel, bay2=machinery, bay3=textiles
# So fuel == 1, machinery == 2, textiles == 3

opt_a_constr = And(fuel == 1, machinery == 2, textiles == 3)
opt_b_constr = And(grain == 1, machinery == 2, fuel == 3)
opt_c_constr = And(machinery == 1, livestock == 2, fuel == 3)
opt_d_constr = And(machinery == 1, textiles == 2, fuel == 3)
opt_e_constr = And(machinery == 1, textiles == 2, produce == 3)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        print(f"Option {letter} is SAT. Model: fuel={m[fuel]}, grain={m[grain]}, livestock={m[livestock]}, machinery={m[machinery]}, produce={m[produce]}, textiles={m[textiles]}")
        found_options.append(letter)
    else:
        print(f"Option {letter} is UNSAT")
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