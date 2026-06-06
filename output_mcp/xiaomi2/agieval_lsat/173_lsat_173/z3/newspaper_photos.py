from z3 import *

solver = Solver()

# Photographers: F=0, G=1, H=2
F, G, H = 0, 1, 2

# Variables: photographer for each photo slot
# L1, L2 = Lifestyle; M1, M2 = Metro; S1, S2 = Sports
L1, L2 = Ints('L1 L2')
M1, M2 = Ints('M1 M2')
S1, S2 = Ints('S1 S2')

all_vars = [L1, L2, M1, M2, S1, S2]

# Domain: each photo is by F(0), G(1), or H(2)
for v in all_vars:
    solver.add(Or(v == F, v == G, v == H))

# Constraint 1: For each photographer, at least 1 but no more than 3 photos total
for photographer in [F, G, H]:
    count = Sum([If(v == photographer, 1, 0) for v in all_vars])
    solver.add(count >= 1)
    solver.add(count <= 3)

# Constraint 2: At least one Lifestyle photo is by a photographer who has at least one Metro photo
# For each photographer p: if p has a Lifestyle photo, then p must also have a Metro photo
# Equivalently: there exists a photographer p such that p is in Lifestyle AND p is in Metro
solver.add(Or(
    And(Or(L1 == F, L2 == F), Or(M1 == F, M2 == F)),
    And(Or(L1 == G, L2 == G), Or(M1 == G, M2 == G)),
    And(Or(L1 == H, L2 == H), Or(M1 == H, M2 == H))
))

# Constraint 3: Number of Hue photos in Lifestyle == Number of Fuentes photos in Sports
hue_lifestyle = Sum([If(v == H, 1, 0) for v in [L1, L2]])
fuentes_sports = Sum([If(v == F, 1, 0) for v in [S1, S2]])
solver.add(hue_lifestyle == fuentes_sports)

# Constraint 4: No Gagnon photos in Sports
solver.add(S1 != G)
solver.add(S2 != G)

# Additional premise: Both photos in ONE section are by Gagnon
# At least one section has both photos by Gagnon
solver.add(Or(
    And(L1 == G, L2 == G),  # Lifestyle both Gagnon
    And(M1 == G, M2 == G),  # Metro both Gagnon
    # Sports can't both be Gagnon (constraint 4), but we include it for completeness
    And(S1 == G, S2 == G)
))

# Now test each answer choice
# (A) Both photos in Lifestyle are by Hue
opt_a = And(L1 == H, L2 == H)

# (B) One Lifestyle photo by Fuentes and one by Hue
opt_b = Or(
    And(L1 == F, L2 == H),
    And(L1 == H, L2 == F)
)

# (C) Both Metro photos are by Fuentes
opt_c = And(M1 == F, M2 == F)

# (D) One Metro photo by Gagnon and one by Hue
opt_d = Or(
    And(M1 == G, M2 == H),
    And(M1 == H, M2 == G)
)

# (E) Both Sports photos are by Hue
opt_e = And(S1 == H, S2 == H)

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