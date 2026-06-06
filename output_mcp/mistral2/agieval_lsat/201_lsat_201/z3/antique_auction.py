from z3 import *

solver = Solver()

# Days are June 1st (0) to June 6th (5)
days = list(range(6))

# Antiques to be auctioned
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Assign each antique to a day (0-5)
assignment = {a: Int(f"day_{a}") for a in antiques}

# Each antique is auctioned on exactly one day
for a in antiques:
    solver.add(And(assignment[a] >= 0, assignment[a] < 6))

# All antiques are auctioned on distinct days
solver.add(Distinct(list(assignment.values())))

# Constraint 1: The sundial is not auctioned on June 1st (day 0)
solver.add(assignment["sundial"] != 0)

# Constraint 2: If the harmonica is auctioned on an earlier date than the lamp,
# then the mirror is also auctioned on an earlier date than the lamp.
# This is equivalent to: harmonica < lamp implies mirror < lamp
# Which is equivalent to: harmonica >= lamp or mirror < lamp
solver.add(Implies(assignment["harmonica"] < assignment["lamp"], 
                   assignment["mirror"] < assignment["lamp"]))

# Constraint 3: The sundial is auctioned on an earlier date than the mirror and also on an earlier date than the vase.
solver.add(assignment["sundial"] < assignment["mirror"])
solver.add(assignment["sundial"] < assignment["vase"])

# Constraint 4: The table is auctioned on an earlier date than the harmonica or on an earlier date than the vase, but not both.
# This is equivalent to: (table < harmonica) XOR (table < vase)
solver.add(Xor(assignment["table"] < assignment["harmonica"], 
               assignment["table"] < assignment["vase"]))

# Base constraints are set. Now evaluate each option.

# Option A: The sundial is auctioned on June 5th (day 4)
opt_a_constr = (assignment["sundial"] == 4)

# Option B: The sundial is auctioned on June 4th (day 3)
opt_b_constr = (assignment["sundial"] == 3)

# Option C: The lamp is auctioned on June 5th (day 4) and the mirror is auctioned on June 6th (day 5)
opt_c_constr = And(assignment["lamp"] == 4, assignment["mirror"] == 5)

# Option D: The table is auctioned on June 3rd (day 2) and the lamp is auctioned on June 4th (day 3)
opt_d_constr = And(assignment["table"] == 2, assignment["lamp"] == 3)

# Option E: The harmonica is auctioned on June 2nd (day 1) and the vase is auctioned on June 3rd (day 2)
opt_e_constr = And(assignment["harmonica"] == 1, assignment["vase"] == 2)

# Evaluate each option
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