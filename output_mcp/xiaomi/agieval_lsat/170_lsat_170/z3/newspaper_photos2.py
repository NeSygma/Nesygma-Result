from z3 import *

solver = Solver()

# Sections: Lifestyle(0), Metro(1), Sports(2)
# Photographers: Fuentes(0), Gagnon(1), Hue(2)
# 6 photographs total, 2 per section
# photos[section][slot] = photographer (0, 1, 2)

photos = [[Int(f"photo_{s}_{i}") for i in range(2)] for s in range(3)]

# Each photo is by one of the three photographers
for s in range(3):
    for i in range(2):
        solver.add(Or(photos[s][i] == 0, photos[s][i] == 1, photos[s][i] == 2))

# For each photographer, at least 1 but no more than 3 photographs must appear
for p in range(3):
    count = Sum([If(photos[s][i] == p, 1, 0) for s in range(3) for i in range(2)])
    solver.add(count >= 1)
    solver.add(count <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
# This means: there exists a photographer p such that p appears in Lifestyle AND p appears in Metro
solver.add(Or([
    And(
        Or(photos[0][0] == p, photos[0][1] == p),  # p in Lifestyle
        Or(photos[1][0] == p, photos[1][1] == p)   # p in Metro
    )
    for p in range(3)
]))

# Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_lifestyle = Sum([If(photos[0][i] == 2, 1, 0) for i in range(2)])
fuentes_sports = Sum([If(photos[2][i] == 0, 1, 0) for i in range(2)])
solver.add(hue_lifestyle == fuentes_sports)

# None of Gagnon's photographs can be in Sports
for i in range(2):
    solver.add(photos[2][i] != 1)

# Additional condition: one photo in Lifestyle is by Gagnon and one is by Hue
# This means exactly one Gagnon and exactly one Hue in Lifestyle (2 slots total)
gagnon_lifestyle = Sum([If(photos[0][i] == 1, 1, 0) for i in range(2)])
hue_lifestyle_count = Sum([If(photos[0][i] == 2, 1, 0) for i in range(2)])
solver.add(gagnon_lifestyle == 1)
solver.add(hue_lifestyle_count == 1)

# Now evaluate each answer choice
# (A) Exactly one photograph in the Metro section is by Fuentes.
opt_a = Sum([If(photos[1][i] == 0, 1, 0) for i in range(2)]) == 1

# (B) Exactly one photograph in the Metro section is by Gagnon.
opt_b = Sum([If(photos[1][i] == 1, 1, 0) for i in range(2)]) == 1

# (C) Both photographs in the Metro section are by Gagnon.
opt_c = And(photos[1][0] == 1, photos[1][1] == 1)

# (D) Exactly one photograph in the Sports section is by Hue.
opt_d = Sum([If(photos[2][i] == 2, 1, 0) for i in range(2)]) == 1

# (E) Both photographs in the Sports section are by Hue.
opt_e = And(photos[2][0] == 2, photos[2][1] == 2)

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