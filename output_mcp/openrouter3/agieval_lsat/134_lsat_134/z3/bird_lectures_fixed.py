from z3 import *

# Create solver
solver = Solver()

# We'll model the problem differently: 
# For each position (1-5), we have a bird type and a venue
# Let's use arrays for bird type and venue at each position
bird_at_pos = [Int(f'bird_at_pos_{i}') for i in range(5)]  # 0-4 for bird types
venue_at_pos = [Int(f'venue_at_pos_{i}') for i in range(5)]  # 0=Gladwyn, 1=Howard

# Bird type mapping: 0=Oystercatchers, 1=Petrels, 2=Rails, 3=Sandpipers, 4=Terns
# Constraints:
# 1. First lecture is in Gladwyn Hall
solver.add(venue_at_pos[0] == 0)

# 2. Fourth lecture is in Howard Auditorium
solver.add(venue_at_pos[3] == 1)

# 3. Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(venue_at_pos[i] == 0, 1, 0) for i in range(5)]) == 3)

# 4. Sandpipers lecture is in Howard Auditorium and earlier than oystercatchers
# We need to find positions of sandpipers and oystercatchers
# Use Or-Loop pattern to avoid indexing with Z3 variables
sandpipers_pos = Int('sandpipers_pos')
oystercatchers_pos = Int('oystercatchers_pos')
solver.add(sandpipers_pos >= 0, sandpipers_pos < 5)
solver.add(oystercatchers_pos >= 0, oystercatchers_pos < 5)
solver.add(sandpipers_pos < oystercatchers_pos)

# Link bird types to positions using Or-Loop
for i in range(5):
    # If position i has sandpipers (type 3)
    solver.add(Implies(bird_at_pos[i] == 3, sandpipers_pos == i))
    # If position i has oystercatchers (type 0)
    solver.add(Implies(bird_at_pos[i] == 0, oystercatchers_pos == i))

# Sandpipers must be in Howard Auditorium
solver.add(venue_at_pos[sandpipers_pos] == 1)

# 5. Terns lecture is earlier than petrels, and petrels is in Gladwyn Hall
terns_pos = Int('terns_pos')
petrels_pos = Int('petrels_pos')
solver.add(terns_pos >= 0, terns_pos < 5)
solver.add(petrels_pos >= 0, petrels_pos < 5)
solver.add(terns_pos < petrels_pos)

# Link bird types to positions
for i in range(5):
    # If position i has terns (type 4)
    solver.add(Implies(bird_at_pos[i] == 4, terns_pos == i))
    # If position i has petrels (type 1)
    solver.add(Implies(bird_at_pos[i] == 1, petrels_pos == i))

# Petrels must be in Gladwyn Hall
solver.add(venue_at_pos[petrels_pos] == 0)

# Each bird type appears exactly once
solver.add(Distinct(bird_at_pos))

# Each position has exactly one bird type (already ensured by Distinct)

# Now evaluate each answer choice
found_options = []

# Option A: oystercatchers, petrels, rails, sandpipers, terns
solver.push()
solver.add(bird_at_pos[0] == 0)  # oystercatchers first
solver.add(bird_at_pos[1] == 1)  # petrels second
solver.add(bird_at_pos[2] == 2)  # rails third
solver.add(bird_at_pos[3] == 3)  # sandpipers fourth
solver.add(bird_at_pos[4] == 4)  # terns fifth
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: petrels, sandpipers, oystercatchers, terns, rails
solver.push()
solver.add(bird_at_pos[0] == 1)  # petrels first
solver.add(bird_at_pos[1] == 3)  # sandpipers second
solver.add(bird_at_pos[2] == 0)  # oystercatchers third
solver.add(bird_at_pos[3] == 4)  # terns fourth
solver.add(bird_at_pos[4] == 2)  # rails fifth
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: rails, sandpipers, terns, petrels, oystercatchers
solver.push()
solver.add(bird_at_pos[0] == 2)  # rails first
solver.add(bird_at_pos[1] == 3)  # sandpipers second
solver.add(bird_at_pos[2] == 4)  # terns third
solver.add(bird_at_pos[3] == 1)  # petrels fourth
solver.add(bird_at_pos[4] == 0)  # oystercatchers fifth
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: sandpipers, terns, oystercatchers, rails, petrels
solver.push()
solver.add(bird_at_pos[0] == 3)  # sandpipers first
solver.add(bird_at_pos[1] == 4)  # terns second
solver.add(bird_at_pos[2] == 0)  # oystercatchers third
solver.add(bird_at_pos[3] == 2)  # rails fourth
solver.add(bird_at_pos[4] == 1)  # petrels fifth
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: terns, petrels, sandpipers, oystercatchers, rails
solver.push()
solver.add(bird_at_pos[0] == 4)  # terns first
solver.add(bird_at_pos[1] == 1)  # petrels second
solver.add(bird_at_pos[2] == 3)  # sandpipers third
solver.add(bird_at_pos[3] == 0)  # oystercatchers fourth
solver.add(bird_at_pos[4] == 2)  # rails fifth
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