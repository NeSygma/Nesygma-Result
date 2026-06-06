from z3 import *

solver = Solver()

# Variables: counts for each photographer in each section
# L_F, L_G, L_H = counts in Lifestyle
# M_F, M_G, M_H = counts in Metro
# S_F, S_G, S_H = counts in Sports
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Domain: each count is non-negative integer, at most 2
for v in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
    solver.add(v >= 0)
    solver.add(v <= 2)

# Each section has exactly 2 photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Total photos per photographer between 1 and 3
solver.add(L_F + M_F + S_F >= 1)
solver.add(L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1)
solver.add(L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1)
solver.add(L_H + M_H + S_H <= 3)

# Constraint 2: At least one photographer has a photo in both Lifestyle and Metro
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(L_H == S_F)

# Constraint 4: None of Gagnon's photos can be in Sports
solver.add(S_G == 0)

# Now test each answer choice
found_options = []

# Option A: L_F=1, M_F=1, S_F=1
solver.push()
solver.add(L_F == 1)
solver.add(M_F == 1)
solver.add(S_F == 1)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: L_F=1, M_F=0, S_F=2
solver.push()
solver.add(L_F == 1)
solver.add(M_F == 0)
solver.add(S_F == 2)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: L_F=2, M_F=0, S_F=1
solver.push()
solver.add(L_F == 2)
solver.add(M_F == 0)
solver.add(S_F == 1)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: L_F=0, M_F=1, S_F=2
solver.push()
solver.add(L_F == 0)
solver.add(M_F == 1)
solver.add(S_F == 2)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: L_F=0, M_F=2, S_F=1
solver.push()
solver.add(L_F == 0)
solver.add(M_F == 2)
solver.add(S_F == 1)
if solver.check() == sat:
    found_options.append('E')
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