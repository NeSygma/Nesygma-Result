from z3 import *

# Define solver and variables
solver = Solver()
# Variables for positions 1..6
G = Int('G')  # guitarist
K = Int('K')  # keyboard
P = Int('P')  # percussion
S = Int('S')  # saxophonist
T = Int('T')  # trumpeter
V = Int('V')  # violinist
vars = [G, K, P, S, T, V]
# Domain constraints
for v in vars:
    solver.add(v >= 1, v <= 6)
# All distinct
solver.add(Distinct(vars))
# Base constraints
solver.add(G != 4)  # guitarist not fourth
solver.add(P < K)   # percussion before keyboard
solver.add(V < K, K < G)  # violin before keyboard before guitarist
# Sax after either percussion or trumpeter but not both (XOR)
cond1 = S > P
cond2 = S > T
solver.add(Xor(cond1, cond2))

# Option constraints
opt_a_constr = (K == 1)
opt_b_constr = (G == 2)
opt_c_constr = (G < S)
opt_d_constr = (G < P)
opt_e_constr = (K < S)

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