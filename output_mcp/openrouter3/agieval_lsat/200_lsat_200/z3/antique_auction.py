from z3 import *

# Create solver
solver = Solver()

# Days: 1-6
days = [1, 2, 3, 4, 5, 6]

# Antiques
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Create variables: each antique assigned to a day
assign = {antique: Int(antique) for antique in antiques}

# Domain constraints: each antique gets a unique day from 1-6
for antique in antiques:
    solver.add(assign[antique] >= 1)
    solver.add(assign[antique] <= 6)

# All antiques on different days
solver.add(Distinct([assign[antique] for antique in antiques]))

# Constraint 1: Sundial is not auctioned on June 1st
solver.add(assign["sundial"] != 1)

# Constraint 2: If harmonica < lamp, then mirror < lamp
# This is: (harmonica < lamp) => (mirror < lamp)
# In Z3: Implies(assign["harmonica"] < assign["lamp"], assign["mirror"] < assign["lamp"])
solver.add(Implies(assign["harmonica"] < assign["lamp"], assign["mirror"] < assign["lamp"]))

# Constraint 3: Sundial < mirror AND sundial < vase
solver.add(assign["sundial"] < assign["mirror"])
solver.add(assign["sundial"] < assign["vase"])

# Constraint 4: Table < harmonica XOR table < vase
# XOR means exactly one is true
table_harmonica = assign["table"] < assign["harmonica"]
table_vase = assign["table"] < assign["vase"]
solver.add(Or(table_harmonica, table_vase))  # At least one true
solver.add(Not(And(table_harmonica, table_vase)))  # Not both true

# Now test each option
found_options = []

# Option A: The mirror is auctioned on June 2nd
opt_a_constr = (assign["mirror"] == 2)

# Option B: The lamp is auctioned on June 2nd
opt_b_constr = (assign["lamp"] == 2)

# Option C: The vase is auctioned on June 2nd
opt_c_constr = (assign["vase"] == 2)

# Option D: The lamp is auctioned on June 3rd
opt_d_constr = (assign["lamp"] == 3)

# Option E: The mirror is auctioned on June 5th
opt_e_constr = (assign["mirror"] == 5)

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
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