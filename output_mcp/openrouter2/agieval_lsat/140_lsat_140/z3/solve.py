from z3 import *

solver = Solver()
# Variables for positions of each member
G = Int('G')
K = Int('K')
P = Int('P')
S = Int('S')
T = Int('T')
V = Int('V')

# Domain constraints: positions 1..6
for var in [G,K,P,S,T,V]:
    solver.add(var >= 1, var <= 6)

# All distinct
solver.add(Distinct([G,K,P,S,T,V]))

# Base constraints
solver.add(G != 4)  # guitarist not fourth
solver.add(P < K)   # percussion before keyboard
solver.add(V < K)   # violin before keyboard
solver.add(K < G)   # keyboard before guitarist
# Saxophonist after either percussion or trumpet, but not both
solver.add(Xor(S > P, S > T))

# Additional assumption: percussion before saxophonist
solver.add(P < S)

# Option constraints
opt_a_constr = (P == 1)
opt_b_constr = (P == 2)
opt_c_constr = (V < S)
opt_d_constr = (P < T)
opt_e_constr = (S < K)

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