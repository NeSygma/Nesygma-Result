from z3 import *

# Initialize solver
solver = Solver()

# Variables for number of photographs by each photographer in each section
# Lifestyle: L_F, L_G, L_H
# Metro: M_F, M_G, M_H
# Sports: S_F, S_G, S_H
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Constraints
# Total photographs per section
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Given condition: Both photographs in Lifestyle are by Hue
solver.add(L_H == 2)
solver.add(L_F == 0)
solver.add(L_G == 0)

# Constraint 2: At least one photograph in Lifestyle must be by a photographer who has at least one photograph in Metro
# Since L_H = 2, this implies M_H >= 1
solver.add(M_H >= 1)

# Constraint 3: Number of Hue's photographs in Lifestyle must equal number of Fuentes' photographs in Sports
solver.add(L_H == S_F)

# Constraint 4: None of Gagnon's photographs can be in the Sports section
solver.add(S_G == 0)

# Total photographs per photographer (at least 1, at most 3)
solver.add(L_F + M_F + S_F >= 1)
solver.add(L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1)
solver.add(L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1)
solver.add(L_H + M_H + S_H <= 3)

# Evaluate answer choices
found_options = []

# (A) Exactly one is by Fuentes
solver.push()
solver.add(L_F + M_F + S_F == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# (B) Exactly three are by Fuentes
solver.push()
solver.add(L_F + M_F + S_F == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# (C) Exactly one is by Gagnon
solver.push()
solver.add(L_G + M_G + S_G == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# (D) Exactly two are by Gagnon
solver.push()
solver.add(L_G + M_G + S_G == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# (E) Exactly two are by Hue
solver.push()
solver.add(L_H + M_H + S_H == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")