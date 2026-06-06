from z3 import *

solver = Solver()

# Three sections: Lifestyle (L), Metro (M), Sports (S)
# Each section has exactly 2 photographs
# Three photographers: Fuentes (F=0), Gagnon (G=1), Hue (H=2)

L0, L1 = Ints('L0 L1')
M0, M1 = Ints('M0 M1')
S0, S1 = Ints('S0 S1')

all_slots = [L0, L1, M0, M1, S0, S1]

for slot in all_slots:
    solver.add(slot >= 0, slot <= 2)

# Count per photographer
count_F = Sum([If(slot == 0, 1, 0) for slot in all_slots])
count_G = Sum([If(slot == 1, 1, 0) for slot in all_slots])
count_H = Sum([If(slot == 2, 1, 0) for slot in all_slots])

solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# At least one photographer has photos in both Lifestyle and Metro
has_L = [Bool(f'has_L_{p}') for p in range(3)]
has_M = [Bool(f'has_M_{p}') for p in range(3)]

for p in range(3):
    solver.add(has_L[p] == Or(L0 == p, L1 == p))
    solver.add(has_M[p] == Or(M0 == p, M1 == p))

solver.add(Or([And(has_L[p], has_M[p]) for p in range(3)]))

# Hue's photos in Lifestyle = Fuentes' photos in Sports
count_H_L = Sum([If(slot == 2, 1, 0) for slot in [L0, L1]])
count_F_S = Sum([If(slot == 0, 1, 0) for slot in [S0, S1]])
solver.add(count_H_L == count_F_S)

# No Gagnon in Sports
solver.add(S0 != 1)
solver.add(S1 != 1)

# Given: One Lifestyle photo is Gagnon (1), one is Hue (2)
solver.add(Or(And(L0 == 1, L1 == 2), And(L0 == 2, L1 == 1)))

# Now evaluate each option using push/pop
found_options = []

# Option A: Exactly one Metro by Fuentes
opt_a = Sum([If(M0 == 0, 1, 0), If(M1 == 0, 1, 0)]) == 1

# Option B: Exactly one Metro by Gagnon
opt_b = Sum([If(M0 == 1, 1, 0), If(M1 == 1, 1, 0)]) == 1

# Option C: Both Metro by Gagnon
opt_c = And(M0 == 1, M1 == 1)

# Option D: Exactly one Sports by Hue
opt_d = Sum([If(S0 == 2, 1, 0), If(S1 == 2, 1, 0)]) == 1

# Option E: Both Sports by Hue
opt_e = And(S0 == 2, S1 == 2)

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