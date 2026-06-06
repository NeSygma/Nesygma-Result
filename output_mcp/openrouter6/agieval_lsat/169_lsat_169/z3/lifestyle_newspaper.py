from z3 import *

solver = Solver()

# Variables for counts per section per photographer
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# 1. Each section has exactly two photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# 2. Each photographer appears 1 to 3 times total
Total_F = L_F + M_F + S_F
Total_G = L_G + M_G + S_G
Total_H = L_H + M_H + S_H
solver.add(Total_F >= 1, Total_F <= 3)
solver.add(Total_G >= 1, Total_G <= 3)
solver.add(Total_H >= 1, Total_H <= 3)

# 3. At least one Lifestyle photo by a photographer who also has at least one Metro photo
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# 4. Hue's Lifestyle photos equals Fuentes Sports photos
solver.add(L_H == S_F)

# 5. Gagnon not in Sports
solver.add(S_G == 0)

# Conditional: both Lifestyle photos are by Hue
solver.add(L_H == 2)
solver.add(L_F == 0)
solver.add(L_G == 0)

# Answer choices
opt_a = (Total_F == 1)
opt_b = (Total_F == 3)
opt_c = (Total_G == 1)
opt_d = (Total_G == 2)
opt_e = (Total_H == 2)

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