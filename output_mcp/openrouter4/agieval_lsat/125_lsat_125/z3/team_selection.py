from z3 import *

solver = Solver()

# Boolean variables for each employee
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))

# At least 4 employees on the team
solver.add(Sum([M, O, P, S, T, W, Y, Z]) >= 4)

# Given: Yoder is not on the team
solver.add(Not(Y))

# Now test each option: which person CAN be on the team (SAT means could be on team)
# The one that is UNSAT is the EXCEPTION (cannot be on the team)
options = [
    ("A", Z, "Zayre"),
    ("B", T, "Thomson"),
    ("C", P, "Paine"),
    ("D", O, "Ortega"),
    ("E", M, "Myers")
]

# Find which options are UNSAT (the exceptions)
unsat_options = []
for letter, var, name in options:
    solver.push()
    solver.add(var == True)  # Force this person to be on the team
    result = solver.check()
    if result == unsat:
        unsat_options.append(letter)
    solver.pop()

print(f"Options that CANNOT be on the team (exceptions): {unsat_options}")
print()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple exceptions found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No exceptions found (all options could be on the team)")