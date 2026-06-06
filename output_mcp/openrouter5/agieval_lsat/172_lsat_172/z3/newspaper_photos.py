from z3 import *

# We have 3 sections: Lifestyle (L), Metro (M), Sports (S)
# Each section has exactly 2 photographs
# 3 photographers: Fuentes (F), Gagnon (G), Hue (H)
# Total 6 photographs

# Let's model using integer variables for each section's two slots.
# We'll use 0=Fuentes, 1=Gagnon, 2=Hue

solver = Solver()

# Variables: L0, L1 for Lifestyle; M0, M1 for Metro; S0, S1 for Sports
L0, L1 = Ints('L0 L1')
M0, M1 = Ints('M0 M1')
S0, S1 = Ints('S0 S1')

all_photos = [L0, L1, M0, M1, S0, S1]

# Domain: each photo is by one of the three photographers
for p in all_photos:
    solver.add(Or(p == 0, p == 1, p == 2))  # 0=Fuentes, 1=Gagnon, 2=Hue

# Constraint 1: For each photographer, at least 1 but no more than 3 photos appear.
# Count photos per photographer
count_F = Sum([If(p == 0, 1, 0) for p in all_photos])
count_G = Sum([If(p == 1, 1, 0) for p in all_photos])
count_H = Sum([If(p == 2, 1, 0) for p in all_photos])

solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# Constraint 2: At least one photograph in Lifestyle is by a photographer who has at least one photograph in Metro.
# A photographer has at least one photo in Metro if count_Metro[photog] >= 1
count_M_F = Sum([If(p == 0, 1, 0) for p in [M0, M1]])
count_M_G = Sum([If(p == 1, 1, 0) for p in [M0, M1]])
count_M_H = Sum([If(p == 2, 1, 0) for p in [M0, M1]])

# At least one Lifestyle photo is by a photographer who has >=1 Metro photo
# L0 or L1 is by a photographer with count in Metro >= 1
solver.add(Or(
    And(Or(L0 == 0, L1 == 0), count_M_F >= 1),
    And(Or(L0 == 1, L1 == 1), count_M_G >= 1),
    And(Or(L0 == 2, L1 == 2), count_M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
count_L_H = Sum([If(p == 2, 1, 0) for p in [L0, L1]])
count_S_F = Sum([If(p == 0, 1, 0) for p in [S0, S1]])
solver.add(count_L_H == count_S_F)

# Constraint 4: None of Gagnon's photos can be in Sports
solver.add(S0 != 1)
solver.add(S1 != 1)

# Given condition: One photo in Lifestyle is by Fuentes and one is by Hue
solver.add(Or(And(L0 == 0, L1 == 2), And(L0 == 2, L1 == 0)))

# Now evaluate each option
found_options = []

# Option A: Both photographs in Metro are by Fuentes
opt_a = And(M0 == 0, M1 == 0)

# Option B: Both photographs in Metro are by Gagnon
opt_b = And(M0 == 1, M1 == 1)

# Option C: Exactly one photograph in Metro is by Hue
opt_c = Sum([If(p == 2, 1, 0) for p in [M0, M1]]) == 1

# Option D: Both photographs in Sports are by Hue
opt_d = And(S0 == 2, S1 == 2)

# Option E: Neither photograph in Sports is by Hue
opt_e = And(S0 != 2, S1 != 2)

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