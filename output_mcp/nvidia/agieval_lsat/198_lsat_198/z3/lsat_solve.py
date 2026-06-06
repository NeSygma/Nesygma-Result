from z3 import *

solver = Solver()

# Declare variables
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Add domain constraints
for var in [harmonica, lamp, mirror, sundial, table, vase]:
    solver.add(var >= 1, var <= 6)

# All items distinct
solver.add(Distinct([harmonica, lamp, mirror, sundial, table, vase]))

# Base constraints
solver.add(sundial != 1)  # sundial not on June 1st
solver.add(Implies(harmonica < lamp, mirror < lamp))  # conditional
solver.add(sundial < mirror)  # sundial earlier than mirror
solver.add(sundial < vase)    # sundial earlier than vase
solver.add(Xor(table < harmonica, table < vase))  # table earlier than exactly one of harmonica or vase
solver.add(table > mirror)    # table later than mirror
solver.add(table > vase)      # table later than vase

# Option constraints
opt_a_constr = harmonica < table
opt_b_constr = table < lamp
opt_c_constr = table < sundial
opt_d_constr = mirror < vase
opt_e_constr = sundial < lamp

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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