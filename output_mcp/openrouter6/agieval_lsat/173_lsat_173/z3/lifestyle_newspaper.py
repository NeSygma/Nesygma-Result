from z3 import *

solver = Solver()

# Variables for counts per section per photographer
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Domain constraints: each count between 0 and 2
solver.add(L_F >= 0, L_F <= 2)
solver.add(L_G >= 0, L_G <= 2)
solver.add(L_H >= 0, L_H <= 2)
solver.add(M_F >= 0, M_F <= 2)
solver.add(M_G >= 0, M_G <= 2)
solver.add(M_H >= 0, M_H <= 2)
solver.add(S_F >= 0, S_F <= 2)
solver.add(S_G >= 0, S_G <= 2)
solver.add(S_H >= 0, S_H <= 2)

# Each section has exactly two photographs
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

# At least one photograph in Lifestyle by a photographer who also has at least one in Metro
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Number of Hue's photographs in Lifestyle equals number of Fuentes photographs in Sports
solver.add(L_H == S_F)

# None of Gagnon's photographs in Sports
solver.add(S_G == 0)

# Extra condition: both photographs in one section are by Gagnon (Lifestyle or Metro, since Sports cannot have Gagnon)
solver.add(Or(L_G == 2, M_G == 2))

# Answer choices constraints
opt_a = (L_H == 2)
opt_b = And(L_F == 1, L_H == 1)  # implies L_G == 0 automatically due to section total
opt_c = (M_F == 2)
opt_d = And(M_G == 1, M_H == 1)  # implies M_F == 0
opt_e = (S_H == 2)

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