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

# Additional implicit constraints: each rug must have at least one color (since it's woven)
for r in range(3):
    solver.add(Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) >= 1)

# Check base satisfiability
print("Checking base satisfiability...")
if solver.check() == sat:
    print("Base constraints are satisfiable.")
    # Optionally print a model
    m = solver.model()
    # Print which colors are used in which rugs
    for r in range(3):
        colors_in_rug = [c for c in range(6) if is_true(m[in_color_rug[c][r]])]
        print(f"Rug {r}: colors {colors_in_rug}")
else:
    print("Base constraints are unsatisfiable. Something is wrong.")
    exit()

# Now test each option's necessity: check if negation is unsatisfiable
options = [
    ("A", "No multicolored rugs with forest", 
     And([Implies(in_color_rug[0][r], Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) == 1) for r in range(3)])),
    ("B", "No multicolored rugs with turquoise",
     And([Implies(in_color_rug[3][r], Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) == 1) for r in range(3)])),
    ("C", "Peach is used",
     Sum([If(in_color_rug[2][r], 1, 0) for r in range(3)]) == 1),
    ("D", "Turquoise is used",
     Sum([If(in_color_rug[3][r], 1, 0) for r in range(3)]) == 1),
    ("E", "Yellow is used",
     Sum([If(in_color_rug[5][r], 1, 0) for r in range(3)]) == 1)
]

necessary_options = []
for letter, desc, constr in options:
    # Create a new solver for each test
    s = Solver()
    # Add base constraints
    for c in range(6):
        s.add(Sum([If(in_color_rug[c][r], 1, 0) for r in range(3)]) <= 1)
    used_colors = [Sum([If(in_color_rug[c][r], 1, 0) for r in range(3)]) for c in range(6)]
    s.add(Sum([If(used_colors[c] == 1, 1, 0) for c in range(6)]) == 5)
    for r in range(3):
        total_colors_r = Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)])
        s.add(Implies(in_color_rug[4][r], total_colors_r == 3))
    for r in range(3):
        s.add(Implies(in_color_rug[1][r], in_color_rug[2][r]))
    for r in range(3):
        s.add(Not(And(in_color_rug[0][r], in_color_rug[3][r])))
    for r in range(3):
        s.add(Not(And(in_color_rug[2][r], in_color_rug[3][r])))
    for r in range(3):
        s.add(Not(And(in_color_rug[2][r], in_color_rug[5][r])))
    for r in range(3):
        s.add(Sum([If(in_color_rug[c][r], 1, 0) for c in range(6)]) >= 1)
    
    # Add negation of the option
    s.add(Not(constr))
    
    # Check satisfiability
    if s.check() == unsat:
        necessary_options.append(letter)
        print(f"Option {letter} ({desc}) must be true (negation unsatisfiable).")
    else:
        print(f"Option {letter} ({desc}) is not necessarily true (negation satisfiable).")

print()
print("Necessary options:", necessary_options)

if len(necessary_options) == 1:
    print("STATUS: sat")
    print(f"answer:{necessary_options[0]}")
elif len(necessary_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {necessary_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")