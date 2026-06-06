from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# 1. Declare symbolic variables
# bays[i] is the cargo type in bay i+1 (0=fuel, 1=grain, 2=livestock, 3=machinery, 4=produce, 5=textiles)
bays = [Int(f'bay_{i+1}') for i in range(6)]

# positions[i] is the bay number (1-6) for cargo type i
positions = [Int(f'pos_{cargo}') for cargo in range(6)]

# Cargo type constants
fuel, grain, livestock, machinery, produce, textiles = 0, 1, 2, 3, 4, 5

# 2. Add base constraints
solver = Solver()

# Each bay has a distinct cargo type
solver.add(Distinct(bays))

# Each cargo type is assigned to exactly one bay
solver.add(Distinct(positions))

# Link cargo types to positions: bays[i] = cargo type, positions[cargo] = bay number (1-6)
for i in range(6):
    for cargo in range(6):
        solver.add(Implies(bays[i] == cargo, positions[cargo] == i+1))

# Constraint 1: grain > livestock (positionally)
solver.add(positions[grain] > positions[livestock])

# Constraint 2: livestock > textiles (positionally)
solver.add(positions[livestock] > positions[textiles])

# Constraint 3: produce > fuel (positionally)
solver.add(positions[produce] > positions[fuel])

# Constraint 4: textiles is next to produce (adjacent positions)
solver.add(Or(
    positions[textiles] == positions[produce] + 1,
    positions[textiles] == positions[produce] - 1
))

# 3. Evaluate each option
found_options = []

# Option A: fuel is next to machinery
opt_a_constr = Or(
    Or([And(positions[fuel] == positions[machinery] + 1, positions[fuel] != 6) for _ in range(1)]),
    Or([And(positions[fuel] == positions[machinery] - 1, positions[fuel] != 1) for _ in range(1)])
)

# Option B: grain is next to machinery
opt_b_constr = Or(
    Or([And(positions[grain] == positions[machinery] + 1, positions[grain] != 6) for _ in range(1)]),
    Or([And(positions[grain] == positions[machinery] - 1, positions[grain] != 1) for _ in range(1)])
)

# Option C: livestock is next to fuel
opt_c_constr = Or(
    Or([And(positions[livestock] == positions[fuel] + 1, positions[livestock] != 6) for _ in range(1)]),
    Or([And(positions[livestock] == positions[fuel] - 1, positions[livestock] != 1) for _ in range(1)])
)

# Option D: produce is next to livestock
opt_d_constr = Or(
    Or([And(positions[produce] == positions[livestock] + 1, positions[produce] != 6) for _ in range(1)]),
    Or([And(positions[produce] == positions[livestock] - 1, positions[produce] != 1) for _ in range(1)])
)

# Option E: textiles is next to fuel
opt_e_constr = Or(
    Or([And(positions[textiles] == positions[fuel] + 1, positions[textiles] != 6) for _ in range(1)]),
    Or([And(positions[textiles] == positions[fuel] - 1, positions[textiles] != 1) for _ in range(1)])
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")