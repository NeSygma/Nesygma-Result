from z3 import *

solver = Solver()

# Photographers: 0=Fuentes(F), 1=Gagnon(G), 2=Hue(H)
F, G, H = 0, 1, 2

# Variables: each section has 2 photographs, each assigned a photographer
L1, L2 = Ints('L1 L2')  # Lifestyle
M1, M2 = Ints('M1 M2')  # Metro
S1, S2 = Ints('S1 S2')  # Sports

all_vars = [L1, L2, M1, M2, S1, S2]

# Domain: each photograph is by F(0), G(1), or H(2)
for v in all_vars:
    solver.add(Or(v == F, v == G, v == H))

# Constraint 1: For each photographer, at least 1 but no more than 3 photographs total
for photographer in [F, G, H]:
    count = Sum([If(v == photographer, 1, 0) for v in all_vars])
    solver.add(count >= 1)
    solver.add(count <= 3)

# Constraint 2: At least one photograph in Lifestyle must be by a photographer 
# who has at least one photograph in Metro.
# This means: there exists a photographer P such that P has a photo in Lifestyle AND P has a photo in Metro.
# We need: exists P in {F,G,H}: (L1==P or L2==P) and (M1==P or M2==P)
solver.add(Or(
    And(Or(L1 == F, L2 == F), Or(M1 == F, M2 == F)),
    And(Or(L1 == G, L2 == G), Or(M1 == G, M2 == G)),
    And(Or(L1 == H, L2 == H), Or(M1 == H, M2 == H))
))

# Constraint 3: Number of Hue's photos in Lifestyle == Number of Fuentes' photos in Sports
hue_lifestyle = Sum([If(v == H, 1, 0) for v in [L1, L2]])
fuentes_sports = Sum([If(v == F, 1, 0) for v in [S1, S2]])
solver.add(hue_lifestyle == fuentes_sports)

# Constraint 4: None of Gagnon's photographs can be in Sports section
solver.add(S1 != G)
solver.add(S2 != G)

# Additional given: One photograph in Metro is by Fuentes and one is by Hue
solver.add(Or(M1 == F, M2 == F))
solver.add(Or(M1 == H, M2 == H))
# Exactly one F and one H in Metro (since there are only 2 spots)
# Could be (F,H) or (H,F) - but we also need to ensure not both are F or both are H
# Actually "one is by Fuentes and one is by Hue" means exactly one of each
solver.add(Sum([If(M1 == F, 1, 0), If(M2 == F, 1, 0)]) == 1)
solver.add(Sum([If(M1 == H, 1, 0), If(M2 == H, 1, 0)]) == 1)

# Now evaluate each option
# (A) Both photographs in Lifestyle are by Fuentes
opt_a = And(L1 == F, L2 == F)

# (B) Both photographs in Lifestyle are by Gagnon
opt_b = And(L1 == G, L2 == G)

# (C) One photograph in Lifestyle is by Gagnon and one is by Hue
opt_c = Or(And(L1 == G, L2 == H), And(L1 == H, L2 == G))

# (D) Both photographs in Lifestyle are by Hue
opt_d = And(L1 == H, L2 == H)

# (E) Both photographs in Sports are by Fuentes
opt_e = And(S1 == F, S2 == F)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: L=({m[L1]},{m[L2]}), M=({m[M1]},{m[M2]}), S=({m[S1]},{m[S2]})")
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