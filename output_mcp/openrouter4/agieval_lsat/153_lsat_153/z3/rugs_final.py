from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
NUM_COLORS = 6
NUM_RUGS = 3

# x[c][r] is True if color c is used in rug r
x = [[Bool(f"x_{c}_{r}") for r in range(NUM_RUGS)] for c in range(NUM_COLORS)]

# Each color can be used in at most one rug
for c in range(NUM_COLORS):
    solver.add(Sum([If(x[c][r], 1, 0) for r in range(NUM_RUGS)]) <= 1)

# Each rug must have at least 1 color
for r in range(NUM_RUGS):
    solver.add(Sum([If(x[c][r], 1, 0) for c in range(NUM_COLORS)]) >= 1)

# Exactly 5 colors are used total
total_colors_used = Sum([If(x[c][r], 1, 0) for c in range(NUM_COLORS) for r in range(NUM_RUGS)])
solver.add(total_colors_used == 5)

# ---- RULES ----

# Rule 1: In any rug where white (4) is used, exactly two other colors are also used.
for r in range(NUM_RUGS):
    white_in_r = x[4][r]
    other_colors_in_r = Sum([If(x[c][r], 1, 0) for c in range(NUM_COLORS) if c != 4])
    solver.add(Implies(white_in_r, other_colors_in_r == 2))

# Rule 2: If olive (1) is used in a rug, peach (2) is also used in that rug.
for r in range(NUM_RUGS):
    solver.add(Implies(x[1][r], x[2][r]))

# Rule 3: Forest (0) and turquoise (3) are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(x[0][r], x[3][r])))

# Rule 4: Peach (2) and turquoise (3) are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(x[2][r], x[3][r])))

# Rule 5: Peach (2) and yellow (5) are not used together in a rug.
for r in range(NUM_RUGS):
    solver.add(Not(And(x[2][r], x[5][r])))

# GIVEN: Forest and peach are used together in a rug.
given_condition = Or([And(x[0][r], x[2][r]) for r in range(NUM_RUGS)])
solver.add(given_condition)

# ---- OPTIONS ----

# (A) Exactly one solid rug (rug with exactly 1 color)
opt_a = Sum([If(Sum([If(x[c][r], 1, 0) for c in range(NUM_COLORS)]) == 1, 1, 0) for r in range(NUM_RUGS)]) == 1

# (B) White is not used in any rug
opt_b = And([Not(x[4][r]) for r in range(NUM_RUGS)])

# (C) Yellow is not used in any rug
opt_c = And([Not(x[5][r]) for r in range(NUM_RUGS)])

# (D) Turquoise and white are used together in a rug
opt_d = Or([And(x[3][r], x[4][r]) for r in range(NUM_RUGS)])

# (E) Turquoise and yellow are used together in a rug
opt_e = Or([And(x[3][r], x[5][r]) for r in range(NUM_RUGS)])

# ---- EVALUATE ----
found_options = []
context = {
    "A": opt_a,
    "B": opt_b,
    "C": opt_c,
    "D": opt_d,
    "E": opt_e
}

for letter in ["A", "B", "C", "D", "E"]:
    solver.push()
    solver.add(context[letter])
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