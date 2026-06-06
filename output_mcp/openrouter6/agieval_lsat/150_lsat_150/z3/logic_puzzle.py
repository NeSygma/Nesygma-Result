from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
# Rugs: 0,1,2
in_color_rug = [[Bool(f"in_{c}_{r}") for r in range(3)] for c in range(6)]

# Base constraints

# 1. Each color in at most one rug
for c in range(6):
    solver.add(Sum([If(in_color_rug[c][r], 1, 0) for r in range(3)]) <= 1)

# 2. Exactly five colors used
used_colors = [Sum([If(in_color_rug[c][r], 1, 0) for r in range(3)]) for c in range(6)]
solver.add(Sum([If(used_colors[c] == 1, 1, 0) for c in range(6)]) == 5)

# 3. For each rug, if white is used, total colors = 3
for r in range(3):
    total_colors_r = Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)])
    solver.add(Implies(in_color_rug[4][r], total_colors_r == 3))

# 4. If olive is used, peach is also used
for r in range(3):
    solver.add(Implies(in_color_rug[1][r], in_color_rug[2][r]))

# 5. Forest and turquoise not together
for r in range(3):
    solver.add(Not(And(in_color_rug[0][r], in_color_rug[3][r])))

# 6. Peach and turquoise not together
for r in range(3):
    solver.add(Not(And(in_color_rug[2][r], in_color_rug[3][r])))

# 7. Peach and yellow not together
for r in range(3):
    solver.add(Not(And(in_color_rug[2][r], in_color_rug[5][r])))

# Define option constraints
# (A) No multicolored rugs with forest: if forest in a rug, that rug has exactly 1 color
opt_a_constr = And([Implies(in_color_rug[0][r], Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) == 1) for r in range(3)])

# (B) No multicolored rugs with turquoise
opt_b_constr = And([Implies(in_color_rug[3][r], Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) == 1) for r in range(3)])

# (C) Peach is used
opt_c_constr = Sum([If(in_color_rug[2][r], 1, 0) for r in range(3)]) == 1

# (D) Turquoise is used
opt_d_constr = Sum([If(in_color_rug[3][r], 1, 0) for r in range(3)]) == 1

# (E) Yellow is used
opt_e_constr = Sum([If(in_color_rug[5][r], 1, 0) for r in range(3)]) == 1

# Evaluate each option using the skeleton
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