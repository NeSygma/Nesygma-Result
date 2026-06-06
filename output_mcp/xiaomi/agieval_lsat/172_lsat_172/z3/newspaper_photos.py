from z3 import *

solver = Solver()

# Sections: 0=Lifestyle, 1=Metro, 2=Sports
# Photographers: 0=Fuentes, 1=Gagnon, 2=Hue
# photos[section][photographer] = count of that photographer's photos in that section

photos = [[Int(f"photos_{s}_{p}") for p in range(3)] for s in range(3)]

# Each count is non-negative
for s in range(3):
    for p in range(3):
        solver.add(photos[s][p] >= 0)

# Exactly 2 photographs per section
for s in range(3):
    solver.add(Sum([photos[s][p] for p in range(3)]) == 2)

# For each photographer, at least 1 but no more than 3 total
for p in range(3):
    total = Sum([photos[s][p] for s in range(3)])
    solver.add(total >= 1)
    solver.add(total <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
# This means: there exists a photographer p such that photos[0][p] >= 1 AND photos[1][p] >= 1
solver.add(Or([And(photos[0][p] >= 1, photos[1][p] >= 1) for p in range(3)]))

# Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
# Hue=2, Fuentes=0
solver.add(photos[0][2] == photos[2][0])

# None of Gagnon's photos can be in Sports
# Gagnon=1
solver.add(photos[2][1] == 0)

# Given condition: one photograph in Lifestyle is by Fuentes and one is by Hue
solver.add(photos[0][0] == 1)  # Fuentes in Lifestyle = 1
solver.add(photos[0][2] == 1)  # Hue in Lifestyle = 1
# This implies photos[0][1] = 0 (Gagnon in Lifestyle)
solver.add(photos[0][1] == 0)

# From Hue in Lifestyle = 1 and the constraint photos[0][2] == photos[2][0]:
# photos[2][0] = 1 (Fuentes in Sports = 1)
# Sports has 2 photos, Gagnon=0 in Sports, Fuentes=1, so Hue=1 in Sports
# solver.add(photos[2][0] == 1)  -- derived
# solver.add(photos[2][2] == 1)  -- derived

# Now evaluate each option
found_options = []

# (A) Both photographs in the Metro section are by Fuentes.
opt_a = And(photos[1][0] == 2, photos[1][1] == 0, photos[1][2] == 0)

# (B) Both photographs in the Metro section are by Gagnon.
opt_b = And(photos[1][0] == 0, photos[1][1] == 2, photos[1][2] == 0)

# (C) Exactly one photograph in the Metro section is by Hue.
opt_c = (photos[1][2] == 1)

# (D) Both photographs in the Sports section are by Hue.
opt_d = And(photos[2][0] == 0, photos[2][2] == 2)

# (E) Neither photograph in the Sports section is by Hue.
opt_e = (photos[2][2] == 0)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for s in range(3):
            for p in range(3):
                print(f"  photos[{s}][{p}] = {m[photos[s][p]]}")
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