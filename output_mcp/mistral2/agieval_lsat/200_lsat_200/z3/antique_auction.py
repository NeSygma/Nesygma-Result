from z3 import *

# Declare symbolic variables for each antique's auction day (1 to 6)
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Ensure all days are between 1 and 6 and distinct
solver = Solver()
solver.add(Distinct(harmonica, lamp, mirror, sundial, table, vase))
solver.add(harmonica >= 1, harmonica <= 6)
solver.add(lamp >= 1, lamp <= 6)
solver.add(mirror >= 1, mirror <= 6)
solver.add(sundial >= 1, sundial <= 6)
solver.add(table >= 1, table <= 6)
solver.add(vase >= 1, vase <= 6)

# Constraint 1: The sundial is not auctioned on June 1st
solver.add(sundial != 1)

# Constraint 2: If harmonica is auctioned earlier than lamp, then mirror is also auctioned earlier than lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned earlier than the mirror and earlier than the vase
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned earlier than the harmonica or earlier than the vase, but not both
solver.add(Or(
    And(table < harmonica, Not(table < vase)),
    And(table < vase, Not(table < harmonica))
))

# Evaluate each option
found_options = []
options = [
    ("A", mirror == 2),
    ("B", lamp == 2),
    ("C", vase == 2),
    ("D", lamp == 3),
    ("E", mirror == 5)
]

for letter, constr in options:
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