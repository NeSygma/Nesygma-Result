from z3 import *

# Create a solver
solver = Solver()

# Days: 0 (June 1) to 5 (June 6)
days = list(range(6))

# Antiques: 0=harmonica, 1=lamp, 2=mirror, 3=sundial, 4=table, 5=vase
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')
antiques = [harmonica, lamp, mirror, sundial, table, vase]

# Each antique is assigned to a unique day
solver.add(Distinct(antiques))
for a in antiques:
    solver.add(a >= 0, a <= 5)

# Constraint 1: The sundial is not auctioned on June 1st (day 0)
solver.add(sundial != 0)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
# This is equivalent to: harmonica < lamp implies mirror < lamp
# Which is equivalent to: harmonica >= lamp or mirror < lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both.
# This is equivalent to: (table < harmonica) XOR (table < vase)
solver.add(Xor(table < harmonica, table < vase))

# Now, for each option, check if it is IMPOSSIBLE for the antique to be auctioned on the day immediately before the vase.
# Let vase_day = vase, and the day before is vase_day - 1.
# We need to check if the antique in the option CANNOT be assigned to vase_day - 1.

impossible_options = []

# Option A: the harmonica is auctioned on the day before the vase
solver.push()
solver.add(harmonica == vase - 1)
if solver.check() == unsat:
    impossible_options.append("A")
solver.pop()

# Option B: the lamp is auctioned on the day before the vase
solver.push()
solver.add(lamp == vase - 1)
if solver.check() == unsat:
    impossible_options.append("B")
solver.pop()

# Option C: the mirror is auctioned on the day before the vase
solver.push()
solver.add(mirror == vase - 1)
if solver.check() == unsat:
    impossible_options.append("C")
solver.pop()

# Option D: the sundial is auctioned on the day before the vase
solver.push()
solver.add(sundial == vase - 1)
if solver.check() == unsat:
    impossible_options.append("D")
solver.pop()

# Option E: the table is auctioned on the day before the vase
solver.push()
solver.add(table == vase - 1)
if solver.check() == unsat:
    impossible_options.append("E")
solver.pop()

# Output the result
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")