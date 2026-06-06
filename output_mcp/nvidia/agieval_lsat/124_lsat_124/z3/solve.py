from z3 import *

solver = Solver()

# Declare boolean variables for each employee
M = Bool('M')
O = Bool('O')
P = Bool('P')
S = Bool('S')
T = Bool('T')
W = Bool('W')
Y = Bool('Y')
Z = Bool('Z')

# At least 4 employees selected
solver.add(Sum([M, O, P, S, T, W, Y, Z]) >= 4)

# Constraints
solver.add(Implies(M, Not(O)))
solver.add(Implies(M, Not(P)))
solver.add(Implies(S, And(P, T)))
solver.add(Implies(W, And(M, Y)))

# Option constraints
opt_a_constr = And(M, T)  # Myers and Thomson
opt_b_constr = And(O, Y)  # Ortega and Yoder
opt_c_constr = And(P, Z)  # Paine and Zayre
opt_d_constr = And(S, W)  # Schmidt and Wong
opt_e_constr = And(W, Y)  # Wong and Yoder

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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