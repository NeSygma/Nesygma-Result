from z3 import *

# Variables: Number of photos by each photographer in each section
# L: Lifestyle, M: Metro, S: Sports
# F: Fuentes, G: Gagnon, H: Hue
L_F, L_G, L_H = Int('L_F'), Int('L_G'), Int('L_H')
M_F, M_G, M_H = Int('M_F'), Int('M_G'), Int('M_H')
S_F, S_G, S_H = Int('S_F'), Int('S_G'), Int('S_H')

solver = Solver()

# Total photos per section is 2
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Non-negative counts
for v in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
    solver.add(v >= 0)

# Total photos per photographer (1 to 3)
F_total = L_F + M_F + S_F
G_total = L_G + M_G + S_G
H_total = L_H + M_H + S_H
for v in [F_total, G_total, H_total]:
    solver.add(v >= 1, v <= 3)

# Constraint 2: At least one photo in L must be by a photographer who has at least one photo in M
has_M_F = (M_F > 0)
has_M_G = (M_G > 0)
has_M_H = (M_H > 0)
solver.add(Or(
    And(L_F > 0, has_M_F),
    And(L_G > 0, has_M_G),
    And(L_H > 0, has_M_H)
))

# Constraint 3: L_H == S_F
solver.add(L_H == S_F)

# Constraint 4: S_G == 0
solver.add(S_G == 0)

# Question condition: L_F == 1 and L_H == 1 (implies L_G = 0)
solver.add(L_F == 1, L_H == 1, L_G == 0)

# Answer Choices
# (A) Both photographs in the Metro section are by Fuentes (M_F == 2)
# (B) Both photographs in the Metro section are by Gagnon (M_G == 2)
# (C) Exactly one photograph in the Metro section is by Hue (M_H == 1)
# (D) Both photographs in the Sports section are by Hue (S_H == 2)
# (E) Neither photograph in the Sports section is by Hue (S_H == 0)

options = [
    ("A", M_F == 2),
    ("B", M_G == 2),
    ("C", M_H == 1),
    ("D", S_H == 2),
    ("E", S_H == 0)
]

found_options = []
for letter, constr in options:
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