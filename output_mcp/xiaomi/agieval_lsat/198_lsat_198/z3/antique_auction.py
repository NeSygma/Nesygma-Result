from z3 import *

solver = Solver()

# Variables: day each antique is auctioned (1-6)
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

antiques = [harmonica, lamp, mirror, sundial, table, vase]

# Each antique is auctioned on a day 1-6, all different
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(sundial != 1)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(Xor(table < harmonica, table < vase))

# Additional condition from the question:
# The table is auctioned on a date that is later than both the date on which
# the mirror is auctioned and the date on which the vase is auctioned.
solver.add(table > mirror)
solver.add(table > vase)

# Define option constraints
# (A) The harmonica is auctioned on an earlier date than the table.
opt_a = harmonica < table

# (B) The table is auctioned on an earlier date than the lamp.
opt_b = table < lamp

# (C) The table is auctioned on an earlier date than the sundial.
opt_c = table < sundial

# (D) The mirror is auctioned on an earlier date than the vase.
opt_d = mirror < vase

# (E) The sundial is auctioned on an earlier date than the lamp.
opt_e = sundial < lamp

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