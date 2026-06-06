from z3 import *

# Variables: 8 employees, each is either on the team (True) or not (False)
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

# Additional condition from the question: Paine is NOT on the team.
solver.add(Not(P))

# Now evaluate each option
# Option A: Neither Myers nor Ortega is on the team.
opt_a = And(Not(M), Not(O))

# Option B: Neither Myers nor Thomson is on the team.
opt_b = And(Not(M), Not(T))

# Option C: Neither Myers nor Zayre is on the team.
opt_c = And(Not(M), Not(Z))

# Option D: Neither Ortega nor Thomson is on the team.
opt_d = And(Not(O), Not(T))

# Option E: Neither Ortega nor Yoder is on the team.
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