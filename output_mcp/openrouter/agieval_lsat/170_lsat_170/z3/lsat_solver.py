from z3 import *

# Base constraints
# Variables: counts per photographer per section
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

solver = Solver()
# Section totals
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)
# Given condition: Lifestyle has one G and one H
solver.add(L_G == 1)
solver.add(L_H == 1)
solver.add(L_F == 0)
# Photographer overall counts between 1 and 3
# Fuentes
total_F = L_F + M_F + S_F
solver.add(total_F >= 1, total_F <= 3)
# Gagnon
total_G = L_G + M_G + S_G
solver.add(total_G >= 1, total_G <= 3)
# Hue
total_H = L_H + M_H + S_H
solver.add(total_H >= 1, total_H <= 3)
# Intersection condition: at least one photographer appears in both Lifestyle and Metro
# Since Lifestyle has G and H, require M_G > 0 or M_H > 0
solver.add(Or(M_G > 0, M_H > 0))
# Equality condition: Hue in Lifestyle equals Fuentes in Sports
solver.add(L_H == S_F)
# No Gagnon in Sports
solver.add(S_G == 0)

# Define option constraints (the statement that the option is true)
opt_a_constr = (M_F == 1)                     # Exactly one Fuentes in Metro
opt_b_constr = (M_G == 1)                     # Exactly one Gagnon in Metro
opt_c_constr = And(M_G == 2, M_F == 0, M_H == 0)  # Both Metro photos by Gagnon
opt_d_constr = (S_H == 1)                     # Exactly one Hue in Sports
opt_e_constr = (S_H == 2)                     # Both Sports photos by Hue

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option is forced (must be true). It is the one that appears in all models.
# An option is forced iff its negation is unsat. We can compute forced set by checking unsat of Not(constr).
forced_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        forced_options.append(letter)
    solver.pop()

if len(forced_options) == 1:
    print("STATUS: sat")
    print(f"answer:{forced_options[0]}")
elif len(found_options) == 1:
    # fallback if only one option is possible
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: found_options={found_options}, forced_options={forced_options}")