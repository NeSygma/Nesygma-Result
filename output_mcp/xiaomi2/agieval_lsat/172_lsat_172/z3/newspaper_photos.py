from z3 import *

solver = Solver()

# Photographers: Fuentes=0, Gagnon=1, Hue=2
F, G, H = 0, 1, 2

# Each section has 2 photographs, each assigned to a photographer
L1, L2 = Ints('L1 L2')
M1, M2 = Ints('M1 M2')
S1, S2 = Ints('S1 S2')

all_photos = [L1, L2, M1, M2, S1, S2]

# Domain: each photo is by F(0), G(1), or H(2)
for p in all_photos:
    solver.add(Or(p == F, p == G, p == H))

# Additional condition: one Lifestyle photo is Fuentes, one is Hue
solver.add(Or(And(L1 == F, L2 == H), And(L1 == H, L2 == F)))

# Constraint 1: For each photographer, at least 1 but no more than 3
for photographer in [F, G, H]:
    count = Sum([If(p == photographer, 1, 0) for p in all_photos])
    solver.add(count >= 1)
    solver.add(count <= 3)

# Constraint 2: At least one photograph in Lifestyle must be by a photographer
# who has at least one photograph in Metro.
# Lifestyle photographers: L1, L2
# For each lifestyle photographer, check if they also appear in Metro
# L1 appears in Metro: M1 == L1 or M2 == L1
# L2 appears in Metro: M1 == L2 or M2 == L2
solver.add(Or(
    Or(M1 == L1, M2 == L1),
    Or(M1 == L2, M2 == L2)
))

# Constraint 3: Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_lifestyle = Sum([If(p == H, 1, 0) for p in [L1, L2]])
fuentes_sports = Sum([If(p == F, 1, 0) for p in [S1, S2]])
solver.add(hue_lifestyle == fuentes_sports)

# Constraint 4: None of Gagnon's photographs can be in Sports section
solver.add(S1 != G)
solver.add(S2 != G)

# Now test each option
found_options = []

# (A) Both photographs in Metro are by Fuentes
opt_a = And(M1 == F, M2 == F)

# (B) Both photographs in Metro are by Gagnon
opt_b = And(M1 == G, M2 == G)

# (C) Exactly one photograph in Metro is by Hue
opt_c = Or(And(M1 == H, M2 != H), And(M1 != H, M2 == H))

# (D) Both photographs in Sports are by Hue
opt_d = And(S1 == H, S2 == H)

# (E) Neither photograph in Sports is by Hue
opt_e = And(S1 != H, S2 != H)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        m = solver.model()
        print(f"Option {letter} is SAT: L=({m[L1]},{m[L2]}), M=({m[M1]},{m[M2]}), S=({m[S1]},{m[S2]})")
        found_options.append(letter)
    else:
        print(f"Option {letter} is UNSAT")
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