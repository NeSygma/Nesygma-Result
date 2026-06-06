from z3 import *

# Define cargo types as integers for easier handling
fuel = 0
grain = 1
livestock = 2
machinery = 3
produce = 4
textiles = 5

# Create a solver
solver = Solver()

# Declare variables for each bay (1 through 6)
# bay[i] will hold the cargo type in bay i+1 (0-based index for bays 1-6)
bay = [Int(f'bay_{i+1}') for i in range(6)]

# Add constraints that all cargo types are distinct
solver.add(Distinct(bay))

# Constraint 1: The bay holding grain has a higher number than the bay holding livestock
# Find the index of grain and livestock in the bay list
solver.add(Or([And(bay[i] == grain, bay[j] == livestock, i > j) for i in range(6) for j in range(6)]))

# Constraint 2: The bay holding livestock has a higher number than the bay holding textiles
solver.add(Or([And(bay[i] == livestock, bay[j] == textiles, i > j) for i in range(6) for j in range(6)]))

# Constraint 3: The bay holding produce has a higher number than the bay holding fuel
solver.add(Or([And(bay[i] == produce, bay[j] == fuel, i > j) for i in range(6) for j in range(6)]))

# Constraint 4: The bay holding textiles is next to the bay holding produce
solver.add(Or(
    Or([And(bay[i] == textiles, bay[i+1] == produce) for i in range(5)]),
    Or([And(bay[i] == produce, bay[i+1] == textiles) for i in range(5)])
))

# Now, evaluate the multiple-choice options for bay 4
# Options:
# A: grain
# B: livestock
# C: machinery
# D: produce
# E: textiles

found_options = []

# Option A: bay 4 holds grain
solver.push()
solver.add(bay[3] == grain)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: bay 4 holds livestock
solver.push()
solver.add(bay[3] == livestock)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: bay 4 holds machinery
solver.push()
solver.add(bay[3] == machinery)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: bay 4 holds produce
solver.push()
solver.add(bay[3] == produce)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: bay 4 holds textiles
solver.push()
solver.add(bay[3] == textiles)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")