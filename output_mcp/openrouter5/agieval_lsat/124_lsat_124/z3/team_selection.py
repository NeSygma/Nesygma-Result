from z3 import *

# Define boolean variables for each employee
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

solver = Solver()

# At least 4 employees on the team
solver.add(Sum([If(v, 1, 0) for v in [M, O, P, S, T, W, Y, Z]]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))

# Now evaluate each option: "X and Y cannot be on the team together"
# We test if it's POSSIBLE for both to be on the team together.
# If it's NOT possible (unsat), then they CANNOT be together.

options = [
    ("A", And(M, T)),  # Myers and Thomson
    ("B", And(O, Y)),  # Ortega and Yoder
    ("C", And(P, Z)),  # Paine and Zayre
    ("D", And(S, W)),  # Schmidt and Wong
    ("E", And(W, Y))   # Wong and Yoder
]

found_options = []
for letter, constr in options:
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