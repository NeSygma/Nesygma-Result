from z3 import *

# Create solver
solver = Solver()

# Define sections and photographers
sections = ['Lifestyle', 'Metro', 'Sports']
photographers = ['Fuentes', 'Gagnon', 'Hue']

# Create variables: photo_count[section][photographer] = number of photos
photo_count = {}
for section in sections:
    for photographer in photographers:
        photo_count[(section, photographer)] = Int(f"count_{section}_{photographer}")

# Base constraints

# 1. Total of 6 photos, 2 per section
for section in sections:
    solver.add(Sum([photo_count[(section, p)] for p in photographers]) == 2)

# 2. Each photographer has between 1 and 3 photos total
for photographer in photographers:
    total_photos = Sum([photo_count[(section, photographer)] for section in sections])
    solver.add(total_photos >= 1)
    solver.add(total_photos <= 3)

# 3. At least one Lifestyle photo is by a photographer who also has at least one Metro photo
lifestyle_metro_constraint = Or([
    And(photo_count[('Lifestyle', p)] >= 1, photo_count[('Metro', p)] >= 1)
    for p in photographers
])
solver.add(lifestyle_metro_constraint)

# 4. Number of Hue's photos in Lifestyle = Number of Fuentes's photos in Sports
solver.add(photo_count[('Lifestyle', 'Hue')] == photo_count[('Sports', 'Fuentes')])

# 5. No Gagnon photos in Sports section
solver.add(photo_count[('Sports', 'Gagnon')] == 0)

# Additional condition: Both photos in one section are by Gagnon
# This means: For some section S, photo_count[(S, 'Gagnon')] == 2
# AND for the other sections, Gagnon has 0 photos (since total Gagnon photos = 2)
gagnon_both_constraint = Or([
    photo_count[(section, 'Gagnon')] == 2
    for section in sections
])
solver.add(gagnon_both_constraint)

# Ensure exactly one section has 2 Gagnon photos, others have 0
# Since total Gagnon photos = 2 (from the constraint above), if one section has 2, others must have 0
# But let's be explicit: for each section, if it doesn't have 2 Gagnon photos, it must have 0
for section in sections:
    solver.add(Or(
        photo_count[(section, 'Gagnon')] == 2,
        photo_count[(section, 'Gagnon')] == 0
    ))

# Also ensure that Gagnon doesn't have 2 photos in more than one section
# This is already enforced by the total being 2 and each section having 0 or 2

# Now evaluate each answer choice
found_options = []

# Test option A: Both Lifestyle photos are by Hue
opt_a = And(
    photo_count[('Lifestyle', 'Hue')] == 2,
    photo_count[('Lifestyle', 'Fuentes')] == 0,
    photo_count[('Lifestyle', 'Gagnon')] == 0
)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Test option B: One Lifestyle photo by Fuentes, one by Hue
opt_b = And(
    photo_count[('Lifestyle', 'Fuentes')] == 1,
    photo_count[('Lifestyle', 'Hue')] == 1,
    photo_count[('Lifestyle', 'Gagnon')] == 0
)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Test option C: Both Metro photos are by Fuentes
opt_c = And(
    photo_count[('Metro', 'Fuentes')] == 2,
    photo_count[('Metro', 'Gagnon')] == 0,
    photo_count[('Metro', 'Hue')] == 0
)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Test option D: One Metro photo by Gagnon, one by Hue
opt_d = And(
    photo_count[('Metro', 'Gagnon')] == 1,
    photo_count[('Metro', 'Hue')] == 1,
    photo_count[('Metro', 'Fuentes')] == 0
)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Test option E: Both Sports photos are by Hue
opt_e = And(
    photo_count[('Sports', 'Hue')] == 2,
    photo_count[('Sports', 'Fuentes')] == 0,
    photo_count[('Sports', 'Gagnon')] == 0  # This is already constrained to 0
)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")