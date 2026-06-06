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

# Helper: For a rug, the set of colors it uses
# We'll use the uses variables directly in constraints

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
    # If white is used, then exactly 2 other colors are used
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

# Now, evaluate each multiple-choice option
found_options = []

# Option A: forest only; turquoise only; olive, peach, and white
solver.push()
# Rug1: forest only
solver.add(uses[("rug1", "forest")])
solver.add(Not(uses[("rug1", "olive")]))
solver.add(Not(uses[("rug1", "peach")]))
solver.add(Not(uses[("rug1", "turquoise")]))
solver.add(Not(uses[("rug1", "white")]))
solver.add(Not(uses[("rug1", "yellow")]))
# Rug2: turquoise only
solver.add(uses[("rug2", "turquoise")])
solver.add(Not(uses[("rug2", "forest")]))
solver.add(Not(uses[("rug2", "olive")]))
solver.add(Not(uses[("rug2", "peach")]))
solver.add(Not(uses[("rug2", "white")]))
solver.add(Not(uses[("rug2", "yellow")]))
# Rug3: olive, peach, and white
solver.add(uses[("rug3", "olive")])
solver.add(uses[("rug3", "peach")])
solver.add(uses[("rug3", "white")])
solver.add(Not(uses[("rug3", "forest")]))
solver.add(Not(uses[("rug3", "turquoise")]))
solver.add(Not(uses[("rug3", "yellow")]))

if solver.check() == sat:
    found_options.append("A")
    # Print model for debugging
    model = solver.model()
    print("Option A is SATISFIABLE")
    for r in rugs:
        print(f"{r}:", end=" ")
        for c in colors:
            if is_true(model[uses[(r, c)]]):
                print(c, end=" ")
        print()
else:
    print("Option A is UNSATISFIABLE")
solver.pop()

# Option B: forest only; turquoise only; olive, peach, and yellow
solver.push()
# Rug1: forest only
solver.add(uses[("rug1", "forest")])
solver.add(Not(uses[("rug1", "olive")]))
solver.add(Not(uses[("rug1", "peach")]))
solver.add(Not(uses[("rug1", "turquoise")]))
solver.add(Not(uses[("rug1", "white")]))
solver.add(Not(uses[("rug1", "yellow")]))
# Rug2: turquoise only
solver.add(uses[("rug2", "turquoise")])
solver.add(Not(uses[("rug2", "forest")]))
solver.add(Not(uses[("rug2", "olive")]))
solver.add(Not(uses[("rug2", "peach")]))
solver.add(Not(uses[("rug2", "white")]))
solver.add(Not(uses[("rug2", "yellow")]))
# Rug3: olive, peach, and yellow
solver.add(uses[("rug3", "olive")])
solver.add(uses[("rug3", "peach")])
solver.add(uses[("rug3", "yellow")])
solver.add(Not(uses[("rug3", "forest")]))
solver.add(Not(uses[("rug3", "turquoise")]))
solver.add(Not(uses[("rug3", "white")]))

if solver.check() == sat:
    found_options.append("B")
    # Print model for debugging
    model = solver.model()
    print("Option B is SATISFIABLE")
    for r in rugs:
        print(f"{r}:", end=" ")
        for c in colors:
            if is_true(model[uses[(r, c)]]):
                print(c, end=" ")
        print()
else:
    print("Option B is UNSATISFIABLE")
solver.pop()

# Option C: peach only; turquoise only; forest, olive, and white
solver.push()
# Rug1: peach only
solver.add(uses[("rug1", "peach")])
solver.add(Not(uses[("rug1", "forest")]))
solver.add(Not(uses[("rug1", "olive")]))
solver.add(Not(uses[("rug1", "turquoise")]))
solver.add(Not(uses[("rug1", "white")]))
solver.add(Not(uses[("rug1", "yellow")]))
# Rug2: turquoise only
solver.add(uses[("rug2", "turquoise")])
solver.add(Not(uses[("rug2", "forest")]))
solver.add(Not(uses[("rug2", "olive")]))
solver.add(Not(uses[("rug2", "peach")]))
solver.add(Not(uses[("rug2", "white")]))
solver.add(Not(uses[("rug2", "yellow")]))
# Rug3: forest, olive, and white
solver.add(uses[("rug3", "forest")])
solver.add(uses[("rug3", "olive")])
solver.add(uses[("rug3", "white")])
solver.add(Not(uses[("rug3", "peach")]))
solver.add(Not(uses[("rug3", "turquoise")]))
solver.add(Not(uses[("rug3", "yellow")]))

