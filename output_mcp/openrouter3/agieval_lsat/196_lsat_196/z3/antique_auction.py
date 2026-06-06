from z3 import *

# Create solver
solver = Solver()

# Days: 1 to 6 (June 1st to June 6th)
days = [1, 2, 3, 4, 5, 6]

# Antiques
antiques = ["harmonica", "lamp", "mirror", "sundial", "table", "vase"]

# Create position variables for each antique (which day they are auctioned)
pos = {antique: Int(f"pos_{antique}") for antique in antiques}

# Each antique gets a unique day from 1 to 6
for antique in antiques:
    solver.add(pos[antique] >= 1, pos[antique] <= 6)

# All antiques must be on different days
solver.add(Distinct([pos[antique] for antique in antiques]))

# Base constraints from problem statement
# 1. Sundial is not auctioned on June 1st
solver.add(pos["sundial"] != 1)

# 2. If harmonica is earlier than lamp, then mirror is also earlier than lamp
# This is: (pos_harmonica < pos_lamp) => (pos_mirror < pos_lamp)
solver.add(Implies(pos["harmonica"] < pos["lamp"], pos["mirror"] < pos["lamp"]))

# 3. Sundial is earlier than mirror AND earlier than vase
solver.add(pos["sundial"] < pos["mirror"])
solver.add(pos["sundial"] < pos["vase"])

# 4. Table is earlier than harmonica OR earlier than vase, but not both
# This means: (pos_table < pos_harmonica) XOR (pos_table < pos_vase)
# XOR can be expressed as: (A OR B) AND NOT(A AND B)
solver.add(Or(pos["table"] < pos["harmonica"], pos["table"] < pos["vase"]))
solver.add(Not(And(pos["table"] < pos["harmonica"], pos["table"] < pos["vase"])))

# Now test each answer choice
# Each choice gives a specific order from June 1st to June 6th
# We need to check if that order satisfies all constraints

# Define the options as constraints that the positions must match the given order
opt_a_constr = And(
    pos["harmonica"] == 1,
    pos["table"] == 2,
    pos["sundial"] == 3,
    pos["lamp"] == 4,
    pos["vase"] == 5,
    pos["mirror"] == 6
)

opt_b_constr = And(
    pos["lamp"] == 1,
    pos["harmonica"] == 2,
    pos["sundial"] == 3,
    pos["mirror"] == 4,
    pos["vase"] == 5,
    pos["table"] == 6
)

opt_c_constr = And(
    pos["harmonica"] == 1,
    pos["sundial"] == 2,
    pos["table"] == 3,
    pos["mirror"] == 4,
    pos["lamp"] == 5,
    pos["vase"] == 6
)

opt_d_constr = And(
    pos["sundial"] == 1,
    pos["mirror"] == 2,
    pos["harmonica"] == 3,
    pos["table"] == 4,
    pos["vase"] == 5,
    pos["lamp"] == 6
)

opt_e_constr = And(
    pos["vase"] == 1,
    pos["sundial"] == 2,
    pos["lamp"] == 3,
    pos["harmonica"] == 4,
    pos["table"] == 5,
    pos["mirror"] == 6
)

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")