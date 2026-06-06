from z3 import *

# BENCHMARK_MODE: ON (model-finding)
BENCHMARK_MODE = True

solver = Solver()

# Encode bird types and locations
bird_types = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
bird_to_int = {b: i for i, b in enumerate(bird_types)}
location_to_int = {"Gladwyn Hall": 0, "Howard Auditorium": 1}

# Decision variables:
# order[i] = bird type for lecture i (0-based index)
# loc[i] = location for lecture i (0-based index)
order = [Int(f"order_{i}") for i in range(5)]
loc = [Int(f"loc_{i}") for i in range(5)]

# Helper: bird type is one of the five
for i in range(5):
    solver.add(And(order[i] >= 0, order[i] < 5))

# Constraint 1: First lecture is in Gladwyn Hall
solver.add(loc[0] == location_to_int["Gladwyn Hall"])

# Constraint 2: Fourth lecture is in Howard Auditorium
solver.add(loc[3] == location_to_int["Howard Auditorium"])

# Constraint 3: Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(loc[i] == location_to_int["Gladwyn Hall"], 1, 0) for i in range(5)]) == 3)

# Constraint 4: Sandpipers (3) is in Howard Auditorium (1) and is earlier than oystercatchers (0)
# We need to find the index of sandpipers and oystercatchers in the order
sandpiper_idx = Int("sandpiper_idx")
oystercatcher_idx = Int("oystercatcher_idx")
# Constrain sandpiper_idx and oystercatcher_idx to be the positions of sandpipers and oystercatchers
solver.add(Or([And(order[i] == bird_to_int["sandpipers"], sandpiper_idx == i) for i in range(5)]))
solver.add(Or([And(order[i] == bird_to_int["oystercatchers"], oystercatcher_idx == i) for i in range(5)]))
# Sandpipers must be in Howard Auditorium
solver.add(Implies(sandpiper_idx == 0, loc[0] == location_to_int["Howard Auditorium"]))
solver.add(Implies(sandpiper_idx == 1, loc[1] == location_to_int["Howard Auditorium"]))
solver.add(Implies(sandpiper_idx == 2, loc[2] == location_to_int["Howard Auditorium"]))
solver.add(Implies(sandpiper_idx == 3, loc[3] == location_to_int["Howard Auditorium"]))
solver.add(Implies(sandpiper_idx == 4, loc[4] == location_to_int["Howard Auditorium"]))
# Sandpipers must be earlier than oystercatchers
solver.add(sandpiper_idx < oystercatcher_idx)

# Constraint 5: Terns (4) is earlier than petrels (1), and petrels is in Gladwyn Hall (0)
tern_idx = Int("tern_idx")
petrel_idx = Int("petrel_idx")
solver.add(Or([And(order[i] == bird_to_int["terns"], tern_idx == i) for i in range(5)]))
solver.add(Or([And(order[i] == bird_to_int["petrels"], petrel_idx == i) for i in range(5)]))
solver.add(tern_idx < petrel_idx)
# Petrels must be in Gladwyn Hall
solver.add(Implies(petrel_idx == 0, loc[0] == location_to_int["Gladwyn Hall"]))
solver.add(Implies(petrel_idx == 1, loc[1] == location_to_int["Gladwyn Hall"]))
solver.add(Implies(petrel_idx == 2, loc[2] == location_to_int["Gladwyn Hall"]))
solver.add(Implies(petrel_idx == 3, loc[3] == location_to_int["Gladwyn Hall"]))
solver.add(Implies(petrel_idx == 4, loc[4] == location_to_int["Gladwyn Hall"]))

# Additional Constraint: Terns (4) is in Howard Auditorium (1)
solver.add(Implies(tern_idx == 0, loc[0] == location_to_int["Howard Auditorium"]))
solver.add(Implies(tern_idx == 1, loc[1] == location_to_int["Howard Auditorium"]))
solver.add(Implies(tern_idx == 2, loc[2] == location_to_int["Howard Auditorium"]))
solver.add(Implies(tern_idx == 3, loc[3] == location_to_int["Howard Auditorium"]))
solver.add(Implies(tern_idx == 4, loc[4] == location_to_int["Howard Auditorium"]))

# All bird types are distinct
solver.add(Distinct(order))

# Now, evaluate the multiple choice options for the third lecture (index 2)
found_options = []

# Option A: Third lecture is oystercatchers and in Gladwyn Hall
solver.push()
solver.add(order[2] == bird_to_int["oystercatchers"])
solver.add(loc[2] == location_to_int["Gladwyn Hall"])
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Third lecture is rails and in Howard Auditorium
solver.push()
solver.add(order[2] == bird_to_int["rails"])
solver.add(loc[2] == location_to_int["Howard Auditorium"])
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Third lecture is rails and in Gladwyn Hall
solver.push()
solver.add(order[2] == bird_to_int["rails"])
solver.add(loc[2] == location_to_int["Gladwyn Hall"])
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Third lecture is sandpipers and in Howard Auditorium
solver.push()
solver.add(order[2] == bird_to_int["sandpipers"])
solver.add(loc[2] == location_to_int["Howard Auditorium"])
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Third lecture is terns and in Howard Auditorium
solver.push()
solver.add(order[2] == bird_to_int["terns"])
solver.add(loc[2] == location_to_int["Howard Auditorium"])
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")