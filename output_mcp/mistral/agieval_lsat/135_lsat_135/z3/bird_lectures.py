from z3 import *

# Base constraints solver
solver = Solver()

# Locations: 0 = Gladwyn Hall, 1 = Howard Auditorium
# 5 lectures, indexed 0 to 4
locations = [Int(f'loc_{i}') for i in range(5)]

# Bird order: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
# bird_order[i] = bird type at position i
bird_order = [Int(f'bird_{i}') for i in range(5)]

# Each bird type appears exactly once
solver.add(Distinct(bird_order))

# Constraints on locations
solver.add(locations[0] == 0)  # First lecture in Gladwyn Hall
solver.add(locations[3] == 1)  # Fourth lecture in Howard Auditorium
solver.add(Sum([locations[i] == 0 for i in range(5)]) == 3)  # Exactly three in Gladwyn Hall

# Constraints on bird positions and locations
# Sandpiper is in Howard Auditorium and earlier than oystercatcher
# Find the position of sandpiper and oystercatcher in bird_order
solver.add(Or([And(bird_order[i] == 3, locations[i] == 1) for i in range(5)]))  # Sandpiper in Howard
solver.add(Or([And(bird_order[i] == 0, bird_order[j] == 3, i < j) for i in range(5) for j in range(5)]))  # Sandpiper earlier than oystercatcher

# Tern is earlier than petrel, and petrel is in Gladwyn Hall
solver.add(Or([And(bird_order[i] == 4, bird_order[j] == 1, i < j) for i in range(5) for j in range(5)]))  # Tern earlier than petrel
solver.add(Or([And(bird_order[i] == 1, locations[i] == 0) for i in range(5)]))  # Petrel in Gladwyn Hall

# Rails must be the remaining position
solver.add(Or([And(bird_order[i] == 2) for i in range(5)]))

# Now evaluate each option
found_options = []

# Option A: The first and second lectures are both in Gladwyn Hall
solver.push()
solver.add(And(locations[0] == 0, locations[1] == 0))
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The second and third lectures are both in Howard Auditorium
solver.push()
solver.add(And(locations[1] == 1, locations[2] == 1))
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The second and fifth lectures are both in Gladwyn Hall
solver.push()
solver.add(And(locations[1] == 0, locations[4] == 0))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The third and fourth lectures are both in Howard Auditorium
solver.push()
solver.add(And(locations[2] == 1, locations[3] == 1))
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The third and fifth lectures are both in Gladwyn Hall
solver.push()
solver.add(And(locations[2] == 0, locations[4] == 0))
if solver.check() == sat:
    found_options.append("E")
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