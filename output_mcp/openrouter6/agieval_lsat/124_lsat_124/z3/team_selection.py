from z3 import *

solver = Solver()

# Declare Boolean variables for each employee
M, O, P, S, T, W, Y, Z = Bools('M O P S T W Y Z')

# Base constraints
# At least four employees
solver.add(Sum([If(M, 1, 0), If(O, 1, 0), If(P, 1, 0), If(S, 1, 0),
                If(T, 1, 0), If(W, 1, 0), If(Y, 1, 0), If(Z, 1, 0)]) >= 4)

# Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
solver.add(Implies(M, And(Not(O), Not(P))))

# Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
solver.add(Implies(S, And(P, T)))

# Condition 3: If Wong is on the team, both Myers and Yoder must also be.
solver.add(Implies(W, And(M, Y)))

# Define constraints for each option (pair together)
opt_a_constr = And(M, T)      # Myers and Thomson
opt_b_constr = And(O, Y)      # Ortega and Yoder
opt_c_constr = And(P, Z)      # Paine and Zayre
opt_d_constr = And(S, W)      # Schmidt and Wong
opt_e_constr = And(W, Y)      # Wong and Yoder

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr),
                       ("C", opt_c_constr), ("D", opt_d_constr),
                       ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:   # If the pair cannot be together, it's unsat
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