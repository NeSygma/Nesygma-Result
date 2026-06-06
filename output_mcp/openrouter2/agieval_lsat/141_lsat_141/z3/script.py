from z3 import *
solver = Solver()
# declare variables
G = Int('G')
K = Int('K')
P = Int('P')
S = Int('S')
T = Int('T')
V = Int('V')
# domain constraints
solver.add(G >= 1, G <= 6)
solver.add(K >= 1, K <= 6)
solver.add(P >= 1, P <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
# distinct
solver.add(Distinct(G, K, P, S, T, V))
# base constraints
solver.add(G != 4)
solver.add(P < K)
solver.add(V < K)
solver.add(K < G)
solver.add(Xor(S > P, S > T))
# option constraints
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