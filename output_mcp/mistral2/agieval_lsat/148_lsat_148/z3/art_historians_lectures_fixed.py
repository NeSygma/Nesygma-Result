from z3 import *

# Declare historians and topics as IntSort for simplicity
Historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
Topics = ['Lithographs', 'OilPaintings', 'Sculptures', 'Watercolors']

# Create solver
solver = Solver()

# Decision variables:
# historian_to_topic[h] = topic assigned to historian h (0-3)
# historian_to_slot[h] = slot assigned to historian h (1-4)
# topic_to_slot[t] = slot assigned to topic t (1-4)

historian_to_topic = [Int(f'ht_{h}') for h in Historians]
historian_to_slot = [Int(f'hs_{h}') for h in Historians]
topic_to_slot = [Int(f'ts_{t}') for t in Topics]

# Each historian gives exactly one lecture (one topic and one slot)
for i in range(4):
    solver.add(historian_to_topic[i] >= 0, historian_to_topic[i] < 4)
    solver.add(historian_to_slot[i] >= 1, historian_to_slot[i] <= 4)

# Each topic is given by exactly one historian and in exactly one slot
for i in range(4):
    solver.add(topic_to_slot[i] >= 1, topic_to_slot[i] <= 4)

# Each slot has exactly one historian and one topic
for s in range(1, 5):
    solver.add(Sum([If(hs == s, 1, 0) for hs in historian_to_slot]) == 1)
    solver.add(Sum([If(ts == s, 1, 0) for ts in topic_to_slot]) == 1)

# Constraint: Garcia gives the Sculptures lecture
# Garcia is index 1, Sculptures is index 2
solver.add(historian_to_topic[1] == 2)

# Ordering constraints
# Oil Paintings (1) < Lithographs (0)
# Watercolors (3) < Lithographs (0)
# Farley's lecture (0) < Oil Paintings lecture (1)
# Holden's lecture (2) < Garcia's lecture (1)
# Holden's lecture (2) < Jiang's lecture (3)

# Instead of ForAll, we will directly encode the ordering constraints using the topic_to_slot mapping
solver.add(topic_to_slot[1] < topic_to_slot[0])  # OilPaintings < Lithographs
solver.add(topic_to_slot[3] < topic_to_slot[0])  # Watercolors < Lithographs

# To encode Farley's lecture < Oil Paintings lecture, we need to find the slot of Farley's lecture
# We know Farley's topic is historian_to_topic[0], and its slot is historian_to_slot[0]
# Oil Paintings topic is historian_to_topic[i] == 1, and its slot is topic_to_slot[1]
# So we need: historian_to_slot[0] < topic_to_slot[1]

# Similarly, Holden's lecture < Garcia's lecture and Holden's lecture < Jiang's lecture
# Holden's slot is historian_to_slot[2]
# Garcia's slot is historian_to_slot[1]
# Jiang's slot is historian_to_slot[3]
# So we need: historian_to_slot[2] < historian_to_slot[1] and historian_to_slot[2] < historian_to_slot[3]

solver.add(historian_to_slot[0] < topic_to_slot[1])  # Farley < OilPaintings
solver.add(historian_to_slot[2] < historian_to_slot[1])  # Holden < Garcia
solver.add(historian_to_slot[2] < historian_to_slot[3])  # Holden < Jiang

# Ensure all historians and topics are assigned uniquely
solver.add(Distinct(historian_to_topic))
solver.add(Distinct(historian_to_slot))
solver.add(Distinct(topic_to_slot))

# Now evaluate the multiple choice options
found_options = []

# Option A: The lithographs lecture is third
solver.push()
solver.add(topic_to_slot[0] == 3)  # Lithographs is index 0
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The oil paintings lecture is third
solver.push()
solver.add(topic_to_slot[1] == 3)  # OilPaintings is index 1
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The sculptures lecture is first
solver.push()
solver.add(topic_to_slot[2] == 1)  # Sculptures is index 2
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The sculptures lecture is second
solver.push()
solver.add(topic_to_slot[2] == 2)  # Sculptures is index 2
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The watercolors lecture is second
solver.push()
solver.add(topic_to_slot[3] == 2)  # Watercolors is index 3
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