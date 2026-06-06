from z3 import *

# Declare boolean variables for each employee
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

# Create solver
solver = Solver()

# Add base constraints
# 1. If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))
# 2. If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))
# 3. If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))
# 4. Team size at least 4
team_vars = [M, O, P, S, T, W, Y, Z]
solver.add(Sum([If(v, 1, 0) for v in team_vars]) >= 4)

# Define options as pairs of employees that must have at least one on the team
# For each option, we will test if it's possible to have a valid team without both.
# If impossible (unsat), then the pair is mandatory.
options = [
    ("A", [O, S]),  # Ortega and Schmidt
    ("B", [O, W]),  # Ortega and Wong
    ("C", [P, S]),  # Paine and Schmidt
    ("D", [T, Y]),  # Thomson and Yoder
    ("E", [Y, Z]),  # Yoder and Zayre
]

found_options = []
for letter, pair in options:
    solver.push()
    # Add constraint that both employees in the pair are NOT on the team
    solver.add(Not(pair[0]))
    solver.add(Not(pair[1]))
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