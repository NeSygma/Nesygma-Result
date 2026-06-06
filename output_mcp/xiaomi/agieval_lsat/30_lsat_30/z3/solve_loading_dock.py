from z3 import *

solver = Solver()

# Bays 1-6, each holds a different cargo
# Cargos: fuel=0, grain=1, livestock=2, machinery=3, produce=4, textiles=5
cargos = ['fuel', 'grain', 'livestock', 'machinery', 'produce', 'textiles']
cargo_vars = [Int(f'bay_{i}') for i in range(1, 7)]

# Each bay holds a cargo 0-5, all different
for c in cargo_vars:
    solver.add(c >= 0, c <= 5)
solver.add(Distinct(cargo_vars))

# grain > livestock (bay number)
solver.add(Or([And(cargo_vars[i] == 1, cargo_vars[j] == 2, i > j) for i in range(6) for j in range(6)]))
# livestock > textiles
solver.add(Or([And(cargo_vars[i] == 2, cargo_vars[j] == 5, i > j) for i in range(6) for j in range(6)]))
# produce > fuel
solver.add(Or([And(cargo_vars[i] == 4, cargo_vars[j] == 0, i > j) for i in range(6) for j in range(6)]))
# textiles is next to produce
solver.add(Or([And(cargo_vars[i] == 5, cargo_vars[j] == 4, Or(i == j + 1, j == i + 1)) for i in range(6) for j in range(6)]))

# Define options for first three bays (bay1, bay2, bay3)
# A: fuel, machinery, textiles
opt_a = And(cargo_vars[0] == 0, cargo_vars[1] == 3, cargo_vars[2] == 5)
# B: grain, machinery, fuel
opt_b = And(cargo_vars[0] == 1, cargo_vars[1] == 3, cargo_vars[2] == 0)
# C: machinery, livestock, fuel
opt_c = And(cargo_vars[0] == 3, cargo_vars[1] == 2, cargo_vars[2] == 0)
# D: machinery, textiles, fuel
opt_d = And(cargo_vars[0] == 3, cargo_vars[1] == 5, cargo_vars[2] == 0)
# E: machinery, textiles, produce
opt_e = And(cargo_vars[0] == 3, cargo_vars[1] == 5, cargo_vars[2] == 4)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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