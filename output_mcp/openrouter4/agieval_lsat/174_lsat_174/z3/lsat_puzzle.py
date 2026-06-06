from z3 import *

solver = Solver()

# Variables: counts of each photographer in each section
# Each variable is an integer from 0 to 2
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Domain constraints: 0 to 2
all_vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
for v in all_vars:
    solver.add(v >= 0)
    solver.add(v <= 2)

# Each section has exactly 2 photographs
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Constraint 1: For each photographer, at least 1 but no more than 3 total
solver.add(L_F + M_F + S_F >= 1)
solver.add(L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1)
solver.add(L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1)
solver.add(L_H + M_H + S_H <= 3)

# Constraint 2: At least one photo in Lifestyle is by a photographer who has at least one photo in Metro
# (L_F >= 1 and M_F >= 1) OR (L_G >= 1 and M_G >= 1) OR (L_H >= 1 and M_H >= 1)
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes's photos in Sports
solver.add(L_H == S_F)

# Constraint 4: No Gagnon in Sports
solver.add(S_G == 0)

# Given condition: One photo in Metro is by Fuentes and one is by Hue
solver.add(M_F == 1)
solver.add(M_H == 1)
# So M_G must be 0 (since total is 2), but that's implied by the constraints

# Now evaluate each option
found_options = []

# Option A: Both photographs in Lifestyle are by Fuentes
opt_a = And(L_F == 2, L_G == 0, L_H == 0)

# Option B: Both photographs in Lifestyle are by Gagnon
opt_b = And(L_F == 0, L_G == 2, L_H == 0)

# Option C: One in Lifestyle is by Gagnon and one is by Hue
opt_c = And(L_F == 0, L_G == 1, L_H == 1)

# Option D: Both photographs in Lifestyle are by Hue
opt_d = And(L_F == 0, L_G == 0, L_H == 2)

# Option E: Both photographs in Sports are by Fuentes
opt_e = And(S_F == 2, S_G == 0, S_H == 0)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        # Print model for the valid option
        m = solver.model()
        print(f"Option {letter} is SAT. Model:")
        print(f"  L: F={m[L_F]}, G={m[L_G]}, H={m[L_H]}")
        print(f"  M: F={m[M_F]}, G={m[M_G]}, H={m[M_H]}")
        print(f"  S: F={m[S_F]}, G={m[S_G]}, H={m[S_H]}")
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