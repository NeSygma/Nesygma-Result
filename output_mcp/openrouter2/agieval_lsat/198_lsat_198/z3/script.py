from z3 import *
solver = Solver()

# Variables
H = Int('H')
L = Int('L')
M = Int('M')
S = Int('S')
T = Int('T')
V = Int('V')

# Domain constraints
solver.add(H >= 1, H <= 6)
solver.add(L >= 1, L <= 6)
solver.add(M >= 1, M <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)

# Distinct
solver.add(Distinct(H, L, M, S, T, V))

# Constraints
solver.add(S != 1)
solver.add(Implies(H < L, M < L))
solver.add(S < M)
solver.add(S < V)
solver.add(Xor(T < H, T < V))

# Assumption: T > M and T > V
solver.add(T > M)
solver.add(T > V)

# Options
opt_a_constr = H < T
opt_b_constr = T < L
opt_c_constr = T < S
opt_d_constr = M < V
opt_e_constr = S < L

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