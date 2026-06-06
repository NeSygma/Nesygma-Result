from z3 import *

solver = Solver()

# Variables: counts per section and photographer
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Non-negativity
vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
for v in vars:
    solver.add(v >= 0)

# Section totals = 2
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Given: both Lifestyle photos are Hue
solver.add(L_H == 2)
solver.add(L_F == 0, L_G == 0)

# No Gagnon in Sports
solver.add(S_G == 0)

# Photographer totals between 1 and 3
total_F = L_F + M_F + S_F
total_G = L_G + M_G + S_G
total_H = L_H + M_H + S_H
solver.add(And(total_F >= 1, total_F <= 3))
solver.add(And(total_G >= 1, total_G <= 3))
solver.add(And(total_H >= 1, total_H <= 3))

# Hue in Lifestyle equals Fuentes in Sports
solver.add(L_H == S_F)

# At least one photographer appears in both Lifestyle and Metro
# Since only Hue in Lifestyle, Hue must appear in Metro
solver.add(M_H >= 1)

# Option constraints
opt_a = (total_F == 1)
opt_b = (total_F == 3)
opt_c = (total_G == 1)
opt_d = (total_G == 2)
opt_e = (total_H == 2)

found = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")