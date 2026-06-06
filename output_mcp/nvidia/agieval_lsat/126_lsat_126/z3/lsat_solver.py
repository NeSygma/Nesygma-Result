from z3 import *

solver = Solver()

# Declare boolean variables
M = Bool('M')
O = Bool('O')
P = Bool('P')
S = Bool('S')
T = Bool('T')
W = Bool('W')
Y = Bool('Y')
Z = Bool('Z')

# Base constraints
# At least 4 employees
solver.add(Sum([If(M, 1, 0), If(O, 1, 0), If(P, 1, 0), If(S, 1, 0), If(T, 1, 0), If(W, 1, 0), If(Y, 1, 0), If(Z, 1, 0)]) >= 4)

# Constraints
solver.add(Implies(M, And(Not(O), Not(P))))
solver.add(Implies(S, And(P, T)))
solver.add(Implies(W, And(M, Y)))
solver.add(Not(P))

# Option constraints
opt_a_constr = And(Not(M), Not(O))
opt_b_constr = And(Not(M), Not(T))
opt_c_constr = And(Not(M), Not(Z))
opt_d_constr = And(Not(O), Not(T))
opt_e_constr = And(Not(O), Not(Y))

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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