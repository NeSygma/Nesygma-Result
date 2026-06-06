from z3 import *

solver = Solver()

# Sections: 0=Lifestyle, 1=Metro, 2=Sports
# Photographers: 0=Fuentes, 1=Gagnon, 2=Hue
# 6 photographs total, 2 per section
# photo[section][0] and photo[section][1] = photographer index

photo = [[Int(f"photo_{s}_{p}") for p in range(2)] for s in range(3)]

# Each photo is by photographer 0, 1, or 2
for s in range(3):
    for p in range(2):
        solver.add(Or(photo[s][p] == 0, photo[s][p] == 1, photo[s][p] == 2))

# Count photos per photographer
fuentes_count = Sum([If(photo[s][p] == 0, 1, 0) for s in range(3) for p in range(2)])
gagnon_count = Sum([If(photo[s][p] == 1, 1, 0) for s in range(3) for p in range(2)])
hue_count = Sum([If(photo[s][p] == 2, 1, 0) for s in range(3) for p in range(2)])

# For each photographer, at least 1 but no more than 3
solver.add(fuentes_count >= 1, fuentes_count <= 3)
solver.add(gagnon_count >= 1, gagnon_count <= 3)
solver.add(hue_count >= 1, hue_count <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
# For each photographer, check if they have a photo in Lifestyle AND in Metro
for photographer in range(3):
    has_in_lifestyle = Or(photo[0][0] == photographer, photo[0][1] == photographer)
    has_in_metro = Or(photo[1][0] == photographer, photo[1][1] == photographer)
    # If photographer has in lifestyle, they must also have in metro (for at least one such photographer)
    # We need: exists photographer such that has_in_lifestyle AND has_in_metro
    # This is an OR over all photographers
    pass

# Better encoding: at least one photographer has photos in both Lifestyle and Metro
solver.add(Or([
    And(Or(photo[0][0] == ph, photo[0][1] == ph), Or(photo[1][0] == ph, photo[1][1] == ph))
    for ph in range(3)
]))

# Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_in_lifestyle = Sum([If(photo[0][p] == 2, 1, 0) for p in range(2)])
fuentes_in_sports = Sum([If(photo[2][p] == 0, 1, 0) for p in range(2)])
solver.add(hue_in_lifestyle == fuentes_in_sports)

# None of Gagnon's photographs can be in the Sports section
solver.add(photo[2][0] != 1)
solver.add(photo[2][1] != 1)

# GIVEN CONDITION: Both photographs in Lifestyle are by Hue
solver.add(photo[0][0] == 2)
solver.add(photo[0][1] == 2)

# Now check each answer choice
# (A) Exactly one is by Fuentes.
# (B) Exactly three are by Fuentes.
# (C) Exactly one is by Gagnon.
# (D) Exactly two are by Gagnon.
# (E) Exactly two are by Hue.

opt_a = (fuentes_count == 1)
opt_b = (fuentes_count == 3)
opt_c = (gagnon_count == 1)
opt_d = (gagnon_count == 2)
opt_e = (hue_count == 2)

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

# Also print the model for debugging
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample model:")
    for s in range(3):
        section_name = ["Lifestyle", "Metro", "Sports"][s]
        for p in range(2):
            ph = m[photo[s][p]]
            ph_name = ["Fuentes", "Gagnon", "Hue"][ph.as_long()]
            print(f"  {section_name} photo {p+1}: {ph_name}")
    print(f"  Fuentes total: {m.evaluate(fuentes_count)}")
    print(f"  Gagnon total: {m.evaluate(gagnon_count)}")
    print(f"  Hue total: {m.evaluate(hue_count)}")
solver.pop()