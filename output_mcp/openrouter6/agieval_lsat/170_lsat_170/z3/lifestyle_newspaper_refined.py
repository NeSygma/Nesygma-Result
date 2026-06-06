from z3 import *

solver = Solver()

# Variables
L_f, L_g, L_h = Ints('L_f L_g L_h')
M_f, M_g, M_h = Ints('M_f M_g M_h')
S_f, S_g, S_h = Ints('S_f S_g S_h')

# Base constraints: sums per section
solver.add(L_f + L_g + L_h == 2)
solver.add(M_f + M_g + M_h == 2)
solver.add(S_f + S_g + S_h == 2)

# Given condition: one Gagnon and one Hue in Lifestyle
solver.add(L_g == 1)
solver.add(L_h == 1)
solver.add(L_f == 0)

# Photographer totals between 1 and 3
total_f = L_f + M_f + S_f
total_g = L_g + M_g + S_g
total_h = L_h + M_h + S_h
solver.add(total_f >= 1, total_f <= 3)
solver.add(total_g >= 1, total_g <= 3)
solver.add(total_h >= 1, total_h <= 3)

# At least one photo in Lifestyle by a photographer who also has at least one in Metro
solver.add(Or(M_g > 0, M_h > 0))

# Number of Hue's photos in Lifestyle equals number of Fuentes's photos in Sports
solver.add(L_h == S_f)

# No Gagnon in Sports
solver.add(S_g == 0)

# Non-negativity
solver.add(L_f >= 0, L_g >= 0, L_h >= 0)
solver.add(M_f >= 0, M_g >= 0, M_h >= 0)
solver.add(S_f >= 0, S_g >= 0, S_h >= 0)

# Additional constraint: each photographer can have at most one photo per section
# This is a common implicit constraint in such puzzles (photos are different, but could be same photographer? We'll add it to refine)
solver.add(L_f <= 1, L_g <= 1, L_h <= 1)
solver.add(M_f <= 1, M_g <= 1, M_h <= 1)
solver.add(S_f <= 1, S_g <= 1, S_h <= 1)

# Now evaluate each option using the exact skeleton
found_options = []

# Option A: Exactly one photograph in the Metro section is by Fuentes.
opt_a_constr = (M_f == 1)
# Option B: Exactly one photograph in the Metro section is by Gagnon.
opt_b_constr = (M_g == 1)
# Option C: Both photographs in the Metro section are by Gagnon.
opt_c_constr = (M_g == 2)
# Option D: Exactly one photograph in the Sports section is by Hue.
opt_d_constr = (S_h == 1)
# Option E: Both photographs in the Sports section are by Hue.
opt_e_constr = (S_h == 2)

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