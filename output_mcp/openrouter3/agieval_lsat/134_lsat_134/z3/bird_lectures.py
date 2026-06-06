from z3 import *

# Create solver
solver = Solver()

# Define variables
# We'll use arrays for positions and venues
# positions: 0-indexed for positions 1-5
positions = [Int(f'pos_{i}') for i in range(5)]  # values: 0-4 representing bird types
# Let's map bird types to numbers:
# 0: oystercatchers, 1: petrels, 2: rails, 3: sandpipers, 4: terns
bird_names = ['oystercatchers', 'petrels', 'rails', 'sandpipers', 'terns']

# Venue for each position: 0 = Gladwyn Hall, 1 = Howard Auditorium
venue = [Int(f'venue_{i}') for i in range(5)]

# Base constraints
# 1. First lecture is in Gladwyn Hall (position 0 venue = 0)
solver.add(venue[0] == 0)

# 2. Fourth lecture is in Howard Auditorium (position 3 venue = 1)
solver.add(venue[3] == 1)

# 3. Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(venue[i] == 0, 1, 0) for i in range(5)]) == 3)

# 4. Sandpipers lecture is in Howard Auditorium and earlier than oystercatchers
# Find position of sandpipers (bird 3) and oystercatchers (bird 0)
sandpipers_pos = Int('sandpipers_pos')
oystercatchers_pos = Int('oystercatchers_pos')
solver.add(sandpipers_pos >= 0, sandpipers_pos < 5)
solver.add(oystercatchers_pos >= 0, oystercatchers_pos < 5)

# Link positions to venue array
solver.add(venue[sandpipers_pos] == 1)  # sandpipers in Howard
solver.add(sandpipers_pos < oystercatchers_pos)  # sandpipers earlier

# 5. Terns lecture is earlier than petrels, and petrels is in Gladwyn Hall
terns_pos = Int('terns_pos')
petrels_pos = Int('petrels_pos')
solver.add(terns_pos >= 0, terns_pos < 5)
solver.add(petrels_pos >= 0, petrels_pos < 5)
solver.add(terns_pos < petrels_pos)  # terns earlier than petrels
solver.add(venue[petrels_pos] == 0)  # petrels in Gladwyn Hall

# Each bird type appears exactly once
bird_positions = [Int(f'bird_{i}_pos') for i in range(5)]  # position of each bird type
for i in range(5):
    solver.add(bird_positions[i] >= 0, bird_positions[i] < 5)
solver.add(Distinct(bird_positions))  # all positions different

# Link bird_positions to our specific variables
solver.add(bird_positions[3] == sandpipers_pos)  # sandpipers
solver.add(bird_positions[0] == oystercatchers_pos)  # oystercatchers
solver.add(bird_positions[4] == terns_pos)  # terns
solver.add(bird_positions[1] == petrels_pos)  # petrels

# Now evaluate each answer choice
# For each option, we'll add constraints that the order matches the given sequence
found_options = []

# Option A: oystercatchers, petrels, rails, sandpipers, terns
solver.push()
# Add constraints for this specific order
solver.add(bird_positions[0] == 0)  # oystercatchers first
solver.add(bird_positions[1] == 1)  # petrels second
solver.add(bird_positions[2] == 2)  # rails third
solver.add(bird_positions[3] == 3)  # sandpipers fourth
solver.add(bird_positions[4] == 4)  # terns fifth
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: petrels, sandpipers, oystercatchers, terns, rails
solver.push()
solver.add(bird_positions[1] == 0)  # petrels first
solver.add(bird_positions[3] == 1)  # sandpipers second
solver.add(bird_positions[0] == 2)  # oystercatchers third
solver.add(bird_positions[4] == 3)  # terns fourth
solver.add(bird_positions[2] == 4)  # rails fifth
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: rails, sandpipers, terns, petrels, oystercatchers
solver.push()
solver.add(bird_positions[2] == 0)  # rails first
solver.add(bird_positions[3] == 1)  # sandpipers second
solver.add(bird_positions[4] == 2)  # terns third
solver.add(bird_positions[1] == 3)  # petrels fourth
solver.add(bird_positions[0] == 4)  # oystercatchers fifth
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: sandpipers, terns, oystercatchers, rails, petrels
solver.push()
solver.add(bird_positions[3] == 0)  # sandpipers first
solver.add(bird_positions[4] == 1)  # terns second
solver.add(bird_positions[0] == 2)  # oystercatchers third
solver.add(bird_positions[2] == 3)  # rails fourth
solver.add(bird_positions[1] == 4)  # petrels fifth
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: terns, petrels, sandpipers, oystercatchers, rails
solver.push()
solver.add(bird_positions[4] == 0)  # terns first
solver.add(bird_positions[1] == 1)  # petrels second
solver.add(bird_positions[3] == 2)  # sandpipers third
solver.add(bird_positions[0] == 3)  # oystercatchers fourth
solver.add(bird_positions[2] == 4)  # rails fifth
if solver.check() == sat:
    found_options.append("E")
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