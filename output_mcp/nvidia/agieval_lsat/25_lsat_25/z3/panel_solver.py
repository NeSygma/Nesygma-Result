from z3 import *
solver = Solver()

# Declare Boolean variables for each scientist
F = Bool('F')
G = Bool('G')
H = Bool('H')
K = Bool('K')
L = Bool('L')
M = Bool('M')
P = Bool('P')
Q = Bool('Q')
R = Bool('R')

# Helper to count selections
def count_bool_vars(*vars):
    return Sum([If(v, 1, 0) for v in vars])

# Count each group
num_botanist = count_bool_vars(F, G, H)
num_chemist = count_bool_vars(K, L, M)
num_zoologist = count_bool_vars(P, Q, R)

# Exactly five scientists selected
solver.add(Sum([If(v, 1, 0) for v in [F,G,H,K,L,M,P,Q,R]]) == 5)

# At least one of each type
solver.add(num_botanist >= 1)
solver.add(num_chemist >= 1)
solver.add(num_zoologist >= 1)

# If more than one botanist selected, then at most one zoologist selected
solver.add(Not(And(num_botanist >= 2, num_zoologist >= 2)))

# F and K cannot both be selected
solver.add(Not(And(F, K)))

# K and M cannot both be selected
solver.add(Not(And(K, M)))

# If M is selected, both P and R must be selected
solver.add(Or(Not(M), And(P, R)))

# Define option constraints
opt_a_constr = And(F, G, K, P, Q, Not(H), Not(L), Not(M), Not(R))
opt_b_constr = And(G, H, K, L, M, Not(F), Not(P), Not(Q), Not(R))
opt_c_constr = And(G, H, K, L, R, Not(F), Not(M), Not(P), Not(Q))
opt_d_constr = And(H, K, M, P, R, Not(F), Not(G), Not(L), Not(Q))
opt_e_constr = And(H, L, M, P, Q, Not(F), Not(G), Not(K), Not(R))

# List of options
options = [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]

found_options = []
for letter, constr in options:
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