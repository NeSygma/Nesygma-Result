from z3 import *

solver = Solver()

# Birds: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# Venues: 0=Gladwyn, 1=Howard
bird = [Int(f'bird_{i}') for i in range(1, 6)]  # positions 1-5 (0-indexed: 0..4)
venue = [Int(f'venue_{i}') for i in range(1, 6)]

# Each bird is 0-4, all different
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)
solver.add(Distinct(bird))

# Each venue is 0 or 1
for i in range(5):
    solver.add(Or(venue[i] == 0, venue[i] == 1))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(venue[0] == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(venue[3] == 1)

# Constraint 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(venue[i] == 0, 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers (3) is in Howard Auditorium and earlier than oystercatchers (0)
# Find position of sandpipers and oystercatchers
sand_pos = Int('sand_pos')
oyst_pos = Int('oyst_pos')
solver.add(Or([And(bird[i] == 3, sand_pos == i) for i in range(5)]))
solver.add(Or([And(bird[i] == 0, oyst_pos == i) for i in range(5)]))
# Sandpipers venue is Howard
solver.add(Or([And(bird[i] == 3, venue[i] == 1) for i in range(5)]))
# Sandpipers earlier than oystercatchers
solver.add(sand_pos < oyst_pos)

# Constraint 5: Terns (4) earlier than petrels (1), petrels in Gladwyn
tern_pos = Int('tern_pos')
petr_pos = Int('petr_pos')
solver.add(Or([And(bird[i] == 4, tern_pos == i) for i in range(5)]))
solver.add(Or([And(bird[i] == 1, petr_pos == i) for i in range(5)]))
solver.add(tern_pos < petr_pos)
# Petrels in Gladwyn
solver.add(Or([And(bird[i] == 1, venue[i] == 0) for i in range(5)]))

# Additional condition: Third lecture (index 2) is on sandpipers
solver.add(bird[2] == 3)

# Now evaluate each option
# (A) The second lecture is on oystercatchers and is in Gladwyn Hall.
opt_a = And(bird[1] == 0, venue[1] == 0)

# (B) The fifth lecture is on oystercatchers and is in Howard Auditorium.
opt_b = And(bird[4] == 0, venue[4] == 1)

# (C) The second lecture is on rails and is in Howard Auditorium.
opt_c = And(bird[1] == 2, venue[1] == 1)

# (D) The second lecture is on terns and is in Gladwyn Hall.
opt_d = And(bird[1] == 4, venue[1] == 0)

# (E) The fourth lecture is on terns and is in Howard Auditorium.
opt_e = And(bird[3] == 4, venue[3] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for i in range(5):
            bird_names = ['oystercatchers', 'petrels', 'rails', 'sandpipers', 'terns']
            venue_names = ['Gladwyn', 'Howard']
            print(f"  Lecture {i+1}: {bird_names[m[bird[i]].as_long()]} at {venue_names[m[venue[i]].as_long()]}")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")