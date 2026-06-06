from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
N_COLORS = 6
N_RUGS = 3
NOT_USED = 3  # special value meaning color is not used

# rug_of[c] = which rug (0,1,2) color c is assigned to, or 3 if not used
rug_of = [Int(f'rug_{c}') for c in range(N_COLORS)]

for c in range(N_COLORS):
    solver.add(rug_of[c] >= 0, rug_of[c] <= NOT_USED)

# Exactly 5 of the 6 colors are used
solver.add(Sum([If(rug_of[c] != NOT_USED, 1, 0) for c in range(N_COLORS)]) == 5)

# Each rug must have at least 1 color (three rugs are woven)
for r in range(N_RUGS):
    solver.add(Sum([If(rug_of[c] == r, 1, 0) for c in range(N_COLORS)]) >= 1)

# CONDITION: One rug is solid yellow.
# Let rug 0 be the solid yellow rug.
solver.add(rug_of[5] == 0)  # yellow is in rug 0
# No other color is in rug 0
for c in range(5):  # colors 0-4 are not yellow
    solver.add(rug_of[c] != 0)

# RULE 1: If white is used in a rug, that rug has exactly 3 colors (white + 2 others)
for r in range(N_RUGS):
    count_in_rug_r = Sum([If(rug_of[c] == r, 1, 0) for c in range(N_COLORS)])
    solver.add(Implies(rug_of[4] == r, count_in_rug_r == 3))

# RULE 2: If olive is used, peach is in the same rug
solver.add(Implies(rug_of[1] != NOT_USED, rug_of[2] == rug_of[1]))

# RULE 3: Forest and turquoise are not used together in a rug
solver.add(Or(rug_of[0] == NOT_USED, rug_of[3] == NOT_USED, rug_of[0] != rug_of[3]))

# RULE 4: Peach and turquoise are not used together in a rug
solver.add(Or(rug_of[2] == NOT_USED, rug_of[3] == NOT_USED, rug_of[2] != rug_of[3]))

# RULE 5: Peach and yellow are not used together in a rug
# Since yellow is in rug 0, peach cannot be in rug 0 (unless peach is not used)
solver.add(Or(rug_of[2] == NOT_USED, rug_of[2] != 0))

# Helper: count colors in a rug
def count_in_rug(r):
    return Sum([If(rug_of[c] == r, 1, 0) for c in range(N_COLORS)])

# Define each option constraint
# (A) There is exactly one solid color rug.
# Since rug 0 is solid yellow, this means rugs 1 and 2 are NOT solid (each has >= 2 colors)
opt_a = And(
    count_in_rug(1) >= 2,
    count_in_rug(2) >= 2
)

# (B) One of the rugs is solid forest.
# Forest is used as the only color in some rug (rug 1 or rug 2, since rug 0 is yellow)
opt_b = And(
    rug_of[0] != NOT_USED,  # forest is used
    Or(
        And(rug_of[0] == 1, count_in_rug(1) == 1),
        And(rug_of[0] == 2, count_in_rug(2) == 1)
    )
)

# (C) Turquoise is not used in any of the rugs.
opt_c = rug_of[3] == NOT_USED

# (D) Forest and olive are used together in a rug.
opt_d = And(rug_of[0] != NOT_USED, rug_of[1] != NOT_USED, rug_of[0] == rug_of[1])

# (E) Peach and white are used together in a rug.
opt_e = And(rug_of[2] != NOT_USED, rug_of[4] != NOT_USED, rug_of[2] == rug_of[4])

# Since the question asks "could be true EXCEPT" (find the IMPOSSIBLE one),
# we find which option is UNSAT (cannot be true)
impossible_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == unsat:
        impossible_options.append(letter)
    solver.pop()

print()
if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
elif len(impossible_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options impossible {impossible_options}")
elif len(impossible_options) == 0:
    print("STATUS: unsat")
    print("Refine: No options impossible (all could be true)")
else:
    print("STATUS: unknown")