from z3 import *

# Constants for photographers
F, G, H = 0, 1, 2

# Variables for each photo slot
L1, L2 = Ints('L1 L2')
M1, M2 = Ints('M1 M2')
S1, S2 = Ints('S2 S1')  # note order swapped but fine

vars = [L1, L2, M1, M2, S1, S2]
solver = Solver()

# Domain constraints
for v in vars:
    solver.add(Or(v == F, v == G, v == H))

# Base constraints
# 1. Each photographer appears at least 1 and at most 3 times overall
for p in [F, G, H]:
    cnt = Sum([If(v == p, 1, 0) for v in vars])
    solver.add(cnt >= 1, cnt <= 3)

# 2. Metro section: exactly one Fuentes and one Hue, no Gagnon
solver.add(Sum([If(M1 == F, 1, 0), If(M2 == F, 1, 0)]) == 1)
solver.add(Sum([If(M1 == H, 1, 0), If(M2 == H, 1, 0)]) == 1)
solver.add(Sum([If(M1 == G, 1, 0), If(M2 == G, 1, 0)]) == 0)

# 3. At least one photographer appears in both Lifestyle and Metro
# Define predicates for presence in Lifestyle
F_in_L = Or(L1 == F, L2 == F)
G_in_L = Or(L1 == G, L2 == G)
H_in_L = Or(L1 == H, L2 == H)
# Presence in Metro (we already know counts, but define)
F_in_M = Or(M1 == F, M2 == F)
G_in_M = Or(M1 == G, M2 == G)
H_in_M = Or(M1 == H, M2 == H)
solver.add(Or(And(F_in_L, F_in_M), And(G_in_L, G_in_M), And(H_in_L, H_in_M)))

# 4. Hue's photos in Lifestyle equal Fuentes photos in Sports
cnt_H_L = Sum([If(L1 == H, 1, 0), If(L2 == H, 1, 0)])
cnt_F_S = Sum([If(S1 == F, 1, 0), If(S2 == F, 1, 0)])
solver.add(cnt_H_L == cnt_F_S)

# 5. No Gagnon in Sports
solver.add(S1 != G, S2 != G)

# Option constraints definitions
opt_a = And(L1 == F, L2 == F)  # both Lifestyle by Fuentes
opt_b = And(L1 == G, L2 == G)  # both by Gagnon
opt_c = Or(And(L1 == G, L2 == H), And(L1 == H, L2 == G))  # one G one H
opt_d = And(L1 == H, L2 == H)  # both Hue
opt_e = And(S1 == F, S2 == F)  # both Sports Fuentes

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