from z3 import *

solver = Solver()
# Variables for positions of each member (1..6)
G, K, P, S, T, V = Ints('G K P S T V')
# Domain constraints
solver.add(G >= 1, G <= 6)
solver.add(K >= 1, K <= 6)
solver.add(P >= 1, P <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
# All distinct
solver.add(Distinct(G, K, P, S, T, V))
# Base constraints
solver.add(G != 4)  # guitarist not fourth
solver.add(P < K)   # percussion before keyboard
solver.add(V < K)   # violin before keyboard
solver.add(K < G)   # keyboard before guitarist
solver.add(Xor(S > P, S > T))  # sax after either percussion or trumpet, but not both

# Option constraints
opt_a_constr = [V == 1, P == 2, S == 3, G == 4, T == 5, K == 6]
opt_b_constr = [P == 1, V == 2, K == 3, T == 4, S == 5, G == 6]
opt_c_constr = [V == 1, T == 2, S == 3, P == 4, K == 5, G == 6]
opt_d_constr = [K == 1, T == 2, V == 3, S == 4, G == 5, P == 6]
opt_e_constr = [G == 1, V == 2, K == 3, P == 4, S == 5, T == 6]

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