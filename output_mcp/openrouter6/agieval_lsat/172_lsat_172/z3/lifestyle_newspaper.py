from z3 import *

solver = Solver()

# Variables for counts per section per photographer
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Section constraints: exactly two photos per section
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Photographer total constraints: at least one, at most three
solver.add(1 <= L_F + M_F + S_F, L_F + M_F + S_F <= 3)
solver.add(1 <= L_G + M_G + S_G, L_G + M_G + S_G <= 3)
solver.add(1 <= L_H + M_H + S_H, L_H + M_H + S_H <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Hue's Lifestyle equals Fuentes's Sports
solver.add(L_H == S_F)

# No Gagnon in Sports
solver.add(S_G == 0)

# Given condition: one photograph in Lifestyle is by Fuentes and one by Hue
solver.add(L_F == 1)
solver.add(L_H == 1)
solver.add(L_G == 0)  # follows from L_F + L_H = 2

# Option constraints
opt_a = And(M_F == 2, M_G == 0, M_H == 0)
opt_b = And(M_G == 2, M_F == 0, M_H == 0)
opt_c = And(M_H == 1, M_F + M_G == 1)  # exactly one Hue in Metro
opt_d = And(S_H == 2, S_F == 0, S_G == 0)
opt_e = S_H == 0

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