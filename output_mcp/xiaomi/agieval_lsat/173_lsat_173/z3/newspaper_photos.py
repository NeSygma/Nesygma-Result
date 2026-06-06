from z3 import *

solver = Solver()

# Sections: 0=Lifestyle, 1=Metro, 2=Sports
# Photographers: 0=Fuentes, 1=Gagnon, 2=Hue
# photos[section][slot] = photographer (0, 1, or 2)

photos = [[Int(f"photo_{s}_{i}") for i in range(2)] for s in range(3)]

# Each photo is by one of the three photographers
for s in range(3):
    for i in range(2):
        solver.add(Or(photos[s][i] == 0, photos[s][i] == 1, photos[s][i] == 2))

# For each photographer, at least 1 but no more than 3 of their photos must appear
for p in range(3):
    count_p = Sum([If(photos[s][i] == p, 1, 0) for s in range(3) for i in range(2)])
    solver.add(count_p >= 1)
    solver.add(count_p <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one photo in Metro
# For each Lifestyle photo, check if that photographer also has a photo in Metro
for i in range(2):
    # photographer photos[0][i] has at least one photo in Metro
    solver.add(Or(
        And(photos[0][i] == 0, Or(photos[1][0] == 0, photos[1][1] == 0)),
        And(photos[0][i] == 1, Or(photos[1][0] == 1, photos[1][1] == 1)),
        And(photos[0][i] == 2, Or(photos[1][0] == 2, photos[1][1] == 2))
    ))

# Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_lifestyle = Sum([If(photos[0][i] == 2, 1, 0) for i in range(2)])
fuentes_sports = Sum([If(photos[2][i] == 0, 1, 0) for i in range(2)])
solver.add(hue_lifestyle == fuentes_sports)

# None of Gagnon's photos can be in Sports
for i in range(2):
    solver.add(photos[2][i] != 1)

# Additional condition: both photographs in one of the three sections are by Gagnon
# This means at least one section has both photos by Gagnon
solver.add(Or(
    And(photos[0][0] == 1, photos[0][1] == 1),  # Lifestyle both Gagnon
    And(photos[1][0] == 1, photos[1][1] == 1),  # Metro both Gagnon
    And(photos[2][0] == 1, photos[2][1] == 1)   # Sports both Gagnon (but Gagnon can't be in Sports, so this is impossible)
))

# Now evaluate each answer choice
# (A) Both photographs in the Lifestyle section are by Hue
opt_a = And(photos[0][0] == 2, photos[0][1] == 2)

# (B) One photograph in the Lifestyle section is by Fuentes and one is by Hue
opt_b = Or(
    And(photos[0][0] == 0, photos[0][1] == 2),
    And(photos[0][0] == 2, photos[0][1] == 0)
)

# (C) Both photographs in the Metro section are by Fuentes
opt_c = And(photos[1][0] == 0, photos[1][1] == 0)

# (D) One photograph in the Metro section is by Gagnon and one is by Hue
opt_d = Or(
    And(photos[1][0] == 1, photos[1][1] == 2),
    And(photos[1][0] == 2, photos[1][1] == 1)
)

# (E) Both photographs in the Sports section are by Hue
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