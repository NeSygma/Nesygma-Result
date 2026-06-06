from z3 import *

# Bool variables: True = Fall, False = Spring
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

solver = Solver()
# Base constraints
solver.add(M != P)               # M and P cannot be same season
solver.add(K == N)               # K and N same season
solver.add(Implies(K, O))        # If K is fall then O is fall
solver.add(Implies(M, Not(N)))   # If M is fall then N is spring (i.e., not fall)
# Assumption: M is fall
solver.add(M == True)

# Define option constraints
opt_a_constr = And(K == True, O == True)          # A: K and O fall
opt_b_constr = And(L == True, N == True)          # B: L and N fall
opt_c_constr = And(L == True, O == True)          # C: L and O fall
opt_d_constr = And(N == True, P == True)          # D: N and P fall
opt_e_constr = And(O == True, P == True)          # E: O and P fall

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