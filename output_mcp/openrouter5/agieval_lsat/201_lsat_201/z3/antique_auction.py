from z3 import *

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
# We'll use Int variables for each antique, representing the day (0-5)
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')

solver = Solver()

# Domain: each antique is auctioned on exactly one day from 0 to 5
antiques = [harmonica, lamp, mirror, sundial, table, vase]
for a in antiques:
    solver.add(a >= 0, a <= 5)

# All distinct: each day has exactly one antique
solver.add(Distinct(antiques))

# Condition 1: The sundial is not auctioned on June 1st (day 0).
solver.add(sundial != 0)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
# harmonica < lamp => mirror < lamp
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
# (table < harmonica) XOR (table < vase)
solver.add(Or(
    And(table < harmonica, Not(table < vase)),
    And(Not(table < harmonica), table < vase)
))

# Now evaluate each option
found_options = []

# Option A: The sundial is auctioned on June 5th (day 4).
opt_a = (sundial == 4)

# Option B: The sundial is auctioned on June 4th (day 3).
opt_b = (sundial == 3)

# Option C: The lamp is auctioned on June 5th (day 4) and the mirror is auctioned on June 6th (day 5).
opt_c = And(lamp == 4, mirror == 5)

# Option D: The table is auctioned on June 3rd (day 2) and the lamp is auctioned on June 4th (day 3).
opt_d = And(table == 2, lamp == 3)

# Option E: The harmonica is auctioned on June 2nd (day 1) and the vase is auctioned on June 3rd (day 2).
opt_e = And(harmonica == 1, vase == 2)

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