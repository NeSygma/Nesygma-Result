from z3 import *

# Six colors: forest, olive, peach, turquoise, white, yellow
# Exactly 5 of the 6 colors are used.
# Each used color is used in only one rug.
# Three rugs: rug0, rug1, rug2
# Each rug is either solid (1 color) or multicolored (2+ colors).
# Rules:
# 1. In any rug in which white is used, two other colors are also used. (So white rug has exactly 3 colors total)
# 2. In any rug in which olive is used, peach is also used.
# 3. Forest and turquoise are not used together in a rug.
# 4. Peach and turquoise are not used together in a rug.
# 5. Peach and yellow are not used together in a rug.
# Additional condition: forest and peach are used together in a rug.

# We need to find which option COULD be true (i.e., is satisfiable given all constraints).

# Let's model this.
# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
num_colors = 6
num_rugs = 3

# Decision variables:
# used[c] = True if color c is used at all
used = [Bool(f"used_{c}") for c in range(num_colors)]

# in_rug[c][r] = True if color c is used in rug r
in_rug = [[Bool(f"in_rug_{c}_{r}") for r in range(num_rugs)] for c in range(num_colors)]

# rug_has_color[r][c] = same as in_rug[c][r] but maybe easier to read
# We'll use in_rug[c][r]

solver = Solver()

# Exactly 5 of the 6 colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(num_colors)]) == 5)

# A color is used iff it appears in at least one rug
for c in range(num_colors):
    solver.add(used[c] == Or([in_rug[c][r] for r in range(num_rugs)]))

# Each used color is used in exactly one rug
for c in range(num_colors):
    solver.add(Implies(used[c], Sum([If(in_rug[c][r], 1, 0) for r in range(num_rugs)]) == 1))
    # If not used, it's in no rug
    solver.add(Implies(Not(used[c]), And([Not(in_rug[c][r]) for r in range(num_rugs)])))

# Each rug must have at least one color (it's woven)
for r in range(num_rugs):
    solver.add(Or([in_rug[c][r] for c in range(num_colors)]))

# Rule 1: In any rug in which white is used, two other colors are also used.
# So if white is in rug r, then rug r has exactly 3 colors total (white + 2 others)
for r in range(num_rugs):
    solver.add(Implies(in_rug[4][r], Sum([If(in_rug[c][r], 1, 0) for c in range(num_colors)]) == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
for r in range(num_rugs):
    solver.add(Implies(in_rug[1][r], in_rug[2][r]))

# Rule 3: Forest and turquoise are not used together in a rug.
for r in range(num_rugs):
    solver.add(Not(And(in_rug[0][r], in_rug[3][r])))

# Rule 4: Peach and turquoise are not used together in a rug.
for r in range(num_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[3][r])))

# Rule 5: Peach and yellow are not used together in a rug.
for r in range(num_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[5][r])))

# Additional condition: forest and peach are used together in a rug.
# There exists a rug r such that both forest and peach are in it.
solver.add(Or([And(in_rug[0][r], in_rug[2][r]) for r in range(num_rugs)]))

# Now evaluate each option

# Option A: There is exactly one solid rug.
# A solid rug has exactly 1 color.
opt_a = Sum([If(Sum([If(in_rug[c][r], 1, 0) for c in range(num_colors)]) == 1, 1, 0) for r in range(num_rugs)]) == 1

# Option B: White is not used in any of the rugs.
opt_b = Not(used[4])

# Option C: Yellow is not used in any of the rugs.
opt_c = Not(used[5])

# Option D: Turquoise and white are used together in a rug.
opt_d = Or([And(in_rug[3][r], in_rug[4][r]) for r in range(num_rugs)])

# Option E: Turquoise and yellow are used together in a rug.
opt_e = Or([And(in_rug[3][r], in_rug[5][r]) for r in range(num_rugs)])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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