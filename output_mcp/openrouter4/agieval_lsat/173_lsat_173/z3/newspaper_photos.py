from z3 import *

solver = Solver()

# Variables: counts per photographer per section
# Lifestyle: L_F, L_G, L_H
L_F = Int('L_F')
L_G = Int('L_G')
L_H = Int('L_H')

# Metro: M_F, M_G, M_H
M_F = Int('M_F')
M_G = Int('M_G')
M_H = Int('M_H')

# Sports: S_F, S_G, S_H
S_F = Int('S_F')
S_G = Int('S_G')
S_H = Int('S_H')

# Domain constraints: each count between 0 and 2
all_vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
for v in all_vars:
    solver.add(v >= 0, v <= 2)

# Each section has exactly 2 photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Each photographer appears 1 to 3 times total
solver.add(L_F + M_F + S_F >= 1)
solver.add(L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1)
solver.add(L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1)
solver.add(L_H + M_H + S_H <= 3)

# Constraint 2: At least one photo in Lifestyle is by a photographer who also has at least one photo in Metro
# i.e., (L_F >= 1 and M_F >= 1) or (L_G >= 1 and M_G >= 1) or (L_H >= 1 and M_H >= 1)
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(L_H == S_F)

# Constraint 4: No Gagnon photos in Sports
solver.add(S_G == 0)

# Additional condition: Both photographs in one of the three sections are by Gagnon
# S_G = 0, so it must be Lifestyle or Metro
solver.add(Or(L_G == 2, M_G == 2))

# Now test each option
# Option A: Both photos in Lifestyle are by Hue -> L_H = 2
opt_a_constr = (L_H == 2)

# Option B: One photo in Lifestyle by Fuentes and one by Hue -> L_F = 1, L_H = 1
opt_b_constr = And(L_F == 1, L_H == 1)

# Option C: Both photos in Metro are by Fuentes -> M_F = 2
opt_c_constr = (M_F == 2)

# Option D: One photo in Metro by Gagnon and one by Hue -> M_G = 1, M_H = 1
opt_d_constr = And(M_G == 1, M_H == 1)

# Option E: Both photos in Sports are by Hue -> S_H = 2
opt_e_constr = (S_H == 2)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        print(f"Option {letter} is SAT. Model:")
        m = solver.model()
        print(f"  L: F={m[L_F]}, G={m[L_G]}, H={m[L_H]}")
        print(f"  M: F={m[M_F]}, G={m[M_G]}, H={m[M_H]}")
        print(f"  S: F={m[S_F]}, G={m[S_G]}, H={m[S_H]}")
    else:
        print(f"Option {letter} is UNSAT")
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