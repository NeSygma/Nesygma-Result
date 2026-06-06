from z3 import *
solver = Solver()

# Variables
G, K, P, S, T, V = Ints('G K P S T V')

# Domain constraints
for var in [G, K, P, S, T, V]:
    solver.add(var >= 1, var <= 6)

# Distinct
solver.add(Distinct(G, K, P, S, T, V))

# Base constraints
solver.add(G != 4)
solver.add(P < K)
solver.add(V < K)
solver.add(K < G)
solver.add(Xor(S > P, S > T))

# Assumption: V == 4
solver.add(V == 4)

# Option negations
opt_a_constr = Not(P < V)   # P >= V
opt_b_constr = Not(T < V)   # T >= V
opt_c_constr = Not(T < G)   # T >= G
opt_d_constr = Not(S < V)   # S >= V
opt_e_constr = Not(T < S)   # T >= S

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