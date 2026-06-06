from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each antique's auction day
# Days are 1 (June 1) to 6 (June 6)
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Base constraints
solver = Solver()

# Each antique is auctioned on a unique day
solver.add(Distinct(harmonica, lamp, mirror, sundial, table, vase))

# Days are between 1 and 6 inclusive
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
# This is an XOR: exactly one of (table < harmonica) or (table < vase) is true
solver.add(Or(And(table < harmonica, Not(table < vase)), And(Not(table < harmonica), table < vase)))

# Now evaluate the multiple-choice options
found_options = []

# Option A: The mirror is auctioned on June 2nd
solver.push()
solver.add(mirror == 2)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The lamp is auctioned on June 2nd
solver.push()
solver.add(lamp == 2)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The vase is auctioned on June 2nd
solver.push()
solver.add(vase == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The lamp is auctioned on June 3rd
solver.push()
solver.add(lamp == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The mirror is auctioned on June 5th
solver.push()
solver.add(mirror == 5)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")