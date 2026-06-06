from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Declare symbolic variables for each antique's auction day (0=June 1, 1=June 2, ..., 5=June 6)
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# Each antique is auctioned on a distinct day
solver = Solver()
solver.add(Distinct(harmonica, lamp, mirror, sundial, table, vase))

# Constraint 1: The sundial is not auctioned on June 1st (day 0)
solver.add(sundial != 0)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp, then the mirror is also auctioned on an earlier date than the lamp.
# This is equivalent to: harmonica < lamp implies mirror < lamp
# Which is equivalent to: harmonica >= lamp or mirror < lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both.
# This is equivalent to: (table < harmonica) XOR (table < vase)
# Which is equivalent to: (table < harmonica and table >= vase) or (table >= harmonica and table < vase)
solver.add(Or(And(table < harmonica, table >= vase), And(table >= harmonica, table < vase)))

# Base constraints for day bounds (0 to 5)
solver.add(harmonica >= 0, harmonica <= 5)
solver.add(lamp >= 0, lamp <= 5)
solver.add(mirror >= 0, mirror <= 5)
solver.add(sundial >= 0, sundial <= 5)
solver.add(table >= 0, table <= 5)
solver.add(vase >= 0, vase <= 5)

# Now, evaluate each option
found_options = []

# Option A: harmonica, table, sundial, lamp, vase, mirror
solver.push()
solver.add(harmonica == 0)
solver.add(table == 1)
solver.add(sundial == 2)
solver.add(lamp == 3)
solver.add(vase == 4)
solver.add(mirror == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: lamp, harmonica, sundial, mirror, vase, table
solver.push()
solver.add(lamp == 0)
solver.add(harmonica == 1)
solver.add(sundial == 2)
solver.add(mirror == 3)
solver.add(vase == 4)
solver.add(table == 5)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: harmonica, sundial, table, mirror, lamp, vase
solver.push()
solver.add(harmonica == 0)
solver.add(sundial == 1)
solver.add(table == 2)
solver.add(mirror == 3)
solver.add(lamp == 4)
solver.add(vase == 5)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: sundial, mirror, harmonica, table, vase, lamp
solver.push()
solver.add(sundial == 0)
solver.add(mirror == 1)
solver.add(harmonica == 2)
solver.add(table == 3)
solver.add(vase == 4)
solver.add(lamp == 5)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: vase, sundial, lamp, harmonica, table, mirror
solver.push()
solver.add(vase == 0)
solver.add(sundial == 1)
solver.add(lamp == 2)
solver.add(harmonica == 3)
solver.add(table == 4)
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