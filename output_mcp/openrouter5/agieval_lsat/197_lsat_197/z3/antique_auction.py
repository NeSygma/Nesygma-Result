from z3 import *

solver = Solver()

# Days: June 1st = 0, June 2nd = 1, ..., June 6th = 5
days = list(range(6))  # 0..5

# Variables: each antique gets a day (0-5)
harmonica, lamp, mirror, sundial, table, vase = Ints('harmonica lamp mirror sundial table vase')

# Domain: each antique is assigned a distinct day from 0 to 5
antiques = [harmonica, lamp, mirror, sundial, table, vase]
for a in antiques:
    solver.add(a >= 0, a <= 5)
solver.add(Distinct(antiques))

# Condition 1: The sundial is not auctioned on June 1st.
solver.add(sundial != 0)

# Condition 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Condition 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Condition 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(If(table < harmonica, 1, 0) + If(table < vase, 1, 0) == 1)

# Now evaluate each option
# Option A: The table is auctioned on June 2nd (day 1) and the lamp is auctioned on June 3rd (day 2).
opt_a_constr = And(table == 1, lamp == 2)

# Option B: The sundial is auctioned on June 2nd (day 1) and the vase is auctioned on June 3rd (day 2).
opt_b_constr = And(sundial == 1, vase == 2)

# Option C: The mirror is auctioned on June 3rd (day 2) and the sundial is auctioned on June 4th (day 3).
opt_c_constr = And(mirror == 2, sundial == 3)

# Option D: The vase is auctioned on June 4th (day 3) and the sundial is auctioned on June 5th (day 4).
opt_d_constr = And(vase == 3, sundial == 4)

# Option E: The sundial is auctioned on June 4th (day 3) and the table is auctioned on June 5th (day 4).
opt_e_constr = And(sundial == 3, table == 4)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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