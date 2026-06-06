from z3 import *

solver = Solver()

# Define boolean variables for each employee
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

# Base constraints
# At least four employees on the team
team_size = Sum([If(M, 1, 0), If(O, 1, 0), If(P, 1, 0), If(S, 1, 0),
                 If(T, 1, 0), If(W, 1, 0), If(Y, 1, 0), If(Z, 1, 0)])
solver.add(team_size >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))

# Additional given: Paine is not on the team.
solver.add(Not(P))

# Define the choice constraints
opt_a = And(Not(M), Not(O))
opt_b = And(Not(M), Not(T))
opt_c = And(Not(M), Not(Z))
opt_d = And(Not(O), Not(T))
opt_e = And(Not(O), Not(Y))

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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