from z3 import *

# Define people and zones
people = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']
zone = {p: Int(f'zone_{p}') for p in people}

solver = Solver()

# Domain constraints: each zone between 1 and 3
for p in people:
    solver.add(zone[p] >= 1)
    solver.add(zone[p] <= 3)

# Constraint 1: Either Parra or Tiao (but not both) works in Zone 1.
solver.add((zone['Parra'] == 1) != (zone['Tiao'] == 1))

# Constraint 2: Either Tiao or Udall (but not both) works in Zone 2.
solver.add((zone['Tiao'] == 2) != (zone['Udall'] == 2))

# Constraint 3: Parra and Quinn work in the same sales zone.
solver.add(zone['Parra'] == zone['Quinn'])

# Constraint 4: Stuckey and Udall work in the same sales zone.
solver.add(zone['Stuckey'] == zone['Udall'])

# Constraint 5: More reps in Zone 3 than Zone 2.
count2 = Sum([If(zone[p] == 2, 1, 0) for p in people])
count3 = Sum([If(zone[p] == 3, 1, 0) for p in people])
solver.add(count3 > count2)

# Extra condition for the question: Mahr and Stuckey work in the same zone.
solver.add(zone['Mahr'] == zone['Stuckey'])

# Now test each answer choice
found_options = []

# Option A: Kim works in Zone 2.
solver.push()
solver.add(zone['Kim'] == 2)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Mahr works in Zone 1.
solver.push()
solver.add(zone['Mahr'] == 1)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: Parra works in Zone 3.
solver.push()
solver.add(zone['Parra'] == 3)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Stuckey works in Zone 2.
solver.push()
solver.add(zone['Stuckey'] == 2)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Tiao works in Zone 1.
solver.push()
solver.add(zone['Tiao'] == 1)
if solver.check() == sat:
    found_options.append('E')
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