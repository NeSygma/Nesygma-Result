from z3 import *

# Define colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_to_idx = {c: i for i, c in enumerate(colors)}
num_colors = len(colors)

# Number of rugs
num_rugs = 3

# Create solver
solver = Solver()

# Decision variables:
# used_in_rug[i][c]: True if color c is used in rug i
used_in_rug = [[Bool(f"used_in_rug_{i}_{c}") for c in colors] for i in range(num_rugs)]

# is_solid[i]: True if rug i is solid (exactly one color)
is_solid = [Bool(f"is_solid_{i}") for i in range(num_rugs)]

# is_multicolored[i]: True if rug i is multicolored (at least two colors)
is_multicolored = [Bool(f"is_multicolored_{i}") for i in range(num_rugs)]

# color_used[c]: True if color c is used in any rug
color_used = [Bool(f"color_used_{c}") for c in colors]

# Exactly one rug is solid peach (given condition)
# We'll fix rug0 to be solid peach
solver.add(is_solid[0])
peach_idx = color_to_idx["peach"]
solver.add(used_in_rug[0][peach_idx])
# Ensure no other colors in rug0
for c_idx in range(num_colors):
    if c_idx != peach_idx:
        solver.add(Not(used_in_rug[0][c_idx]))

# Each rug is either solid or multicolored, but not both
for i in range(num_rugs):
    solver.add(Xor(is_solid[i], is_multicolored[i]))

# If a rug is solid, exactly one color is used
for i in range(num_rugs):
    colors_in_rug = [used_in_rug[i][c_idx] for c_idx in range(num_colors)]
    solver.add(Implies(is_solid[i], And(
        Or(colors_in_rug),
        And([Not(And(colors_in_rug[j], colors_in_rug[k])) for j in range(num_colors) for k in range(j+1, num_colors)])
    )))

# If a rug is multicolored, at least two colors are used
for i in range(num_rugs):
    solver.add(Implies(is_multicolored[i], Or([
        And(used_in_rug[i][c1_idx], used_in_rug[i][c2_idx])
        for c1_idx in range(num_colors) for c2_idx in range(c1_idx+1, num_colors)
    ])))

# Each color used is used in only one rug (implied by the way we model)
# But we need to ensure that if a color is used in a rug, it's counted in color_used
for c_idx in range(num_colors):
    c = colors[c_idx]
    solver.add(Implies(color_used[c_idx], Or([used_in_rug[i][c_idx] for i in range(num_rugs)])))
    solver.add(Implies(Not(color_used[c_idx]), And([Not(used_in_rug[i][c_idx]) for i in range(num_rugs)])))

# Exactly 5 colors are used
solver.add(Sum(color_used) == 5)

# Constraints on color usage:

# 1. In any rug in which white is used, two other colors are also used.
# This means white can only appear in multicolored rugs with at least two other colors.
for i in range(num_rugs):
    white_idx = color_to_idx["white"]
    white_used = used_in_rug[i][white_idx]
    # If white is used, at least two other colors must be used in the same rug
    other_colors = [used_in_rug[i][c_idx] for c_idx in range(num_colors) if c_idx != white_idx]
    # At least two other colors must be True
    solver.add(Implies(white_used, Sum(other_colors) >= 2))

# 2. In any rug in which olive is used, peach is also used.
for i in range(num_rugs):
    olive_idx = color_to_idx["olive"]
    peach_idx = color_to_idx["peach"]
    olive_used = used_in_rug[i][olive_idx]
    peach_used = used_in_rug[i][peach_idx]
    solver.add(Implies(olive_used, peach_used))

# 3. Forest and turquoise are not used together in a rug.
for i in range(num_rugs):
    forest_idx = color_to_idx["forest"]
    turquoise_idx = color_to_idx["turquoise"]
    forest_used = used_in_rug[i][forest_idx]
    turquoise_used = used_in_rug[i][turquoise_idx]
    solver.add(Not(And(forest_used, turquoise_used)))

# 4. Peach and turquoise are not used together in a rug.
for i in range(num_rugs):
    peach_idx = color_to_idx["peach"]
    turquoise_idx = color_to_idx["turquoise"]
    peach_used = used_in_rug[i][peach_idx]
    turquoise_used = used_in_rug[i][turquoise_idx]
    solver.add(Not(And(peach_used, turquoise_used)))

# 5. Peach and yellow are not used together in a rug.
for i in range(num_rugs):
    peach_idx = color_to_idx["peach"]
    yellow_idx = color_to_idx["yellow"]
    peach_used = used_in_rug[i][peach_idx]
    yellow_used = used_in_rug[i][yellow_idx]
    solver.add(Not(And(peach_used, yellow_used)))

# Now, we need to find all valid models that satisfy the base constraints and the solid peach condition.
# We will collect the truth values of the options in these models.

# Options to check
options = {
    "A": Or([And(is_solid[i], used_in_rug[i][color_to_idx["forest"]]) for i in range(num_rugs)]),
    "B": Or([And(is_solid[i], used_in_rug[i][color_to_idx["turquoise"]]) for i in range(num_rugs)]),
    "C": Or([And(is_solid[i], used_in_rug[i][color_to_idx["yellow"]]) for i in range(num_rugs)]),
    "D": Or([And(used_in_rug[i][color_to_idx["forest"]], used_in_rug[i][color_to_idx["white"]]) for i in range(num_rugs)]),
    "E": Or([And(used_in_rug[i][color_to_idx["white"]], used_in_rug[i][color_to_idx["yellow"]]) for i in range(num_rugs)])
}

# Collect models
models = []
while len(models) < 2 and solver.check() == sat:
    model = solver.model()
    models.append(model)
    # Block the current model
    solver.add(Or([v() != model[v] for v in model.decls()]))

# If we have at least two models, check which options are true in all of them
if len(models) >= 2:
    must_be_true = []
    for letter, opt in options.items():
        true_in_all = True
        for model in models:
            if not is_true(model.eval(opt, model_completion=True)):
                true_in_all = False
                break
        if true_in_all:
            must_be_true.append(letter)
    
    if len(must_be_true) == 1:
        print("STATUS: sat")
        print(f"answer:{must_be_true[0]}")
    elif len(must_be_true) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options must be true {must_be_true}")
    else:
        print("STATUS: unsat")
        print("Refine: No options must be true")
else:
    print("STATUS: unknown")
    print("Could not find enough models to determine 'must be true'")