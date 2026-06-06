from z3 import *

solver = Solver()

# Colors: 0=forest, 1=olive, 2=peach, 3=turquoise, 4=white, 5=yellow
n_colors = 6
n_rugs = 3
color_names = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']

# in_rug[c][r] = True if color c is in rug r
in_rug = [[Bool(f'in_{c}_{r}') for r in range(n_rugs)] for c in range(n_colors)]

# Each color is in at most one rug
for c in range(n_colors):
    for r1 in range(n_rugs):
        for r2 in range(r1+1, n_rugs):
            solver.add(Not(And(in_rug[c][r1], in_rug[c][r2])))

# Exactly 5 colors used (one color excluded)
solver.add(Sum([If(Or([in_rug[c][r] for r in range(n_rugs)]), 1, 0) for c in range(n_colors)]) == 5)

# Each rug must have at least one color (three rugs are woven)
for r in range(n_rugs):
    solver.add(Or([in_rug[c][r] for c in range(n_colors)]))

# Rule 1: If white (4) is in a rug, two other colors are also in that rug
for r in range(n_rugs):
    others_count = Sum([If(in_rug[c][r], 1, 0) for c in range(n_colors) if c != 4])
    solver.add(Implies(in_rug[4][r], others_count >= 2))

# Rule 2: If olive (1) is in a rug, peach (2) is also in that rug
for r in range(n_rugs):
    solver.add(Implies(in_rug[1][r], in_rug[2][r]))

# Rule 3: Forest (0) and turquoise (3) not together
for r in range(n_rugs):
    solver.add(Not(And(in_rug[0][r], in_rug[3][r])))

# Rule 4: Peach (2) and turquoise (3) not together
for r in range(n_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[3][r])))

# Rule 5: Peach (2) and yellow (5) not together
for r in range(n_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[5][r])))

# Given condition: Forest and peach are used together in a rug
solver.add(Or([And(in_rug[0][r], in_rug[2][r]) for r in range(n_rugs)]))

# Define solid rugs (exactly 1 color)
solid = [Bool(f'solid_{r}') for r in range(n_rugs)]
for r in range(n_rugs):
    rug_size = Sum([If(in_rug[c][r], 1, 0) for c in range(n_colors)])
    solver.add(solid[r] == (rug_size == 1))

num_solid = Sum([If(solid[r], 1, 0) for r in range(n_rugs)])

# Option A: Exactly one solid rug
opt_a = (num_solid == 1)

# Option B: White is not used in any rug
opt_b = And([Not(in_rug[4][r]) for r in range(n_rugs)])

# Option C: Yellow is not used in any rug
opt_c = And([Not(in_rug[5][r]) for r in range(n_rugs)])

# Option D: Turquoise and white are used together in a rug
opt_d = Or([And(in_rug[3][r], in_rug[4][r]) for r in range(n_rugs)])

# Option E: Turquoise and yellow are used together in a rug
opt_e = Or([And(in_rug[3][r], in_rug[5][r]) for r in range(n_rugs)])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for r in range(n_rugs):
            rug_colors = []
            for c in range(n_colors):
                if is_true(m.evaluate(in_rug[c][r])):
                    rug_colors.append(color_names[c])
            print(f"  Rug {r}: {rug_colors}")
    else:
        print(f"Option {letter}: {result}")
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