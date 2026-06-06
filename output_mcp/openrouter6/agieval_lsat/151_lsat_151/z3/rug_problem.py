from z3 import *

# Define colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_index = {c: i for i, c in enumerate(colors)}

# Rugs: 0, 1, 2
num_rugs = 3

# Boolean variables: rug_color[i][c] is True if rug i uses color c
rug_color = [[Bool(f"rug_{i}_{c}") for c in colors] for i in range(num_rugs)]

solver = Solver()

# Constraint: Each color is used in at most one rug (exactly one if used)
for c in colors:
    # Sum over rugs of rug_color[i][c] should be 0 or 1
    solver.add(Sum([If(rug_color[i][c], 1, 0) for i in range(num_rugs)]) <= 1)

# Constraint: Exactly five colors are used
used_color = [Bool(f"used_{c}") for c in colors]
for idx, c in enumerate(colors):
    # used_color[c] is true if at least one rug uses it
    solver.add(used_color[idx] == Or([rug_color[i][c] for i in range(num_rugs)]))
solver.add(Sum([If(uc, 1, 0) for uc in used_color]) == 5)

# Rule 1: If white is used in a rug, that rug has exactly three colors
for i in range(num_rugs):
    white_idx = color_index["white"]
    solver.add(Implies(rug_color[i][white_idx],
                       Sum([If(rug_color[i][c], 1, 0) for c in colors]) == 3))

# Rule 2: If olive is used in a rug, peach is also used in that rug
olive_idx = color_index["olive"]
peach_idx = color_index["peach"]
for i in range(num_rugs):
    solver.add(Implies(rug_color[i][olive_idx], rug_color[i][peach_idx]))

# Rule 3: Forest and turquoise not together
forest_idx = color_index["forest"]
turquoise_idx = color_index["turquoise"]
for i in range(num_rugs):
    solver.add(Not(And(rug_color[i][forest_idx], rug_color[i][turquoise_idx])))

# Rule 4: Peach and turquoise not together
for i in range(num_rugs):
    solver.add(Not(And(rug_color[i][peach_idx], rug_color[i][turquoise_idx])))

# Rule 5: Peach and yellow not together
yellow_idx = color_index["yellow"]
for i in range(num_rugs):
    solver.add(Not(And(rug_color[i][peach_idx], rug_color[i][yellow_idx])))

# Condition: One rug is solid peach
# Find a rug that is solid peach: that rug has peach and no other colors
solid_peach_exists = False
for i in range(num_rugs):
    # This rug has peach and no other colors
    has_peach = rug_color[i][peach_idx]
    no_other_colors = And([Not(rug_color[i][c]) for c in colors if c != "peach"])
    solver.add(Implies(has_peach, no_other_colors))
    # Also, peach must be used in exactly one rug (already enforced by sum <=1)
    # We'll ensure that at least one rug is solid peach by adding a constraint that there exists such a rug
    # But we can just assert that there is a rug with peach and no other colors
    # We'll do it by asserting that for the rug with peach, it has no other colors.
    # However, we need to ensure that exactly one rug has peach. That's already enforced.
    # So we can add: there exists a rug i such that rug_color[i][peach_idx] and for all c != peach, not rug_color[i][c].
    # We'll add this as a constraint for each rug? Actually, we can add a constraint that for the rug that has peach, it has no other colors.
    # Since we don't know which rug has peach, we can use an OR over rugs.
    # But we can simply add: for each rug, if it has peach, then it has no other colors. That's what we did above.
    # That ensures that any rug with peach is solid peach.
    # But we also need to ensure that there is at least one rug with peach. That's already implied by the condition that peach is used (since exactly five colors are used, and peach is one of them).
    # So we don't need an extra constraint.

# Now, we need to check each option for entailment.
# We'll use the theorem proving pattern: for each option, check if the negation is unsatisfiable given the premises.

options = [
    ("A", "One of the rugs is solid forest."),
    ("B", "One of the rugs is solid turquoise."),
    ("C", "One of the rugs is solid yellow."),
    ("D", "Forest and white are used together in a rug."),
    ("E", "White and yellow are used together in a rug.")
]

# We'll encode each option as a Z3 constraint
opt_constraints = []

# Option A: One of the rugs is solid forest.
# That means there exists a rug i such that rug_color[i][forest_idx] is true and for all other colors c != forest, rug_color[i][c] is false.
opt_a = Or([And(rug_color[i][forest_idx],
                *[Not(rug_color[i][c]) for c in colors if c != "forest"])
            for i in range(num_rugs)])
opt_constraints.append(("A", opt_a))

# Option B: One of the rugs is solid turquoise.
opt_b = Or([And(rug_color[i][turquoise_idx],
                *[Not(rug_color[i][c]) for c in colors if c != "turquoise"])
            for i in range(num_rugs)])
opt_constraints.append(("B", opt_b))

# Option C: One of the rugs is solid yellow.
opt_c = Or([And(rug_color[i][yellow_idx],
                *[Not(rug_color[i][c]) for c in colors if c != "yellow"])
            for i in range(num_rugs)])
opt_constraints.append(("C", opt_c))

# Option D: Forest and white are used together in a rug.
opt_d = Or([And(rug_color[i][forest_idx], rug_color[i][white_idx])
            for i in range(num_rugs)])
opt_constraints.append(("D", opt_d))

# Option E: White and yellow are used together in a rug.
opt_e = Or([And(rug_color[i][white_idx], rug_color[i][yellow_idx])
            for i in range(num_rugs)])
opt_constraints.append(("E", opt_e))

# Now, for each option, check if the negation is unsatisfiable.
# If the negation is unsat, then the option must be true.
found_options = []
for letter, opt_constr in opt_constraints:
    s = Solver()
    s.add(solver.assertions())  # Add all base constraints
    s.add(Not(opt_constr))      # Add negation of the option
    if s.check() == unsat:
        found_options.append(letter)

# According to the theorem proving pattern, we print STATUS: proved if we have a definitive answer.
# But the user asked for the multiple choice skeleton. However, we are using theorem proving.
# We'll print the answer in the required format for multiple choice.
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")