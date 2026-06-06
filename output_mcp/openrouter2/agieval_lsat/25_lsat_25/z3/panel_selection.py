from z3 import *

solver = Solver()
# Define boolean variables for each scientist
F = Bool('F')
G = Bool('G')
H = Bool('H')
K = Bool('K')
L = Bool('L')
M = Bool('M')
P = Bool('P')
Q = Bool('Q')
R = Bool('R')

# Base constraints
# Exactly 5 selected
solver.add(Sum([If(F,1,0), If(G,1,0), If(H,1,0), If(K,1,0), If(L,1,0), If(M,1,0), If(P,1,0), If(Q,1,0), If(R,1,0)]) == 5)
# At least one botanist
solver.add(Sum([If(F,1,0), If(G,1,0), If(H,1,0)]) >= 1)
# At least one chemist
solver.add(Sum([If(K,1,0), If(L,1,0), If(M,1,0)]) >= 1)
# At least one zoologist
solver.add(Sum([If(P,1,0), If(Q,1,0), If(R,1,0)]) >= 1)
# If more than one botanist, then at most one zoologist
solver.add(Implies(Sum([If(F,1,0), If(G,1,0), If(H,1,0)]) > 1,
                   Sum([If(P,1,0), If(Q,1,0), If(R,1,0)]) <= 1))
# F and K cannot both be selected
solver.add(Not(And(F, K)))
# K and M cannot both be selected
solver.add(Not(And(K, M)))
# If M is selected, both P and R must be selected
solver.add(Implies(M, And(P, R)))

# Define option constraints
opt_a_constr = And(F, G, K, P, Q, Not(H), Not(L), Not(M), Not(R))
opt_b_constr = And(G, H, K, L, M, Not(F), Not(P), Not(Q), Not(R))
opt_c_constr = And(G, H, K, L, R, Not(F), Not(M), Not(P), Not(Q))
opt_d_constr = And(H, K, M, P, R, Not(F), Not(G), Not(L), Not(Q))
opt_e_constr = And(H, L, M, P, Q, Not(F), Not(G), Not(K), Not(R))

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