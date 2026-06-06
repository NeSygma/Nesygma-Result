from z3 import *

# Declare the colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]

# Declare the rugs
rugs = ["rug1", "rug2", "rug3"]

# Create a solver
solver = Solver()

# For each rug and each color, a boolean variable indicating if the rug uses the color
uses = {}
for r in rugs:
    for c in colors:
        uses[(r, c)] = Bool(f"uses_{r}_{c}")

# Constraint 1: Each color is used in at most one rug
for c in colors:
    solver.add(AtMost(*[uses[(r, c)] for r in rugs], 1))

# Constraint 2: Exactly 5 colors are used in total
color_used = [Or([uses[(r, c)] for r in rugs]) for c in colors]
solver.add(Sum([If(used, 1, 0) for used in color_used]) == 5)

# Constraint 3: For each rug, if white is used, exactly 2 other colors are also used
for r in rugs:
    white_used = uses[(r, "white")]
    other_colors_used = [uses[(r, c)] for c in colors if c != "white"]
    solver.add(Implies(white_used, Sum([If(used, 1, 0) for used in other_colors_used]) == 2))

# Constraint 4: If olive is used in a rug, peach must also be used in that rug
for r in rugs:
    olive_used = uses[(r, "olive")]
    peach_used = uses[(r, "peach")]
    solver.add(Implies(olive_used, peach_used))

# Constraint 5: Forest and turquoise are not used together in a rug
for r in rugs:
    forest_used = uses[(r, "forest")]
    turquoise_used = uses[(r, "turquoise")]
    solver.add(Not(And(forest_used, turquoise_used)))

# Constraint 6: Peach and turquoise are not used together in a rug
for r in rugs:
    peach_used = uses[(r, "peach")]
    turquoise_used = uses[(r, "turquoise")]
    solver.add(Not(And(peach_used, turquoise_used)))

# Constraint 7: Peach and yellow are not used together in a rug
for r in rugs:
    peach_used = uses[(r, "peach")]
    yellow_used = uses[(r, "yellow")]
    solver.add(Not(And(peach_used, yellow_used)))

# Define constraints for each option
opt_a_constr = And(
    # Rug1: forest only
    uses[("rug1", "forest")],
    Not(uses[("rug1", "olive")]),
    Not(uses[("rug1", "peach")]),
    Not(uses[("rug1", "turquoise")]),
    Not(uses[("rug1", "white")]),
    Not(uses[("rug1", "yellow")]),
    # Rug2: turquoise only
    uses[("rug2", "turquoise")],
    Not(uses[("rug2", "forest")]),
    Not(uses[("rug2", "olive")]),
    Not(uses[("rug2", "peach")]),
    Not(uses[("rug2", "white")]),
    Not(uses[("rug2", "yellow")]),
    # Rug3: olive, peach, and white
    uses[("rug3", "olive")],
    uses[("rug3", "peach")],
    uses[("rug3", "white")],
    Not(uses[("rug3", "forest")]),
    Not(uses[("rug3", "turquoise")]),
    Not(uses[("rug3", "yellow")])
)

opt_b_constr = And(
    # Rug1: forest only
    uses[("rug1", "forest")],
    Not(uses[("rug1", "olive")]),
    Not(uses[("rug1", "peach")]),
    Not(uses[("rug1", "turquoise")]),
    Not(uses[("rug1", "white")]),
    Not(uses[("rug1", "yellow")]),
    # Rug2: turquoise only
    uses[("rug2", "turquoise")],
    Not(uses[("rug2", "forest")]),
    Not(uses[("rug2", "olive")]),
    Not(uses[("rug2", "peach")]),
    Not(uses[("rug2", "white")]),
    Not(uses[("rug2", "yellow")]),
    # Rug3: olive, peach, and yellow
    uses[("rug3", "olive")],
    uses[("rug3", "peach")],
    uses[("rug3", "yellow")],
    Not(uses[("rug3", "forest")]),
    Not(uses[("rug3", "turquoise")]),
    Not(uses[("rug3", "white")])
)

opt_c_constr = And(
    # Rug1: peach only
    uses[("rug1", "peach")],
    Not(uses[("rug1", "forest")]),
    Not(uses[("rug1", "olive")]),
    Not(uses[("rug1", "turquoise")]),
    Not(uses[("rug1", "white")]),
    Not(uses[("rug1", "yellow")]),
    # Rug2: turquoise only
    uses[("rug2", "turquoise")],
    Not(uses[("rug2", "forest")]),
    Not(uses[("rug2", "olive")]),
    Not(uses[("rug2", "peach")]),
    Not(uses[("rug2", "white")]),
    Not(uses[("rug2", "yellow")]),
    # Rug3: forest, olive, and white
    uses[("rug3", "forest")],
    uses[("rug3", "olive")],
    uses[("rug3", "white")],
    Not(uses[("rug3", "peach")]),
    Not(uses[("rug3", "turquoise")]),
    Not(uses[("rug3", "yellow")])
)

opt_d_constr = And(
    # Rug1: yellow only
    uses[("rug1", "yellow")],
    Not(uses[("rug1", "forest")]),
    Not(uses[("rug1", "olive")]),
    Not(uses[("rug1", "peach")]),
    Not(uses[("rug1", "turquoise")]),
    Not(uses[("rug1", "white")]),
    # Rug2: forest and turquoise
    uses[("rug2", "forest")],
    uses[("rug2", "turquoise")],
    Not(uses[("rug2", "olive")]),
    Not(uses[("rug2", "peach")]),
    Not(uses[("rug2", "white")]),
    Not(uses[("rug2", "yellow")]),
    # Rug3: olive and peach
    uses[("rug3", "olive")],
    uses[("rug3", "peach")],
    Not(uses[("rug3", "forest")]),
    Not(uses[("rug3", "turquoise")]),
    Not(uses[("rug3", "white")]),
    Not(uses[("rug3", "yellow")])
)

opt_e_constr = And(
    # Rug1: yellow only
    uses[("rug1", "yellow")],
    Not(uses[("rug1", "forest")]),
    Not(uses[("rug1", "olive")]),
    Not(uses[("rug1", "peach")]),
    Not(uses[("rug1", "turquoise")]),
    Not(uses[("rug1", "white")]),
    # Rug2: olive and peach
    uses[("rug2", "olive")],
    uses[("rug2", "peach")],
    Not(uses[("rug2", "forest")]),
    Not(uses[("rug2", "turquoise")]),
    Not(uses[("rug2", "white")]),
    Not(uses[("rug2", "yellow")]),
    # Rug3: turquoise and white
    uses[("rug3", "turquoise")],
    uses[("rug3", "white")],
    Not(uses[("rug3", "forest")]),
    Not(uses[("rug3", "olive")]),
    Not(uses[("rug3", "peach")]),
    Not(uses[("rug3", "yellow")])
)

# Now, evaluate each multiple-choice option
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