from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# Rugs: rug0, rug1, rug2
# rug_color[r][c] = True if color c is used in rug r

N_COLORS = 6
N_RUGS = 3

# Boolean variables: rug_color[r][c] means color c is in rug r
rug_color = [[Bool(f"rug{r}_{c}") for c in range(N_COLORS)] for r in range(N_RUGS)]

# used[c] = color c is used in exactly one rug
used = [Bool(f"used_{c}") for c in range(N_COLORS)]

# Each color used in at most one rug
for c in range(N_COLORS):
    for r1 in range(N_RUGS):
        for r2 in range(r1+1, N_RUGS):
            solver.add(Not(And(rug_color[r1][c], rug_color[r2][c])))

# used[c] iff color c appears in some rug
for c in range(N_COLORS):
    solver.add(used[c] == Or([rug_color[r][c] for r in range(N_RUGS)]))

# Exactly 5 of the 6 colors are used
solver.add(Sum([If(used[c], 1, 0) for c in range(N_COLORS)]) == 5)

# Each rug must have at least 1 color
for r in range(N_RUGS):
    solver.add(Sum([If(rug_color[r][c], 1, 0) for c in range(N_COLORS)]) >= 1)

# Rule 1: In any rug in which white is used, two other colors are also used.
# So if white is in a rug, that rug has exactly 3 colors.
for r in range(N_RUGS):
    solver.add(Implies(rug_color[r][4], Sum([If(rug_color[r][c], 1, 0) for c in range(N_COLORS)]) == 3))

# Rule 2: In any rug in which olive is used, peach is also used.
for r in range(N_RUGS):
    solver.add(Implies(rug_color[r][1], rug_color[r][2]))

# Rule 3: Forest and turquoise are not used together in a rug.
for r in range(N_RUGS):
    solver.add(Not(And(rug_color[r][0], rug_color[r][3])))

# Rule 4: Peach and turquoise are not used together in a rug.
for r in range(N_RUGS):
    solver.add(Not(And(rug_color[r][2], rug_color[r][3])))

# Rule 5: Peach and yellow are not used together in a rug.
for r in range(N_RUGS):
    solver.add(Not(And(rug_color[r][2], rug_color[r][5])))

# Define the options
# (A) There are no multicolored rugs in which forest is used.
# A multicolored rug has 2+ colors. So for all rugs, if forest is used, the rug is solid (1 color).
opt_a = And([Implies(rug_color[r][0], Sum([If(rug_color[r][c], 1, 0) for c in range(N_COLORS)]) == 1) for r in range(N_RUGS)])

# (B) There are no multicolored rugs in which turquoise is used.
opt_b = And([Implies(rug_color[r][3], Sum([If(rug_color[r][c], 1, 0) for c in range(N_COLORS)]) == 1) for r in range(N_RUGS)])

# (C) Peach is used in one of the rugs.
opt_c = used[2]

# (D) Turquoise is used in one of the rugs.
opt_d = used[3]

# (E) Yellow is used in one of the rugs.
opt_e = used[5]

# For "must be true" we need to check: is the option entailed by the constraints?
# An option "must be true" if its negation is unsatisfiable (no model where it's false).
# We check each option: if adding NOT(option) is unsat, then it must be true.

must_be_true = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        must_be_true.append(letter)
    solver.pop()

print(f"Options that MUST be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")