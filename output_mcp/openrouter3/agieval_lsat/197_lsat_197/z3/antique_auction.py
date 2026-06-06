from z3 import *

# Create solver
solver = Solver()

# Define days as integers 1-6 (June 1st through June 6th)
days = [1, 2, 3, 4, 5, 6]

# Define antiques as symbolic variables representing their auction day
harmonica = Int('harmonica')
lamp = Int('lamp')
mirror = Int('mirror')
sundial = Int('sundial')
table = Int('table')
vase = Int('vase')

# All antiques must be assigned to distinct days between 1 and 6
antiques = [harmonica, lamp, mirror, sundial, table, vase]
for antique in antiques:
    solver.add(antique >= 1)
    solver.add(antique <= 6)
solver.add(Distinct(antiques))

# Base constraints from problem statement
# 1. The sundial is not auctioned on June 1st
solver.add(sundial != 1)

# 2. If the harmonica is auctioned on an earlier date than the lamp, 
#    then the mirror is also auctioned on an earlier date than the lamp
#    This is: (harmonica < lamp) => (mirror < lamp)
solver.add(Implies(harmonica < lamp, mirror < lamp))

# 3. The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase
solver.add(sundial < mirror)
solver.add(sundial < vase)

# 4. The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both
#    This is: (table < harmonica) XOR (table < vase)
#    XOR in Z3: (A and not B) or (not A and B)
solver.add(Or(And(table < harmonica, Not(table < vase)), And(Not(table < harmonica), table < vase)))

# Now evaluate each answer choice
found_options = []

# Option A: The table is auctioned on June 2nd and the lamp is auctioned on June 3rd
opt_a_constr = And(table == 2, lamp == 3)

# Option B: The sundial is auctioned on June 2nd and the vase is auctioned on June 3rd
opt_b_constr = And(sundial == 2, vase == 3)

# Option C: The mirror is auctioned on June 3rd and the sundial is auctioned on June 4th
opt_c_constr = And(mirror == 3, sundial == 4)

# Option D: The vase is auctioned on June 4th and the sundial is auctioned on June 5th
opt_d_constr = And(vase == 4, sundial == 5)

# Option E: The sundial is auctioned on June 4th and the table is auctioned on June 5th
opt_e_constr = And(sundial == 4, table == 5)

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