if solver.check() == sat:
    found_options.append("C")
    # Print model for debugging
    model = solver.model()
    print("Option C is SATISFIABLE")
    for r in rugs:
        print(f"{r}:", end=" ")
        for c in colors:
            if is_true(model[uses[(r, c)]]):
                print(c, end=" ")
        print()
else:
    print("Option C is UNSATISFIABLE")
solver.pop()

# Option D: yellow only; forest and turquoise; olive and peach
solver.push()
# Rug1: yellow only
solver.add(uses[("rug1", "yellow")])
solver.add(Not(uses[("rug1", "forest")]))
solver.add(Not(uses[("rug1", "olive")]))
solver.add(Not(uses[("rug1", "peach")]))
solver.add(Not(uses[("rug1", "turquoise")]))
solver.add(Not(uses[("rug1", "white")]))
# Rug2: forest and turquoise
solver.add(uses[("rug2", "forest")])
solver.add(uses[("rug2", "turquoise")])
solver.add(Not(uses[("rug2", "olive")]))
solver.add(Not(uses[("rug2", "peach")]))
solver.add(Not(uses[("rug2", "white")]))
solver.add(Not(uses[("rug2", "yellow")]))
# Rug3: olive and peach
solver.add(uses[("rug3", "olive")])
solver.add(uses[("rug3", "peach")])
solver.add(Not(uses[("rug3", "forest")]))
solver.add(Not(uses[("rug3", "turquoise")]))
solver.add(Not(uses[("rug3", "white")]))
solver.add(Not(uses[("rug3", "yellow")]))

if solver.check() == sat:
    found_options.append("D")
    # Print model for debugging
    model = solver.model()
    print("Option D is SATISFIABLE")
    for r in rugs:
        print(f"{r}:", end=" ")
        for c in colors:
            if is_true(model[uses[(r, c)]]):
                print(c, end=" ")
        print()
else:
    print("Option D is UNSATISFIABLE")
solver.pop()

# Option E: yellow only; olive and peach; turquoise and white
solver.push()
# Rug1: yellow only
solver.add(uses[("rug1", "yellow")])
solver.add(Not(uses[("rug1", "forest")]))
solver.add(Not(uses[("rug1", "olive")]))
solver.add(Not(uses[("rug1", "peach")]))
solver.add(Not(uses[("rug1", "turquoise")]))
solver.add(Not(uses[("rug1", "white")]))
# Rug2: olive and peach
solver.add(uses[("rug2", "olive")])
solver.add(uses[("rug2", "peach")])
solver.add(Not(uses[("rug2", "forest")]))
solver.add(Not(uses[("rug2", "turquoise")]))
solver.add(Not(uses[("rug2", "white")]))
solver.add(Not(uses[("rug2", "yellow")]))
# Rug3: turquoise and white
solver.add(uses[("rug3", "turquoise")])
solver.add(uses[("rug3", "white")])
solver.add(Not(uses[("rug3", "forest")]))
solver.add(Not(uses[("rug3", "olive")]))
solver.add(Not(uses[("rug3", "peach")]))
solver.add(Not(uses[("rug3", "yellow")]))

if solver.check() == sat:
    found_options.append("E")
    # Print model for debugging
    model = solver.model()
    print("Option E is SATISFIABLE")
    for r in rugs:
        print(f"{r}:", end=" ")
        for c in colors:
            if is_true(model[uses[(r, c)]]):
                print(c, end=" ")
        print()
else:
    print("Option E is UNSATISFIABLE")
solver.pop()

# Output the result according to the required skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")