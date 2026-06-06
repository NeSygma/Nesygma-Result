from z3 import *

# Days: 1 to 6
days = [1, 2, 3, 4, 5, 6]

# Antiques
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Create variables: day assigned to each antique
day_of = {antique: Int(f"day_{antique}") for antique in antiques}

solver = Solver()

# Domain constraints: each antique gets a unique day between 1 and 6
for antique in antiques:
    solver.add(day_of[antique] >= 1)
    solver.add(day_of[antique] <= 6)

# All antiques on different days
solver.add(Distinct([day_of[antique] for antique in antiques]))

# Constraint 1: Sundial is not auctioned on June 1st
solver.add(day_of["sundial"] != 1)

# Constraint 2: If harmonica < lamp then mirror < lamp
solver.add(Or(day_of["harmonica"] >= day_of["lamp"], day_of["mirror"] < day_of["lamp"]))

# Constraint 3: Sundial < mirror AND sundial < vase
solver.add(day_of["sundial"] < day_of["mirror"])
solver.add(day_of["sundial"] < day_of["vase"])

# Constraint 4: Table < harmonica XOR table < vase
table_harmonica = day_of["table"] < day_of["harmonica"]
table_vase = day_of["table"] < day_of["vase"]
solver.add(Or(table_harmonica, table_vase))  # At least one
solver.add(Not(And(table_harmonica, table_vase)))  # Not both

# Now test each option: which antique CANNOT be immediately before the vase?
# We test if it's POSSIBLE for each antique to be immediately before the vase.
# If it's IMPOSSIBLE (unsat), then that's the answer.

# Base constraints are already added. Now test each option.
impossible_options = []

# Option A: harmonica immediately before vase
opt_a_constr = day_of["harmonica"] == day_of["vase"] - 1

# Option B: lamp immediately before vase
opt_b_constr = day_of["lamp"] == day_of["vase"] - 1

# Option C: mirror immediately before vase
opt_c_constr = day_of["mirror"] == day_of["vase"] - 1

# Option D: sundial immediately before vase
opt_d_constr = day_of["sundial"] == day_of["vase"] - 1

# Option E: table immediately before vase
opt_e_constr = day_of["table"] == day_of["vase"] - 1

for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

# According to the problem, exactly one option CANNOT be immediately before the vase
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")