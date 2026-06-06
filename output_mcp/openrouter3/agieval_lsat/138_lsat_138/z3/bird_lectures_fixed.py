from z3 import *

# Create solver
solver = Solver()

# Define variables
# Lectures: 0=Oystercatchers, 1=Petrels, 2=Rails, 3=Sandpipers, 4=Terns
# Positions: 0,1,2,3,4 (representing 1st through 5th)
# Venue: 0=Gladwyn Hall, 1=Howard Auditorium

# For each position (0-4), what bird is there?
bird_at_pos = [Int(f'bird_at_pos_{i}') for i in range(5)]
# For each position, what venue?
venue_at_pos = [Int(f'venue_at_pos_{i}') for i in range(5)]

# Domain constraints: birds are 0-4, venues are 0-1
for i in range(5):
    solver.add(bird_at_pos[i] >= 0, bird_at_pos[i] <= 4)
    solver.add(venue_at_pos[i] >= 0, venue_at_pos[i] <= 1)

# All birds are used exactly once
solver.add(Distinct(bird_at_pos))

# Constraint 1: First lecture in Gladwyn Hall (venue 0)
solver.add(venue_at_pos[0] == 0)

# Constraint 2: Fourth lecture in Howard Auditorium (venue 1)
solver.add(venue_at_pos[3] == 1)

# Constraint 3: Exactly three lectures in Gladwyn Hall
gladwyn_count = Sum([If(venue_at_pos[i] == 0, 1, 0) for i in range(5)])
solver.add(gladwyn_count == 3)

# Constraint 4: Sandpipers lecture in Howard Auditorium and earlier than oystercatchers
# Sandpipers is bird 3, Oystercatchers is bird 0
# Find positions of sandpipers and oystercatchers
sandpipers_pos = Int('sandpipers_pos')
oystercatchers_pos = Int('oystercatchers_pos')

# Use Or-Loop pattern to find positions
solver.add(Or([bird_at_pos[i] == 3 for i in range(5)]))  # Sandpipers exists
solver.add(Or([bird_at_pos[i] == 0 for i in range(5)]))  # Oystercatchers exists

# Define positions using Or-Loop
solver.add(Or([And(bird_at_pos[i] == 3, sandpipers_pos == i) for i in range(5)]))
solver.add(Or([And(bird_at_pos[i] == 0, oystercatchers_pos == i) for i in range(5)]))

# Sandpipers in Howard Auditorium - use Or-Loop for venue
solver.add(Or([And(sandpipers_pos == i, venue_at_pos[i] == 1) for i in range(5)]))

# Sandpipers earlier than oystercatchers
solver.add(sandpipers_pos < oystercatchers_pos)

# Constraint 5: Terns earlier than petrels, petrels in Gladwyn Hall
# Terns is bird 4, Petrels is bird 1
terns_pos = Int('terns_pos')
petrels_pos = Int('petrels_pos')

solver.add(Or([bird_at_pos[i] == 4 for i in range(5)]))  # Terns exists
solver.add(Or([bird_at_pos[i] == 1 for i in range(5)]))  # Petrels exists

solver.add(Or([And(bird_at_pos[i] == 4, terns_pos == i) for i in range(5)]))
solver.add(Or([And(bird_at_pos[i] == 1, petrels_pos == i) for i in range(5)]))

# Terns earlier than petrels
solver.add(terns_pos < petrels_pos)

# Petrels in Gladwyn Hall - use Or-Loop for venue
solver.add(Or([And(petrels_pos == i, venue_at_pos[i] == 0) for i in range(5)]))

# Additional given: Third lecture is on sandpipers
# Position 2 (0-indexed) is sandpipers
solver.add(bird_at_pos[2] == 3)

# Now test each option
found_options = []

# Option A: The second lecture is on oystercatchers and is in Gladwyn Hall
opt_a = And(bird_at_pos[1] == 0, venue_at_pos[1] == 0)

# Option B: The fifth lecture is on oystercatchers and is in Howard Auditorium
opt_b = And(bird_at_pos[4] == 0, venue_at_pos[4] == 1)

# Option C: The second lecture is on rails and is in Howard Auditorium
opt_c = And(bird_at_pos[1] == 2, venue_at_pos[1] == 1)

# Option D: The second lecture is on terns and is in Gladwyn Hall
opt_d = And(bird_at_pos[1] == 4, venue_at_pos[1] == 0)

# Option E: The fourth lecture is on terns and is in Howard Auditorium
opt_e = And(bird_at_pos[3] == 4, venue_at_pos[3] == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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