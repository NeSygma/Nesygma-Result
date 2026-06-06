from z3 import *

# Declare variables for counts
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

solver = Solver()
# Base constraints
vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
for v in vars:
    solver.add(v >= 0)
# Section totals
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)
# Photographer totals between 1 and 3
F_total = L_F + M_F + S_F
G_total = L_G + M_G + S_G
H_total = L_H + M_H + S_H
solver.add(F_total >= 1, F_total <= 3)
solver.add(G_total >= 1, G_total <= 3)
solver.add(H_total >= 1, H_total <= 3)
# At least one photographer appears in both Lifestyle and Metro
solver.add(Or(And(L_F >= 1, M_F >= 1), And(L_G >= 1, M_G >= 1), And(L_H >= 1, M_H >= 1)))
# Hue in Lifestyle equals Fuentes in Sports
solver.add(L_H == S_F)
# No Gagnon in Sports
solver.add(S_G == 0)

# Define option constraints
opt_a = [L_F == 2, L_G == 0, L_H == 0,
         M_F == 1, M_G == 0, M_H == 1,
         S_F == 0, S_G == 1, S_H == 1]
opt_b = [L_F == 1, L_G == 1, L_H == 0,
         M_F == 1, M_G == 1, M_H == 0,
         S_F == 0, S_G == 0, S_H == 2]
opt_c = [L_F == 2, L_G == 0, L_H == 0,
         M_F == 0, M_G == 2, M_H == 0,
         S_F == 0, S_G == 0, S_H == 2]
opt_d = [L_F == 0, L_G == 2, L_H == 0,
         M_F == 1, M_G == 1, M_H == 0,
         S_F == 1, S_G == 0, S_H == 1]
opt_e = [L_F == 0, L_G == 1, L_H == 1,
         M_F == 0, M_G == 0, M_H == 2,
         S_F == 1, S_G == 0, S_H == 1]

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
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