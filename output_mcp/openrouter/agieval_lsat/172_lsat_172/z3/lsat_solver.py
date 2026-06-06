from z3 import *

solver = Solver()

# Variables: counts per section and photographer
L_F = Int('L_F')
L_G = Int('L_G')
L_H = Int('L_H')
M_F = Int('M_F')
M_G = Int('M_G')
M_H = Int('M_H')
S_F = Int('S_F')
S_G = Int('S_G')
S_H = Int('S_H')
vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]

# Domain constraints: each count between 0 and 2 (since each section has 2 photos)
for v in vars:
    solver.add(v >= 0, v <= 2)

# Section totals = 2
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Photographer overall totals between 1 and 3
for total in [L_F + M_F + S_F, L_G + M_G + S_G, L_H + M_H + S_H]:
    solver.add(total >= 1, total <= 3)

# Given condition: Lifestyle has one Fuentes and one Hue (no G)
solver.add(L_F == 1)
solver.add(L_H == 1)
solver.add(L_G == 0)

# No Gagnon in Sports
solver.add(S_G == 0)

# Hue in Lifestyle equals Fuentes in Sports
solver.add(L_H == S_F)

# At least one photographer appears in both Lifestyle and Metro
# Since L only has F and H, this reduces to (M_F >=1) or (M_H >=1)
solver.add(Or(M_F >= 1, M_H >= 1))

# Define option constraints
opt_a_constr = And(M_F == 2, M_G == 0, M_H == 0)
opt_b_constr = And(M_F == 0, M_G == 2, M_H == 0)
opt_c_constr = And(M_H == 1, M_F + M_G == 1)  # exactly one non-H, will be G to satisfy G>=1
opt_d_constr = And(S_H == 2, S_F == 0, S_G == 0)
opt_e_constr = And(S_H == 0, S_F + S_G == 2)  # with S_G==0 forces S_F==2

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