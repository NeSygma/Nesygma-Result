from z3 import *

solver = Solver()

# Variables: position (day 1-6) for each antique
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

antiques = [harmonica, lamp, mirror, sundial, table, vase]

# Each antique on a different day, days 1-6
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Constraint 1: Sundial not on June 1st
solver.add(sundial != 1)

# Constraint 2: If harmonica < lamp, then mirror < lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: Sundial < mirror AND sundial < vase
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: (table < harmonica OR table < vase) but NOT both (XOR)
solver.add(Xor(table < harmonica, table < vase))

# Define each answer choice
# (A) harmonica, table, sundial, lamp, vase, mirror
opt_a = And(harmonica == 1, table == 2, sundial == 3, lamp == 4, vase == 5, mirror == 6)
# (B) lamp, harmonica, sundial, mirror, vase, table
opt_b = And(lamp == 1, harmonica == 2, sundial == 3, mirror == 4, vase == 5, table == 6)
# (C) harmonica, sundial, table, mirror, lamp, vase
opt_c = And(harmonica == 1, sundial == 2, table == 3, mirror == 4, lamp == 5, vase == 6)
# (D) sundial, mirror, harmonica, table, vase, lamp
opt_d = And(sundial == 1, mirror == 2, harmonica == 3, table == 4, vase == 5, lamp == 6)
# (E) vase, sundial, lamp, harmonica, table, mirror
opt_e = And(vase == 1, sundial == 2, lamp == 3, harmonica == 4, table == 5, mirror == 6)

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