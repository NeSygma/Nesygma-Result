from z3 import *

# Problem setup:
# - 3 sections: Lifestyle (L), Metro (M), Sports (S)
# - Each section has exactly 2 photographs
# - Total 6 photographs
# - Photographers: Fuentes (F), Gagnon (G), Hue (H)
# - Each photographer has between 1 and 3 photographs total

# We'll model each photograph as a variable indicating which photographer took it
# Since we have 6 photographs total, we can index them 0-5
# But we need to track which section each photograph belongs to

# Let's define:
# - L0, L1: photographs in Lifestyle section (indices 0,1)
# - M0, M1: photographs in Metro section (indices 2,3)
# - S0, S1: photographs in Sports section (indices 4,5)

# Each photograph is assigned to a photographer: 0=Fuentes, 1=Gagnon, 2=Hue
photo = [Int(f'photo_{i}') for i in range(6)]

solver = Solver()

# Domain constraints: each photo must be 0, 1, or 2 (F, G, H)
for i in range(6):
    solver.add(Or(photo[i] == 0, photo[i] == 1, photo[i] == 2))

# Section constraints: exactly 2 photos per section
# Lifestyle: photos 0,1
# Metro: photos 2,3
# Sports: photos 4,5

# Constraint: For each photographer, at least one but no more than three photos
# Count photos per photographer
f_count = Sum([If(photo[i] == 0, 1, 0) for i in range(6)])
g_count = Sum([If(photo[i] == 1, 1, 0) for i in range(6)])
h_count = Sum([If(photo[i] == 2, 1, 0) for i in range(6)])

solver.add(f_count >= 1, f_count <= 3)
solver.add(g_count >= 1, g_count <= 3)
solver.add(h_count >= 1, h_count <= 3)

# Constraint: At least one photograph in Lifestyle section must be by a photographer 
# who has at least one photograph in Metro section
# This means: There exists a photographer P such that:
#   P has at least one photo in Lifestyle AND P has at least one photo in Metro

# We'll model this by checking each photographer
# For each photographer, check if they have photos in both Lifestyle and Metro
lifestyle_has_f = Or(photo[0] == 0, photo[1] == 0)
lifestyle_has_g = Or(photo[0] == 1, photo[1] == 1)
lifestyle_has_h = Or(photo[0] == 2, photo[1] == 2)

metro_has_f = Or(photo[2] == 0, photo[3] == 0)
metro_has_g = Or(photo[2] == 1, photo[3] == 1)
metro_has_h = Or(photo[2] == 2, photo[3] == 2)

# At least one photographer has photos in both sections
solver.add(Or(
    And(lifestyle_has_f, metro_has_f),
    And(lifestyle_has_g, metro_has_g),
    And(lifestyle_has_h, metro_has_h)
))

# Constraint: The number of Hue's photographs in Lifestyle section 
# must equal the number of Fuentes photographs in Sports section
# Hue in Lifestyle: count of photo[i]==2 for i in [0,1]
h_lifestyle = Sum([If(photo[i] == 2, 1, 0) for i in range(2)])
# Fuentes in Sports: count of photo[i]==0 for i in [4,5]
f_sports = Sum([If(photo[i] == 0, 1, 0) for i in range(4, 6)])
solver.add(h_lifestyle == f_sports)

# Constraint: None of Gagnon's photographs can be in Sports section
# So photos 4 and 5 (Sports) cannot be Gagnon (1)
solver.add(photo[4] != 1)
solver.add(photo[5] != 1)

# Additional constraint from the question: 
# "If one photograph in the Lifestyle section is by Gagnon and one is by Hue"
# This means: exactly one Gagnon and one Hue in Lifestyle (photos 0,1)
# So: photo[0] and photo[1] are one Gagnon (1) and one Hue (2) in some order
solver.add(Or(
    And(photo[0] == 1, photo[1] == 2),
    And(photo[0] == 2, photo[1] == 1)
))

# Now we need to evaluate each answer choice
# Answer choices:
# (A) Exactly one photograph in the Metro section is by Fuentes.
# (B) Exactly one photograph in the Metro section is by Gagnon.
# (C) Both photographs in the Metro section are by Gagnon.
# (D) Exactly one photograph in the Sports section is by Hue.
# (E) Both photographs in the Sports section are by Hue.

# Define constraints for each option
opt_a = Sum([If(photo[i] == 0, 1, 0) for i in range(2, 4)]) == 1  # Exactly one Fuentes in Metro
opt_b = Sum([If(photo[i] == 1, 1, 0) for i in range(2, 4)]) == 1  # Exactly one Gagnon in Metro
opt_c = Sum([If(photo[i] == 1, 1, 0) for i in range(2, 4)]) == 2  # Both Gagnon in Metro
opt_d = Sum([If(photo[i] == 2, 1, 0) for i in range(4, 6)]) == 1  # Exactly one Hue in Sports
opt_e = Sum([If(photo[i] == 2, 1, 0) for i in range(4, 6)]) == 2  # Both Hue in Sports

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")