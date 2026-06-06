from z3 import *

# Six colors: forest, olive, peach, turquoise, white, yellow
# Exactly 5 of the 6 colors are used.
# Each used color is used in exactly one rug.
# Three rugs: rug0, rug1, rug2
# Each rug is either solid (one color) or multicolored (multiple colors).
# If white is used in a rug, that rug has exactly 3 colors (white + 2 others).
# If olive is used in a rug, peach is also used in that rug.
# Forest and turquoise are not together in a rug.
# Peach and turquoise are not together in a rug.
# Peach and yellow are not together in a rug.

# Additional condition: One of the rugs is solid yellow.

# We need to find which option CANNOT be true (i.e., is impossible) given the condition.

colors = ["F", "O", "P", "T", "W", "Y"]
assign = {c: Int(f"assign_{c}") for c in colors}

solver = Solver()

# Domain: each color assigned to rug 0,1,2 or unused (3)
for c in colors:
    solver.add(assign[c] >= 0, assign[c] <= 3)

# Exactly 5 colors used, so exactly one color is unused (assigned to 3)
solver.add(Sum([If(assign[c] == 3, 1, 0) for c in colors]) == 1)

# Rule: If white is used in a rug, that rug has exactly 3 colors (white + 2 others).
for r in range(3):
    count_in_rug_r = Sum([If(assign[c] == r, 1, 0) for c in colors])
    solver.add(Implies(assign["W"] == r, count_in_rug_r == 3))

# Rule: If olive is used in a rug, peach is also used in that rug.
for r in range(3):
    solver.add(Implies(assign["O"] == r, assign["P"] == r))

# Rule: Forest and turquoise are not together in a rug.
for r in range(3):
    solver.add(Not(And(assign["F"] == r, assign["T"] == r)))

# Rule: Peach and turquoise are not together in a rug.
for r in range(3):
    solver.add(Not(And(assign["P"] == r, assign["T"] == r)))

# Rule: Peach and yellow are not together in a rug.
for r in range(3):
    solver.add(Not(And(assign["P"] == r, assign["Y"] == r)))

# Additional condition: One of the rugs is solid yellow.
# Solid yellow means yellow is used and its rug has only yellow.
solver.add(assign["Y"] != 3)  # yellow is used
# The rug containing yellow has only yellow in it.
solver.add(Sum([If(assign[c] == assign["Y"], 1, 0) for c in colors]) == 1)

# Let's first check if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    for c in colors:
        print(f"  {c}: rug {m[assign[c]]}")
else:
    print("Base constraints are UNSAT!")
    exit()

# Now evaluate each option.

# Option A: There is exactly one solid color rug.
# A solid color rug is a rug with exactly 1 color.
opt_a = Sum([If(Sum([If(assign[c] == r, 1, 0) for c in colors]) == 1, 1, 0) for r in range(3)]) == 1

# Option B: One of the rugs is solid forest.
opt_b = And(assign["F"] != 3, Sum([If(assign[c] == assign["F"], 1, 0) for c in colors]) == 1)

# Option C: Turquoise is not used in any of the rugs.
opt_c = assign["T"] == 3

# Option D: Forest and olive are used together in a rug.
opt_d = Or([And(assign["F"] == r, assign["O"] == r) for r in range(3)])

# Option E: Peach and white are used together in a rug.
opt_e = Or([And(assign["P"] == r, assign["W"] == r) for r in range(3)])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    print(f"Option {letter}: {res}")
    if res == sat:
        found_options.append(letter)
    solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")