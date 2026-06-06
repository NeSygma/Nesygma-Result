from z3 import *

solver = Solver()

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
days = [0, 1, 2, 3, 4, 5]

# Antiques: harmonica, lamp, mirror, sundial, table, vase
# Each gets a day (0-5), all distinct
h, l, m, s, t, v = Ints('h l m s t v')

# Domain: each antique is auctioned on exactly one of the 6 days
solver.add(h >= 0, h <= 5)
solver.add(l >= 0, l <= 5)
solver.add(m >= 0, m <= 5)
solver.add(s >= 0, s <= 5)
solver.add(t >= 0, t <= 5)
solver.add(v >= 0, v <= 5)

# All distinct days
solver.add(Distinct(h, l, m, s, t, v))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(s != 0)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(h < l, m < l))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(s < m)
solver.add(s < v)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(Xor(t < h, t < v))

# Now evaluate each option
# Option A: The mirror is auctioned on June 2nd (day 1)
opt_a = (m == 1)

# Option B: The lamp is auctioned on June 2nd (day 1)
opt_b = (l == 1)

# Option C: The vase is auctioned on June 2nd (day 1)
opt_c = (v == 1)

# Option D: The lamp is auctioned on June 3rd (day 2)
opt_d = (l == 2)

# Option E: The mirror is auctioned on June 5th (day 4)
opt_e = (m == 4)

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