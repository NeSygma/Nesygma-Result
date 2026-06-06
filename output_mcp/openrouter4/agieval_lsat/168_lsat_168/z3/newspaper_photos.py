from z3 import *

solver = Solver()

# Variables: for each section (L, M, S) and photographer (F, G, H), how many photos?
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Domain: each count is between 0 and 2 (at most 2 photos per section)
all_vars = [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]
for v in all_vars:
    solver.add(v >= 0, v <= 2)

# Constraint 1: Exactly 2 photos per section
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Constraint 2: Each photographer has at least 1 but no more than 3 photos total
Total_F = L_F + M_F + S_F
Total_G = L_G + M_G + S_G
Total_H = L_H + M_H + S_H

solver.add(Total_F >= 1, Total_F <= 3)
solver.add(Total_G >= 1, Total_G <= 3)
solver.add(Total_H >= 1, Total_H <= 3)

# Constraint 3: At least one photograph in Lifestyle by a photographer who has at least one photograph in Metro
# i.e., there exists a photographer p such that (photo in L by p >= 1) AND (photo in M by p >= 1)
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 4: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(L_H == S_F)

# Constraint 5: None of Gagnon's photos can be in Sports
solver.add(S_G == 0)

# Now evaluate each option
# Option A: L: both by F, M: one by F and one by H, S: one by G and one by H
opt_a_constr = And(
    L_F == 2, L_G == 0, L_H == 0,
    M_F == 1, M_G == 0, M_H == 1,
    S_F == 0, S_G == 1, S_H == 1
)

# Option B: L: one by F and one by G, M: one by F and one by G, S: both by H
opt_b_constr = And(
    L_F == 1, L_G == 1, L_H == 0,
    M_F == 1, M_G == 1, M_H == 0,
    S_F == 0, S_G == 0, S_H == 2
)

# Option C: L: both by F, M: both by G, S: both by H
opt_c_constr = And(
    L_F == 2, L_G == 0, L_H == 0,
    M_F == 0, M_G == 2, M_H == 0,
    S_F == 0, S_G == 0, S_H == 2
)

# Option D: L: both by G, M: one by F and one by G, S: one by F and one by H
opt_d_constr = And(
    L_F == 0, L_G == 2, L_H == 0,
    M_F == 1, M_G == 1, M_H == 0,
    S_F == 1, S_G == 0, S_H == 1
)

# Option E: L: one by G and one by H, M: both by H, S: one by F and one by H
opt_e_constr = And(
    L_F == 0, L_G == 1, L_H == 1,
    M_F == 0, M_G == 0, M_H == 2,
    S_F == 1, S_G == 0, S_H == 1
)

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