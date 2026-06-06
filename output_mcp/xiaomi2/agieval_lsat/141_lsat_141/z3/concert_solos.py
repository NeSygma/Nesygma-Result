from z3 import *

solver = Solver()

# Each member has a solo position (1-6), all distinct
G = Int('G')  # guitarist
K = Int('K')  # keyboard player
P = Int('P')  # percussionist
S = Int('S')  # saxophonist
T = Int('T')  # trumpeter
V = Int('V')  # violinist

members = [G, K, P, S, T, V]

# All positions 1-6, all distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: Guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: Percussionist before keyboard player
solver.add(P < K)

# Constraint 3: Keyboard player after violinist and before guitarist
solver.add(V < K)
solver.add(K < G)

# Constraint 4: Saxophonist after exactly one of percussionist or trumpeter (XOR)
# (P < S) XOR (T < S)
solver.add(Xor(P < S, T < S))

# Now test each option
# "Must be false EXCEPT" = which one CAN be true (is satisfiable)

opt_a = (K == 1)  # keyboard player performs first solo
opt_b = (G == 2)  # guitarist performs second solo
opt_c = (G < S)   # guitarist before saxophonist
opt_d = (G < P)   # guitarist before percussionist
opt_e = (K < S)   # keyboard player before saxophonist

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: G={m[G]}, K={m[K]}, P={m[P]}, S={m[S]}, T={m[T]}, V={m[V]}")
    else:
        print(f"Option {letter} is UNSAT (must be false)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")