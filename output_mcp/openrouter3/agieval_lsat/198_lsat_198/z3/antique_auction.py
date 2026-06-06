from z3 import *

# Create solver
solver = Solver()

# Days: 1 through 6
days = [1, 2, 3, 4, 5, 6]

# Antiques
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Create assignment variables: each antique gets a day
assign = {antique: Int(antique) for antique in antiques}

# Each antique gets a day between 1 and 6
for antique in antiques:
    solver.add(assign[antique] >= 1)
    solver.add(assign[antique] <= 6)

# All antiques get different days (exactly one per day)
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
solver.add(Or(table_harmonica, table_vase))  # At least one is true
solver.add(Not(And(table_harmonica, table_vase)))  # Not both are true

# Additional condition for the question: Table > mirror AND table > vase
solver.add(assign["table"] > assign["mirror"])
solver.add(assign["table"] > assign["vase"])

# Now evaluate each answer choice
found_options = []

# Option A: The harmonica is auctioned on an earlier date than the table
opt_a_constr = assign["harmonica"] < assign["table"]

# Option B: The table is auctioned on an earlier date than the lamp
opt_b_constr = assign["table"] < assign["lamp"]

# Option C: The table is auctioned on an earlier date than the sundial
opt_c_constr = assign["table"] < assign["sundial"]

# Option D: The mirror is auctioned on an earlier date than the vase
opt_d_constr = assign["mirror"] < assign["vase"]

# Option E: The sundial is auctioned on an earlier date than the lamp
opt_e_constr = assign["sundial"] < assign["lamp"]

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