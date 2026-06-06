from z3 import *

solver = Solver()

# Declare variables
letters = ['D','O','N','A','L','G','E','R','B','T']
vars = {l: Int(l) for l in letters}

# Leading non-zero
solver.add(vars['D'] != 0)
solver.add(vars['G'] != 0)
solver.add(vars['R'] != 0)

# All distinct
solver.add(Distinct(list(vars.values())))

# Digits 0-9 domain
for v in vars.values():
    solver.add(v >= 0, v <= 9)

# Carries
c1 = Int('c1'); c2 = Int('c2'); c3 = Int('c3'); c4 = Int('c4'); c5 = Int('c5')
for c in [c1,c2,c3,c4,c5]:
    solver.add(c >= 0, c <= 1)

# Column equations
solver.add(vars['D'] + vars['D'] == vars['T'] + 10*c1)                     # units
solver.add(vars['L'] + vars['L'] + c1 == vars['R'] + 10*c2)               # tens
solver.add(vars['A'] + vars['A'] + c2 == vars['E'] + 10*c3)               # hundreds
solver.add(vars['N'] + vars['R'] + c3 == vars['B'] + 10*c4)               # thousands
solver.add(vars['E'] + c4 == 10*c5)                                       # ten-thousands simplification
solver.add(vars['D'] + vars['G'] + c5 == vars['R'])                       # hundred-thousands

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    for l in letters:
        print(f"{l} = {model[vars[l]]}")
else:
    print("STATUS: unsat")