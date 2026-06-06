from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each antique's auction day
solver = Solver()

harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Each antique is auctioned on a unique day between 1 and 6
solver.add(Distinct(harmonica, lamp, mirror, sundial, table, vase))
solver.add(harmonica >= 1, harmonica <= 6)
solver.add(lamp >= 1, lamp <= 6)
solver.add(mirror >= 1, mirror <= 6)
solver.add(sundial >= 1, sundial <= 6)
solver.add(table >= 1, table <= 6)
solver.add(vase >= 1, vase <= 6)

# Constraint 1: The sundial is not auctioned on June 1st
solver.add(sundial != 1)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp, then the mirror is also auctioned on an earlier date than the lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both
# This means exactly one of the two conditions must be true
solver.add(Or(
    And(table < harmonica, Not(table < vase)),
    And(table < vase, Not(table < harmonica))
))

# Base constraints are now fully encoded

# Now evaluate each multiple-choice option
found_options = []

# Option A: The sundial is auctioned on June 5th
solver.push()
solver.add(sundial == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The sundial is auctioned on June 4th
solver.push()
solver.add(sundial == 4)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The lamp is auctioned on June 5th and the mirror is auctioned on June 6th
solver.push()
solver.add(lamp == 5)
solver.add(mirror == 6)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The table is auctioned on June 3rd and the lamp is auctioned on June 4th
solver.push()
solver.add(table == 3)
solver.add(lamp == 4)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The harmonica is auctioned on June 2nd and the vase is auctioned on June 3rd
solver.push()
solver.add(harmonica == 2)
solver.add(vase == 3)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")