from z3 import *

solver = Solver()

# Photographers: 0 = Fuentes, 1 = Gagnon, 2 = Hue
F, G, H = 0, 1, 2

# Section photos: Lifestyle (L1, L2), Metro (M1, M2), Sports (S1, S2)
L1, L2 = Ints('L1 L2')
M1, M2 = Ints('M1 M2')
S1, S2 = Ints('S1 S2')

all_photos = [L1, L2, M1, M2, S1, S2]

# Each photo is by one of the three photographers (0, 1, 2)
for p in all_photos:
    solver.add(Or(p == F, p == G, p == H))

# GIVEN CONDITION: Both Lifestyle photos are by Hue
solver.add(L1 == H)
solver.add(L2 == H)

# Constraint 1: For each photographer, at least 1 but no more than 3 photos total
total_F = Sum([If(p == F, 1, 0) for p in all_photos])
total_G = Sum([If(p == G, 1, 0) for p in all_photos])
total_H = Sum([If(p == H, 1, 0) for p in all_photos])

solver.add(total_F >= 1, total_F <= 3)
solver.add(total_G >= 1, total_G <= 3)
solver.add(total_H >= 1, total_H <= 3)

# Constraint 2: At least one Lifestyle photo is by a photographer who has at least one Metro photo
# Since both Lifestyle photos are by Hue, Hue must have at least one Metro photo
solver.add(Or(M1 == H, M2 == H))

# Constraint 3: Number of Hue's photos in Lifestyle == Number of Fuentes' photos in Sports
hue_in_L = Sum([If(p == H, 1, 0) for p in [L1, L2]])
fuentes_in_S = Sum([If(p == F, 1, 0) for p in [S1, S2]])
solver.add(hue_in_L == fuentes_in_S)

# Constraint 4: None of Gagnon's photos can be in Sports
solver.add(S1 != G)
solver.add(S2 != G)

# Now test each answer choice
# (A) Exactly one is by Fuentes
# (B) Exactly three are by Fuentes
# (C) Exactly one is by Gagnon
# (D) Exactly two are by Gagnon
# (E) Exactly two are by Hue

opt_a = (total_F == 1)
opt_b = (total_F == 3)
opt_c = (total_G == 1)
opt_d = (total_G == 2)
opt_e = (total_H == 2)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        tf = m.eval(total_F)
        tg = m.eval(total_G)
        th = m.eval(total_H)
        print(f"Option {letter} is SAT: L=({m[L1]},{m[L2]}), M=({m[M1]},{m[M2]}), S=({m[S1]},{m[S2]})")
        print(f"  Total F={tf}, G={tg}, H={th}")
    else:
        print(f"Option {letter} is UNSAT (must be true)")
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