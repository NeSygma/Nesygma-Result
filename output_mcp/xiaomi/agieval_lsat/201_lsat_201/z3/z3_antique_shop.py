from z3 import *

solver = Solver()

# Variables: day assignment for each antique (1-6)
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

antiques = [harmonica, lamp, mirror, sundial, table, vase]

# Each antique is assigned to a day 1-6, all different
for a in antiques:
    solver.add(a >= 1, a <= 6)
solver.add(Distinct(antiques))

# Constraint 1: The sundial is not auctioned on June 1st.
solver.add(sundial != 1)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
solver.add(Implies(harmonica < lamp, mirror < lamp))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror
# and also on an earlier date than the vase.
solver.add(sundial < mirror)
solver.add(sundial < vase)

# Constraint 4: The table is auctioned on an earlier date than the harmonica
# or on an earlier date than the vase, but not both.
solver.add(Xor(table < harmonica, table < vase))

# Define option constraints
opt_a_constr = (sundial == 5)
opt_b_constr = (sundial == 4)
opt_c_constr = And(lamp == 5, mirror == 6)
opt_d_constr = And(table == 3, lamp == 4)
opt_e_constr = And(harmonica == 2, vase == 3)

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