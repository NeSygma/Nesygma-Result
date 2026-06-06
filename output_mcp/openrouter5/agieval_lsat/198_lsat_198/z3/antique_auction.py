from z3 import *

# Days: June 1 = 0, June 2 = 1, ..., June 6 = 5
# We'll use Int variables for each antique, values 0..5, all distinct.

solver = Solver()

# Variables
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

antiques = [harmonica, lamp, mirror, sundial, table, vase]

# Domain: each day 0..5
for a in antiques:
    solver.add(a >= 0, a <= 5)

# All distinct days
solver.add(Distinct(antiques))

# Constraints:

# 1. The sundial is not auctioned on June 1st.
solver.add(sundial != 0)

# 2. If the harmonica is auctioned on an earlier date than the lamp,
#    then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(harmonica < lamp, mirror < lamp))

# 3. The sundial is auctioned on an earlier date than the mirror
#    and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# 4. The table is auctioned on an earlier date than the harmonica
#    or on an earlier date than the vase, but not both.
# (table < harmonica) XOR (table < vase)
solver.add(If(table < harmonica, 1, 0) + If(table < vase, 1, 0) == 1)

# Additional condition from the question:
# "If the table is auctioned on a date that is later than both the date
#  on which the mirror is auctioned and the date on which the vase is auctioned"
solver.add(table > mirror)
solver.add(table > vase)

# Now evaluate each option
options = []

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