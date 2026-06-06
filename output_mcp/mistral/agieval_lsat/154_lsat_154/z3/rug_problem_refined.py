from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the solver
solver = Solver()

# Colors
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
color_vars = {c: Bool(c) for c in colors}  # True if color is used

# Rugs: 3 rugs, each is a set of colors
# We'll represent each rug as a list of Bool variables indicating which colors are in it
rugs = []
for i in range(3):
    rug_colors = {c: Bool(f"rug{i}_{c}") for c in colors}
    rugs.append(rug_colors)

# Each color is used in exactly one rug or not used at all
for c in colors:
    # If color is used, it must be in exactly one rug
    in_rugs = [rugs[i][c] for i in range(3)]
    solver.add(Implies(color_vars[c], Sum(in_rugs) == 1))
    # If color is not used, it must not be in any rug
    solver.add(Implies(Not(color_vars[c]), And([Not(rugs[i][c]) for i in range(3)])))

# Exactly 5 colors are used
solver.add(Sum(list(color_vars.values())) == 5)

# One rug is solid yellow (has exactly yellow, no other colors)
# We allow the solid yellow rug to be any of the three rugs
# For this problem, we assume rug 0 is solid yellow (as per the problem statement)
solver.add(And(
    rugs[0]["yellow"],
    Not(rugs[0]["forest"]),
    Not(rugs[0]["olive"]),
    Not(rugs[0]["peach"]),
    Not(rugs[0]["turquoise"]),
    Not(rugs[0]["white"])
))

# Helper: For each rug, count how many colors it has
rug_color_counts = []
for i in range(3):
    count = Sum([If(rugs[i][c], 1, 0) for c in colors])
    rug_color_counts.append(count)

# Constraints on color combinations within each rug

# 1. In any rug in which white is used, two other colors are also used.
# This means: if white is in a rug, that rug must have exactly 3 colors total
for i in range(3):
    white_in_rug = rugs[i]["white"]
    count = rug_color_counts[i]
    # If white is in the rug, count must be exactly 3
    solver.add(Implies(white_in_rug, count == 3))

# 2. In any rug in which olive is used, peach is also used.
for i in range(3):
    olive_in_rug = rugs[i]["olive"]
    peach_in_rug = rugs[i]["peach"]
    solver.add(Implies(olive_in_rug, peach_in_rug))

# 3. Forest and turquoise are not used together in a rug.
for i in range(3):
    solver.add(Not(And(rugs[i]["forest"], rugs[i]["turquoise"])))

# 4. Peach and turquoise are not used together in a rug.
for i in range(3):
    solver.add(Not(And(rugs[i]["peach"], rugs[i]["turquoise"])))

# 5. Peach and yellow are not used together in a rug.
for i in range(3):
    solver.add(Not(And(rugs[i]["peach"], rugs[i]["yellow"])))

# Now, evaluate the multiple choice options
# We need to find the option that CANNOT be true (i.e., is unsatisfiable)

# Option A: There is exactly one solid color rug
# A solid rug has exactly one color
opt_a_constr = Sum([If(rug_color_counts[i] == 1, 1, 0) for i in range(3)]) == 1

# Option B: One of the rugs is solid forest
opt_b_constr = Or(
    And(rug_color_counts[0] == 1, rugs[0]["forest"]),
    And(rug_color_counts[1] == 1, rugs[1]["forest"]),
    And(rug_color_counts[2] == 1, rugs[2]["forest"])
)

# Option C: Turquoise is not used in any of the rugs
opt_c_constr = Not(color_vars["turquoise"])

# Option D: Forest and olive are used together in a rug
opt_d_constr = Or(
    And(rugs[0]["forest"], rugs[0]["olive"]),
    And(rugs[1]["forest"], rugs[1]["olive"]),
    And(rugs[2]["forest"], rugs[2]["olive"])
)

# Option E: Peach and white are used together in a rug
opt_e_constr = Or(
    And(rugs[0]["peach"], rugs[0]["white"]),
    And(rugs[1]["peach"], rugs[1]["white"]),
    And(rugs[2]["peach"], rugs[2]["white"])
)

# Test each option for unsatisfiability (i.e., the option cannot be true)
found_impossible_options = []

# Test option A
solver.push()
solver.add(Not(opt_a_constr))
result_a = solver.check()
if result_a == unsat:
    # Option A cannot be false, so it must be always true -> not the answer
    pass
elif result_a == sat:
    # Option A can be false, so it is a possible answer
    found_impossible_options.append("A")
else:
    print("Option A is UNKNOWN")
solver.pop()

# Test option B
solver.push()
solver.add(Not(opt_b_constr))
result_b = solver.check()
if result_b == unsat:
    # Option B cannot be false, so it must be always true -> not the answer
    pass
elif result_b == sat:
    # Option B can be false, so it is a possible answer
    found_impossible_options.append("B")
else:
    print("Option B is UNKNOWN")
solver.pop()

# Test option C
solver.push()
solver.add(Not(opt_c_constr))
result_c = solver.check()
if result_c == unsat:
    # Option C cannot be false, so it must be always true -> not the answer
    pass
elif result_c == sat:
    # Option C can be false, so it is a possible answer
    found_impossible_options.append("C")
else:
    print("Option C is UNKNOWN")
solver.pop()

# Test option D
solver.push()
solver.add(Not(opt_d_constr))
result_d = solver.check()
if result_d == unsat:
    # Option D cannot be false, so it must be always true -> not the answer
    pass
elif result_d == sat:
    # Option D can be false, so it is a possible answer
    found_impossible_options.append("D")
else:
    print("Option D is UNKNOWN")
solver.pop()

# Test option E
solver.push()
solver.add(Not(opt_e_constr))
result_e = solver.check()
if result_e == unsat:
    # Option E cannot be false, so it must be always true -> not the answer
    pass
elif result_e == sat:
    # Option E can be false, so it is a possible answer
    found_impossible_options.append("E")
else:
    print("Option E is UNKNOWN")
solver.pop()

# Determine the answer
if len(found_impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_impossible_options[0]}")
elif len(found_impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {found_impossible_options}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")