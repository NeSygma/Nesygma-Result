from z3 import *

# Create solver
solver = Solver()

# Define variables
# Lectures: 1, 2, 3, 4, 5 (positions)
# Birds: oystercatchers, petrels, rails, sandpipers, terns
# Locations: Gladwyn Hall (G) or Howard Auditorium (H)

# We'll use integers for positions 1-5
positions = [1, 2, 3, 4, 5]

# For each position, we need to know which bird and which location
# We'll use arrays indexed by position (1-5, but we'll use 0-4 for Python indexing)
bird_at = [Int(f'bird_at_{i}') for i in range(5)]  # 0: oystercatchers, 1: petrels, 2: rails, 3: sandpipers, 4: terns
location_at = [Int(f'location_at_{i}') for i in range(5)]  # 0: Gladwyn Hall, 1: Howard Auditorium

# Domain constraints: each bird appears exactly once
bird_values = [0, 1, 2, 3, 4]  # 0-4 for the 5 birds
solver.add(Distinct(bird_at))

# Domain constraints: each location is 0 or 1
for i in range(5):
    solver.add(Or(location_at[i] == 0, location_at[i] == 1))

# Constraint 1: The first lecture is in Gladwyn Hall
solver.add(location_at[0] == 0)  # position 1 (index 0)

# Constraint 2: The fourth lecture is in Howard Auditorium
solver.add(location_at[3] == 1)  # position 4 (index 3)

# Constraint 3: Exactly three of the lectures are in Gladwyn Hall
# Count how many are in Gladwyn Hall (0)
gladwyn_count = Sum([If(location_at[i] == 0, 1, 0) for i in range(5)])
solver.add(gladwyn_count == 3)

# Constraint 4: The lecture on sandpipers is in Howard Auditorium and is given earlier than the lecture on oystercatchers
# sandpipers = 3, oystercatchers = 0
# Find position of sandpipers and oystercatchers
sandpipers_pos = Int('sandpipers_pos')
oystercatchers_pos = Int('oystercatchers_pos')

# Use Or-loop to find positions
solver.add(Or([sandpipers_pos == i for i in range(5)]))
solver.add(Or([oystercatchers_pos == i for i in range(5)]))

# Link positions to bird_at
for i in range(5):
    solver.add(Implies(sandpipers_pos == i, bird_at[i] == 3))
    solver.add(Implies(oystercatchers_pos == i, bird_at[i] == 0))

# Sandpipers in Howard Auditorium (location 1)
solver.add(Or([And(sandpipers_pos == i, location_at[i] == 1) for i in range(5)]))

# Sandpipers earlier than oystercatchers
solver.add(sandpipers_pos < oystercatchers_pos)

# Constraint 5: The lecture on terns is given earlier than the lecture on petrels, which is in Gladwyn Hall
# terns = 4, petrels = 1
terns_pos = Int('terns_pos')
petrels_pos = Int('petrels_pos')

solver.add(Or([terns_pos == i for i in range(5)]))
solver.add(Or([petrels_pos == i for i in range(5)]))

for i in range(5):
    solver.add(Implies(terns_pos == i, bird_at[i] == 4))
    solver.add(Implies(petrels_pos == i, bird_at[i] == 1))

# Terns earlier than petrels
solver.add(terns_pos < petrels_pos)

# Petrels in Gladwyn Hall (location 0)
solver.add(Or([And(petrels_pos == i, location_at[i] == 0) for i in range(5)]))

# Now evaluate each answer choice for the fifth lecture (position 5, index 4)
# We need to check which of these could be true

# Define the options as constraints on the fifth lecture (index 4)
opt_a_constr = And(bird_at[4] == 0, location_at[4] == 0)  # oystercatchers and Gladwyn Hall
opt_b_constr = And(bird_at[4] == 1, location_at[4] == 1)  # petrels and Howard Auditorium
opt_c_constr = And(bird_at[4] == 2, location_at[4] == 1)  # rails and Howard Auditorium
opt_d_constr = And(bird_at[4] == 3, location_at[4] == 1)  # sandpipers and Howard Auditorium
opt_e_constr = And(bird_at[4] == 4, location_at[4] == 0)  # terns and Gladwyn Hall

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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