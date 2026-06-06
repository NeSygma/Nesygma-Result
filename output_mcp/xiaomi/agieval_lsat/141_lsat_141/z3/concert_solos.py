from z3 import *

solver = Solver()

# Define the six band members and their solo positions (1-6)
# G=guitarist, K=keyboard, P=percussionist, S=saxophonist, T=trumpeter, V=violinist
G, K, P, S, T, V = Ints('G K P S T V')
members = [G, K, P, S, T, V]

# Each member performs exactly one solo, positions 1-6, all distinct
for m in members:
    solver.add(m >= 1, m <= 6)
solver.add(Distinct(members))

# Constraint 1: The guitarist does not perform the fourth solo
solver.add(G != 4)

# Constraint 2: The percussionist performs a solo at some time before the keyboard player does
solver.add(P < K)

# Constraint 3: The keyboard player performs a solo at some time after the violinist does
# and at some time before the guitarist does
solver.add(V < K)
solver.add(K < G)

# Constraint 4: The saxophonist performs a solo at some time after either the percussionist
# does or the trumpeter does, but not both
# "after P or after T, but not both" means:
# (S > P XOR S > T) -- exactly one of these is true
solver.add(Xor(S > P, S > T))

# Define option constraints
# (A) The keyboard player performs the first solo
opt_a = (K == 1)

# (B) The guitarist performs the second solo
opt_b = (G == 2)

# (C) The guitarist performs a solo at some time before the saxophonist does
opt_c = (G < S)

# (D) The guitarist performs a solo at some time before the percussionist does
opt_d = (G < P)

# (E) The keyboard player performs a solo at some time before the saxophon does
opt_e = (K < S)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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