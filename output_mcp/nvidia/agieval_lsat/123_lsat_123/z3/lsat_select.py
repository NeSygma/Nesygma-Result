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
solver.add(Sum([M, O, P, S, T, W, Y, Z]) >= 4)
solver.add(Implies(M, Not(O)))
solver.add(Implies(M, Not(P)))
solver.add(Implies(S, P))
solver.add(Implies(S, T))
solver.add(Implies(W, M))
solver.add(Implies(W, Y))

# Option constraints
opt_a_constr = And(M == True, O == False, P == True, S == True, T == True, W == False, Y == False, Z == False)
opt_b_constr = And(O == True, P == True, T == True, Z == True, M == False, S == False, W == False, Y == False)
opt_c_constr = And(P == True, S == True, Y == True, Z == True, M == False, O == False, T == False, W == False)
opt_d_constr = And(S == True, T == True, Y == True, Z == True, M == False, O == False, P == False, W == False)
opt_e_constr = And(T == True, W == True, Y == True, Z == True, M == False, O == False, P == False, S == False)

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