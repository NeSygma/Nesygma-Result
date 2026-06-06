from z3 import *

solver = Solver()

# Variables: counts of each photographer's photos in each section
# L = Lifestyle, M = Metro, S = Sports
# F = Fuentes, G = Gagnon, H = Hue
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Domain constraints: each count is between 0 and 2
for var in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
    solver.add(var >= 0, var <= 2)

# Constraint 1: Each section has exactly 2 photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Constraint 2: For each photographer, at least 1 but no more than 3 photos total
solver.add(L_F + M_F + S_F >= 1)
solver.add(L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1)
solver.add(L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1)
solver.add(L_H + M_H + S_H <= 3)

# Constraint 3: At least one photo in Lifestyle by a photographer who also has at least one in Metro
solver.add(Or(And(L_F >= 1, M_F >= 1), And(L_G >= 1, M_G >= 1), And(L_H >= 1, M_H >= 1)))

# Constraint 4: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(L_H == S_F)

# Constraint 5: None of Gagnon's photos can be in Sports
solver.add(S_G == 0)

# Premise: Both photographs in one of the three sections are by Gagnon
# Since S_G = 0, it can only be Lifestyle or Metro
premise = Or(L_G == 2, M_G == 2)
solver.add(premise)

# Check each option as "could be true" under these constraints
# Option A: Both photographs in Lifestyle are by Hue
opt_a = (L_H == 2)
# Option B: One in Lifestyle by Fuentes and one by Hue
opt_b = And(L_F == 1, L_H == 1)
# Option C: Both in Metro by Fuentes
opt_c = (M_F == 2)
# Option D: One in Metro by Gagnon and one by Hue
opt_d = And(M_G == 1, M_H == 1)
# Option E: Both in Sports by Hue
opt_e = (S_H == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT, model:")
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