from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
colors = ['forest', 'olive', 'peach', 'turquoise', 'white', 'yellow']
n_colors = 6
n_rugs = 3

# rug_of_color[c] = which rug (0,1,2) color c is assigned to, or -1 if not used
rug_of_color = [Int(f'rug_{c}') for c in colors]

# Each color is either not used (-1) or assigned to rug 0, 1, or 2
for c in range(n_colors):
    solver.add(Or(rug_of_color[c] == -1, rug_of_color[c] == 0, rug_of_color[c] == 1, rug_of_color[c] == 2))

# Exactly 5 of 6 colors are used (exactly one is -1)
solver.add(Sum([If(rug_of_color[c] == -1, 1, 0) for c in range(n_colors)]) == 1)

# Count colors per rug
count_in_rug = [Sum([If(rug_of_color[c] == r, 1, 0) for c in range(n_colors)]) for r in range(n_rugs)]

# Each rug must have at least 1 color
for r in range(n_rugs):
    solver.add(count_in_rug[r] >= 1)

# A rug is solid if it has exactly 1 color, multicolored if it has 2+ colors
# Constraint 1: If white is used in a rug, that rug has exactly 3 colors (white + 2 others)
for r in range(n_rugs):
    solver.add(Implies(rug_of_color[4] == r, count_in_rug[r] == 3))

# Constraint 2: If olive is used in a rug, peach is also in that rug
for r in range(n_rugs):
    solver.add(Implies(rug_of_color[1] == r, rug_of_color[2] == r))

# Constraint 3: Forest and turquoise not together
for r in range(n_rugs):
    solver.add(Not(And(rug_of_color[0] == r, rug_of_color[3] == r)))

# Constraint 4: Peach and turquoise not together
for r in range(n_rugs):
    solver.add(Not(And(rug_of_color[2] == r, rug_of_color[3] == r)))

# Constraint 5: Peach and yellow not together
for r in range(n_rugs):
    solver.add(Not(And(rug_of_color[2] == r, rug_of_color[5] == r)))

# Additional condition: Forest and peach are used together in a rug
solver.add(Or([And(rug_of_color[0] == r, rug_of_color[2] == r) for r in range(n_rugs)]))

# Now evaluate each option
# Option A: There is exactly one solid rug (a rug with exactly 1 color)
opt_a_constr = Sum([If(count_in_rug[r] == 1, 1, 0) for r in range(n_rugs)]) == 1

# Option B: White is not used in any of the rugs
opt_b_constr = (rug_of_color[4] == -1)

# Option C: Yellow is not used in any of the rugs
opt_c_constr = (rug_of_color[5] == -1)

# Option D: Turquoise and white are used together in a rug
opt_d_constr = Or([And(rug_of_color[3] == r, rug_of_color[4] == r) for r in range(n_rugs)])

# Option E: Turquoise and yellow are used together in a rug
opt_e_constr = Or([And(rug_of_color[3] == r, rug_of_color[5] == r) for r in range(n_rugs)])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for c in range(n_colors):
            val = m.eval(rug_of_color[c], model_completion=True)
            print(f"  {colors[c]} -> rug {val}")
        for r in range(n_rugs):
            cnt = m.eval(count_in_rug[r], model_completion=True)
            print(f"  Rug {r} has {cnt} colors")
    else:
        print(f"Option {letter} is {result}")
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