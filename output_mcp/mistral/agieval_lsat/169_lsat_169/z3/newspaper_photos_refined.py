from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for each photograph's photographer
# 0 = Fuentes, 1 = Gagnon, 2 = Hue
# Photos: 0,1 = Lifestyle; 2,3 = Metro; 4,5 = Sports
photos = [Int(f'photo_{i}') for i in range(6)]

# Base constraints
solver = Solver()

# Each photo is assigned to exactly one photographer
for p in photos:
    solver.add(Or(p == 0, p == 1, p == 2))

# Exactly two photos per section (implicit in indexing)

# Constraint: For each photographer, at least one but no more than three photographs must appear
fuentes_count = Sum([If(photo == 0, 1, 0) for photo in photos])
gagnon_count = Sum([If(photo == 1, 1, 0) for photo in photos])
hue_count = Sum([If(photo == 2, 1, 0) for photo in photos])

solver.add(fuentes_count >= 1, fuentes_count <= 3)
solver.add(gagnon_count >= 1, gagnon_count <= 3)
solver.add(hue_count >= 1, hue_count <= 3)

# Constraint: At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section
# Lifestyle photos: photos[0], photos[1]
# Metro photos: photos[2], photos[3]
# A photographer has at least one Metro photo if either photo[2] or photo[3] equals that photographer
metro_photographers = Or(photos[2] == 0, photos[3] == 0, 
                         photos[2] == 1, photos[3] == 1, 
                         photos[2] == 2, photos[3] == 2)
# At least one Lifestyle photo must be by a photographer who has at least one Metro photo
lifestyle_constraint = Or(
    And(photos[0] == 0, metro_photographers),
    And(photos[0] == 1, metro_photographers),
    And(photos[0] == 2, metro_photographers),
    And(photos[1] == 0, metro_photographers),
    And(photos[1] == 1, metro_photographers),
    And(photos[1] == 2, metro_photographers)
)
solver.add(lifestyle_constraint)

# Constraint: The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes' photographs in the Sports section
# Lifestyle Hue count
hue_lifestyle_count = Sum([If(And(i < 2, photos[i] == 2), 1, 0) for i in range(6)])
# Sports Fuentes count
fuentes_sports_count = Sum([If(And(i >= 4, photos[i] == 0), 1, 0) for i in range(6)])
solver.add(hue_lifestyle_count == fuentes_sports_count)

# Constraint: None of Gagnon's photographs can be in the Sports section
# Sports photos: photos[4], photos[5]
solver.add(photos[4] != 1)
solver.add(photos[5] != 1)

# Condition for the question: Both photographs in the Lifestyle section are by Hue
solver.push()
solver.add(photos[0] == 2)
solver.add(photos[1] == 2)

# Hue must have at least one Metro photo (to satisfy the lifestyle constraint)
solver.add(Or(photos[2] == 2, photos[3] == 2))

# Fuentes must have exactly 2 photos in Sports (since hue_lifestyle_count = 2)
solver.add(fuentes_sports_count == 2)

# Sports section has 2 photos, so both must be by Fuentes
solver.add(photos[4] == 0)
solver.add(photos[5] == 0)

# Hue must have exactly 3 photos (2 in Lifestyle + 1 in Metro)
solver.add(hue_count == 3)

# Fuentes must have exactly 2 photos (both in Sports)
solver.add(fuentes_count == 2)

# Gagnon must have exactly 1 photo (in Metro, since Sports is fully Fuentes and Lifestyle is fully Hue)
solver.add(gagnon_count == 1)

# Now evaluate the multiple choice options under this condition
found_options = []

# Option A: Exactly one is by Fuentes
solver.push()
solver.add(fuentes_count == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Exactly three are by Fuentes
solver.push()
solver.add(fuentes_count == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Exactly one is by Gagnon
solver.push()
solver.add(gagnon_count == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Exactly two are by Gagnon
solver.push()
solver.add(gagnon_count == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Exactly two are by Hue
solver.push()
solver.add(hue_count == 2)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

solver.pop()  # Pop the condition

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")