from z3 import *

# Create solver
solver = Solver()

# Define entities
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["Lithographs", "Oil", "Sculptures", "Watercolors"]
slots = [1, 2, 3, 4]

# Create variables: topic assignment for each historian
# topic_of[historian] = topic
topic_of = {h: Int(f"topic_{h}") for h in historians}

# Create variables: time slot for each topic
# slot_of[topic] = time slot
slot_of = {t: Int(f"slot_{t}") for t in topics}

# Domain constraints: each historian gets exactly one topic, each topic assigned to exactly one historian
# We'll use distinct constraints
solver.add(Distinct([topic_of[h] for h in historians]))
for h in historians:
    solver.add(Or([topic_of[h] == i for i in range(4)]))

# Domain constraints: each topic gets exactly one time slot
solver.add(Distinct([slot_of[t] for t in topics]))
for t in topics:
    solver.add(Or([slot_of[t] == i for i in range(4)]))

# Map topic names to indices for easier constraint writing
topic_index = {"Lithographs": 0, "Oil": 1, "Sculptures": 2, "Watercolors": 3}

# Constraint 1: Oil paintings and watercolors lectures must both be earlier than lithographs lecture
# slot_of[Oil] < slot_of[Lithographs] AND slot_of[Watercolors] < slot_of[Lithographs]
solver.add(slot_of["Oil"] < slot_of["Lithographs"])
solver.add(slot_of["Watercolors"] < slot_of["Lithographs"])

# Constraint 2: Farley's lecture must be earlier than oil paintings lecture
# slot_of[topic_of[Farley]] < slot_of[Oil]
# We need to express: if Farley gives topic T, then slot_of[T] < slot_of[Oil]
# Use Or-loop pattern
for t in topics:
    solver.add(Implies(topic_of["Farley"] == topic_index[t], slot_of[t] < slot_of["Oil"]))

# Constraint 3: Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture
# slot_of[topic_of[Holden]] < slot_of[topic_of[Garcia]] AND slot_of[topic_of[Holden]] < slot_of[topic_of[Jiang]]
# Use Or-loop pattern for each comparison
for t1 in topics:
    for t2 in topics:
        solver.add(Implies(And(topic_of["Holden"] == topic_index[t1], topic_of["Garcia"] == topic_index[t2]), 
                          slot_of[t1] < slot_of[t2]))
        solver.add(Implies(And(topic_of["Holden"] == topic_index[t1], topic_of["Jiang"] == topic_index[t2]), 
                          slot_of[t1] < slot_of[t2]))

# Given condition: Garcia gives the sculptures lecture
solver.add(topic_of["Garcia"] == topic_index["Sculptures"])

# Now test each option
# Option A: The lithographs lecture is third
opt_a = (slot_of["Lithographs"] == 2)  # slot 2 means third (0-indexed: 0=first, 1=second, 2=third, 3=fourth)

# Option B: The oil paintings lecture is third
opt_b = (slot_of["Oil"] == 2)

# Option C: The sculptures lecture is first
opt_c = (slot_of["Sculptures"] == 0)

# Option D: The sculptures lecture is second
opt_d = (slot_of["Sculptures"] == 1)

# Option E: The watercolors lecture is second
opt_e = (slot_of["Watercolors"] == 1)

# Test each option
found_options = []

# Test A
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Test B
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Test C
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Test D
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Test E
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")