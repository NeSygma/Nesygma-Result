from z3 import *

solver = Solver()

# Colors: F=0, O=1, P=2, T=3, W=4, Y=5
# Rugs: 0, 1, 2
n_colors = 6
n_rugs = 3
color_names = ['Forest', 'Olive', 'Peach', 'Turquoise', 'White', 'Yellow']

# in_rug[c][r] = True if color c is in rug r
in_rug = [[Bool(f'in_{c}_{r}') for r in range(n_rugs)] for c in range(n_colors)]

# Each color is in at most one rug
for c in range(n_colors):
    for r1 in range(n_rugs):
        for r2 in range(r1+1, n_rugs):
            solver.add(Not(And(in_rug[c][r1], in_rug[c][r2])))

# Exactly 5 colors are used
used = [Or([in_rug[c][r] for r in range(n_rugs)]) for c in range(n_colors)]
solver.add(Sum([If(used[c], 1, 0) for c in range(n_colors)]) == 5)

# Each rug has at least 1 color (three rugs are woven)
for r in range(n_rugs):
    solver.add(Sum([If(in_rug[c][r], 1, 0) for c in range(n_colors)]) >= 1)

# === GIVEN: One rug is solid yellow ===
# Yellow is used
solver.add(Or([in_rug[5][r] for r in range(n_rugs)]))
# The rug with yellow has ONLY yellow (solid)
for r in range(n_rugs):
    solver.add(Implies(in_rug[5][r], And([Not(in_rug[c][r]) for c in range(5)])))

# === RULE 1: White in a rug → exactly 2 other colors also in that rug (total = 3) ===
for r in range(n_rugs):
    other_colors = [c for c in range(n_colors) if c != 4]  # all except white
    other_count = Sum([If(in_rug[c][r], 1, 0) for c in other_colors])
    solver.add(Implies(in_rug[4][r], other_count == 2))

# === RULE 2: Olive in a rug → peach also in that rug ===
for r in range(n_rugs):
    solver.add(Implies(in_rug[1][r], in_rug[2][r]))

# === RULE 3: Forest and turquoise not together ===
for r in range(n_rugs):
    solver.add(Not(And(in_rug[0][r], in_rug[3][r])))

# === RULE 4: Peach and turquoise not together ===
for r in range(n_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[3][r])))

# === RULE 5: Peach and yellow not together ===
for r in range(n_rugs):
    solver.add(Not(And(in_rug[2][r], in_rug[5][r])))

# Define solid rugs
solid = []
for r in range(n_rugs):
    count = Sum([If(in_rug[c][r], 1, 0) for c in range(n_colors)])
    s = Bool(f'solid_{r}')
    solver.add(s == (count == 1))
    solid.append(s)

# === OPTION CONSTRAINTS ===

# Option A: There is exactly one solid color rug
opt_a_constr = Sum([If(solid[r], 1, 0) for r in range(n_rugs)]) == 1

# Option B: One of the rugs is solid forest
opt_b_constr = Or([And(in_rug[0][r], solid[r]) for r in range(n_rugs)])

# Option C: Turquoise is not used in any of the rugs
opt_c_constr = Not(Or([in_rug[3][r] for r in range(n_rugs)]))

# Option D: Forest and olive are used together in a rug
opt_d_constr = Or([And(in_rug[0][r], in_rug[1][r]) for r in range(n_rugs)])

# Option E: Peach and white are used together in a rug
opt_e_constr = Or([And(in_rug[2][r], in_rug[4][r]) for r in range(n_rugs)])

# === EVALUATE EACH OPTION ===
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter}: SAT")
        for r in range(n_rugs):
            colors_in_rug = [color_names[c] for c in range(n_colors) if is_true(m.evaluate(in_rug[c][r]))]
            print(f"  Rug {r}: {colors_in_rug}")
    else:
        print(f"Option {letter}: {result}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")