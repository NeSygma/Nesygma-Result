from z3 import *

# Define variables for each cookbook: True if published in fall, False if spring
K = Bool('K')
L = Bool('L')
M = Bool('M')
N = Bool('N')
O = Bool('O')
P = Bool('P')

# Base constraints: none (any assignment is allowed)
solver = Solver()

# Option constraints
opt_a = And(K, L, M, O, Not(N), Not(P))
opt_b = And(K, L, N, O, Not(M), Not(P))
opt_c = And(K, L, N, P, Not(M), Not(O))
opt_d = And(K, M, N, O, Not(L), Not(P))
opt_e = And(M, O, Not(K), Not(L), Not(N), Not(P))

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