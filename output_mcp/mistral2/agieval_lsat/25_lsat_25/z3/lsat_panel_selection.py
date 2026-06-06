from z3 import *

solver = Solver()

# Declare symbolic variables for each scientist (True if selected, False otherwise)
# Botanists
F = Bool('F')
G = Bool('G')
H = Bool('H')

# Chemists
K = Bool('K')
L = Bool('L')
M = Bool('M')

# Zoologists
P = Bool('P')
Q = Bool('Q')
R = Bool('R')

# Base constraints:
# 1. The panel must include at least one scientist of each of the three types.
# At least one botanist
solver.add(Or(F, G, H))
# At least one chemist
solver.add(Or(K, L, M))
# At least one zoologist
solver.add(Or(P, Q, R))

# 2. If more than one botanist is selected, then at most one zoologist is selected.
# This is equivalent to: If two or more botanists are selected, then the number of zoologists <= 1
# We can express this as: (number of botanists > 1) implies (number of zoologists <= 1)
# Which is equivalent to: (number of botanists <= 1) or (number of zoologists <= 1)
# We can encode this as a constraint:
botanists = [F, G, H]
zoologists = [P, Q, R]

# Count botanists
num_botanists = Sum([If(b, 1, 0) for b in botanists])
# Count zoologists
num_zoologists = Sum([If(z, 1, 0) for z in zoologists])

# If num_botanists > 1, then num_zoologists <= 1
solver.add(Implies(num_botanists > 1, num_zoologists <= 1))

# 3. F and K cannot both be selected.
solver.add(Not(And(F, K)))

# 4. K and M cannot both be selected.
solver.add(Not(And(K, M)))

# 5. If M is selected, both P and R must be selected.
solver.add(Implies(M, And(P, R)))

# Panel size is exactly 5
panel_size = Sum([If(b, 1, 0) for b in [F, G, H, K, L, M, P, Q, R]]) == 5
solver.add(panel_size)

# Define the options as constraints
# Option A: F, G, K, P, Q
opt_a_constr = And(F, G, K, P, Q, 
                   Not(H), Not(L), Not(M), Not(R))

# Option B: G, H, K, L, M
opt_b_constr = And(G, H, K, L, M, 
                   Not(F), Not(P), Not(Q), Not(R))

# Option C: G, H, K, L, R
opt_c_constr = And(G, H, K, L, R, 
                   Not(F), Not(M), Not(P), Not(Q))

# Option D: H, K, M, P, R
opt_d_constr = And(H, K, M, P, R, 
                   Not(F), Not(G), Not(L), Not(Q))

# Option E: H, L, M, P, Q
opt_e_constr = And(H, L, M, P, Q, 
                   Not(F), Not(G), Not(K), Not(R))

# Evaluate each option
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