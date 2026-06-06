from z3 import *

solver = Solver()

# ---------- Variables ----------
# Counts of photographs per section (Lifestyle L, Metro M, Sports S)
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# ---------- Base constraints ----------
# Each section has exactly two photographs
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# No Gagnon photographs in Sports
solver.add(S_G == 0)

# At least one but no more than three photographs per photographer overall
total_F = L_F + M_F + S_F
total_G = L_G + M_G + S_G
total_H = L_H + M_H + S_H
solver.add(And(total_F >= 1, total_F <= 3))
solver.add(And(total_G >= 1, total_G <= 3))
solver.add(And(total_H >= 1, total_H <= 3))

# Number of Hue's photos in Lifestyle equals number of Fuentes photos in Sports
solver.add(L_H == S_F)

# At least one photo in Lifestyle must be by a photographer who also has a photo in Metro
# Since both Lifestyle photos are Hue (given), Hue must appear in Metro
solver.add(L_H >= 1)          # given condition (both are Hue)
solver.add(L_F == 0, L_G == 0)  # both Lifestyle photos are Hue
solver.add(M_H >= 1)          # Hue appears in Metro

# ---------- Option constraints ----------
# A: Exactly one photograph is by Fuentes
opt_a_constr = (total_F == 1)

# B: Exactly three photographs are by Fuentes
opt_b_constr = (total_F == 3)

# C: Exactly one photograph is by Gagnon
opt_c_constr = (total_G == 1)

# D: Exactly two photographs are by Gagnon
opt_d_constr = (total_G == 2)

# E: Exactly two photographs are by Hue
opt_e_constr = (total_H == 2)

# ---------- Test each option ----------
found_options = []
for letter, constr in [("A", opt_a_constr),
                       ("B", opt_b_constr),
                       ("C", opt_c_constr),
                       ("D", opt_d_constr),
                       ("E", opt_e_constr)]:
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