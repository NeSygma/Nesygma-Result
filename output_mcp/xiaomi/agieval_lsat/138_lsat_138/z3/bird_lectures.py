from z3 import *

solver = Solver()

# Variables: for each lecture position (1-5), which bird and which hall
# Birds: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# Halls: 0=Gladwyn, 1=Howard

bird = [Int(f'bird_{i}') for i in range(1, 6)]
hall = [Int(f'hall_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(And(bird[i] >= 0, bird[i] <= 4))
    solver.add(Or(hall[i] == 0, hall[i] == 1))

# All birds are different
solver.add(Distinct(bird))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(hall[0] == 0)

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(hall[3] == 1)

# Constraint 3: Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i] == 0, 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers (3) is in Howard and earlier than oystercatchers (0)
# Find positions of sandpipers and oystercatchers
sandpiper_pos = Int('sandpiper_pos')
oystercatcher_pos = Int('oystercatcher_pos')
solver.add(Or([And(bird[i] == 3, sandpiper_pos == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 0, oystercatcher_pos == i+1) for i in range(5)]))
solver.add(sandpiper_pos < oystercatcher_pos)
# Sandpipers in Howard
solver.add(Or([And(bird[i] == 3, hall[i] == 1) for i in range(5)]))

# Constraint 5: Terns (4) earlier than petrels (1), petrels in Gladwyn
tern_pos = Int('tern_pos')
petrel_pos = Int('petrel_pos')
solver.add(Or([And(bird[i] == 4, tern_pos == i+1) for i in range(5)]))
solver.add(Or([And(bird[i] == 1, petrel_pos == i+1) for i in range(5)]))
solver.add(tern_pos < petrel_pos)
# Petrels in Gladwyn
solver.add(Or([And(bird[i] == 1, hall[i] == 0) for i in range(5)]))

# Additional constraint: Third lecture is on sandpipers
solver.add(bird[2] == 3)

# Now evaluate each option
found_options = []

# Option A: Second lecture is on oystercatchers and is in Gladwyn Hall
opt_a = And(bird[1] == 0, hall[1] == 0)

# Option B: Fifth lecture is on oystercatchers and is in Howard Auditorium
opt_b = And(bird[4] == 0, hall[4] == 1)

# Option C: Second lecture is on rails and is in Howard Auditorium
opt_c = And(bird[1] == 2, hall[1] == 1)

# Option D: Second lecture is on terns and is in Gladwyn Hall
opt_d = And(bird[1] == 4, hall[1] == 0)

# Option E: Fourth lecture is on terns and is in Howard Auditorium
opt_e = And(bird[3] == 4, hall[3] == 1)

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