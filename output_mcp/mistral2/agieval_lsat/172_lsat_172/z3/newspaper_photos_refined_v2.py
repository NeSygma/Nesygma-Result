from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare photographers and sections
Fuentes, Gagnon, Hue = Ints('Fuentes Gagnon Hue')
Lifestyle, Metro, Sports = Ints('Lifestyle Metro Sports')

# Assign unique integer values to photographers and sections
Fuentes_val, Gagnon_val, Hue_val = 0, 1, 2
Lifestyle_val, Metro_val, Sports_val = 0, 1, 2

# Total photographs: 6, indexed 0 to 5
num_photos = 6
photos = [Int(f'photo_{i}') for i in range(num_photos)]

# Each photo is assigned to a section and a photographer
section = [Int(f'section_{i}') for i in range(num_photos)]
photographer = [Int(f'photographer_{i}') for i in range(num_photos)]

# Initialize solver
solver = Solver()

# Helper: Add constraints to ensure each photo is assigned to a valid section and photographer
for i in range(num_photos):
    solver.add(Or(section[i] == Lifestyle_val, section[i] == Metro_val, section[i] == Sports_val))
    solver.add(Or(photographer[i] == Fuentes_val, photographer[i] == Gagnon_val, photographer[i] == Hue_val))

# Constraint 1: Exactly 2 photos per section
for sec in [Lifestyle_val, Metro_val, Sports_val]:
    solver.add(Sum([If(section[i] == sec, 1, 0) for i in range(num_photos)]) == 2)

# Constraint 2: Each photographer has at least 1 and at most 3 photos
for ph in [Fuentes_val, Gagnon_val, Hue_val]:
    solver.add(Sum([If(photographer[i] == ph, 1, 0) for i in range(num_photos)]) >= 1)
    solver.add(Sum([If(photographer[i] == ph, 1, 0) for i in range(num_photos)]) <= 3)

# Constraint 3: At least one Lifestyle photo is by a photographer who also has a photo in Metro
lifestyle_photos = [i for i in range(num_photos) if section[i] == Lifestyle_val]
metro_photos = [i for i in range(num_photos) if section[i] == Metro_val]
lifestyle_photographers = [photographer[i] for i in lifestyle_photos]
metro_photographers = [photographer[i] for i in metro_photos]
solver.add(Or([And(ph == metro_photographers[j], ph == lifestyle_photographers[k])
               for j in range(len(metro_photographers))
               for k in range(len(lifestyle_photographers))]))

# Constraint 4: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
hue_in_lifestyle = Sum([If(And(section[i] == Lifestyle_val, photographer[i] == Hue_val), 1, 0) for i in range(num_photos)])
fuentes_in_sports = Sum([If(And(section[i] == Sports_val, photographer[i] == Fuentes_val), 1, 0) for i in range(num_photos)])
solver.add(hue_in_lifestyle == fuentes_in_sports)

# Constraint 5: No Gagnon photos in Sports
solver.add(Sum([If(And(section[i] == Sports_val, photographer[i] == Gagnon_val), 1, 0) for i in range(num_photos)]) == 0)

# Given condition: One Lifestyle photo is by Fuentes, one is by Hue
solver.add(Sum([If(And(section[i] == Lifestyle_val, photographer[i] == Fuentes_val), 1, 0) for i in range(num_photos)]) == 1)
solver.add(Sum([If(And(section[i] == Lifestyle_val, photographer[i] == Hue_val), 1, 0) for i in range(num_photos)]) == 1)

# Multiple-choice options
found_options = []

# Option A: Both Metro photos are by Fuentes
solver.push()
metro_fotos = [i for i in range(num_photos) if section[i] == Metro_val]
solver.add(Sum([If(And(photographer[i] == Fuentes_val, section[i] == Metro_val), 1, 0) for i in metro_fotos]) == 2)
if solver.check() == sat:
    found_options.append("A")
    print("Option A is SAT")
solver.pop()

# Option B: Both Metro photos are by Gagnon
solver.push()
solver.add(Sum([If(And(photographer[i] == Gagnon_val, section[i] == Metro_val), 1, 0) for i in metro_fotos]) == 2)
if solver.check() == sat:
    found_options.append("B")
    print("Option B is SAT")
solver.pop()

# Option C: Exactly one Metro photo is by Hue
solver.push()
solver.add(Sum([If(And(photographer[i] == Hue_val, section[i] == Metro_val), 1, 0) for i in metro_fotos]) == 1)
if solver.check() == sat:
    found_options.append("C")
    print("Option C is SAT")
solver.pop()

# Option D: Both Sports photos are by Hue
solver.push()
sport_fotos = [i for i in range(num_photos) if section[i] == Sports_val]
solver.add(Sum([If(photographer[i] == Hue_val, 1, 0) for i in sport_fotos]) == 2)
if solver.check() == sat:
    found_options.append("D")
    print("Option D is SAT")
solver.pop()

# Option E: Neither Sports photo is by Hue
solver.push()
solver.add(Sum([If(photographer[i] == Hue_val, 1, 0) for i in sport_fotos]) == 0)
if solver.check() == sat:
    found_options.append("E")
    print("Option E is SAT")
solver.pop()

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