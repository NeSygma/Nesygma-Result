from z3 import *

solver = Solver()

# Declare variables
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')

# Base constraints
solver.add(sundial != 0)  # not June 1
solver.add(Implies(harmonica < lamp, mirror < lamp))
solver.add(sundial < mirror)
solver.add(sundial < vase)
solver.add(Xor(table < harmonica, table < vase))
solver.add(Distinct([harmonica, lamp, mirror, sundial, table, vase]))

# Define option constraints
opt_a_constr = And(table == 1, lamp == 2)
opt_b_constr = And(sundial == 1, vase == 2)
opt_c_constr = And(mirror == 2, sundial == 3)
opt_d_constr = And(vase == 3, sundial == 4)
opt_e_constr = And(sundial == 3, table == 4)

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