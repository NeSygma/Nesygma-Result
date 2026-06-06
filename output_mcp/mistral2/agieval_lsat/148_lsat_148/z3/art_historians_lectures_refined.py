from z3 import *

# Declare historians and topics
Historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
Topics = ['Lithographs', 'OilPaintings', 'Sculptures', 'Watercolors']

# Create solver
solver = Solver()

# Decision variables:
# historian_topic[h] = topic assigned to historian h (0-3)
# historian_slot[h] = slot assigned to historian h (1-4)
# topic_slot[t] = slot assigned to topic t (0-3)

historian_topic = [Int(f'ht_{h}') for h in Historians]
historian_slot = [Int(f'hs_{h}') for h in Historians]
topic_slot = [Int(f'ts_{t}') for t in Topics]

# Each historian gives exactly one topic and one slot
for i in range(4):
    solver.add(historian_topic[i] >= 0, historian_topic[i] < 4)
    solver.add(historian_slot[i] >= 1, historian_slot[i] <= 4)

# Each topic is assigned to exactly one historian
solver.add(Distinct(historian_topic))

# Each slot is assigned to exactly one historian
solver.add(Distinct(historian_slot))

# Each topic is assigned to exactly one slot
for t in Topics:
    solver.add(topic_slot[Topics.index(t)] >= 1, topic_slot[Topics.index(t)] <= 4)

# Each slot is assigned to exactly one topic
solver.add(Distinct(topic_slot))

# Constraint: Garcia gives the Sculptures lecture
# Garcia is index 1, Sculptures is index 2
solver.add(historian_topic[1] == 2)

# Link historian_topic to topic_slot: topic_slot[t] = historian_slot[h] where historian_topic[h] = t
for h in range(4):
    for t in range(4):
        solver.add(If(historian_topic[h] == t, topic_slot[t] == historian_slot[h], True))

# Ordering constraints:
# Oil Paintings (1) < Lithographs (0)
# Watercolors (3) < Lithographs (0)
# Farley's lecture (0) < Oil Paintings lecture (1)
# Holden's lecture (2) < Garcia's lecture (1)
# Holden's lecture (2) < Jiang's lecture (3)

solver.add(topic_slot[1] < topic_slot[0])  # OilPaintings < Lithographs
solver.add(topic_slot[3] < topic_slot[0])  # Watercolors < Lithographs
solver.add(historian_slot[0] < topic_slot[1])  # Farley < OilPaintings
solver.add(historian_slot[2] < historian_slot[1])  # Holden < Garcia
solver.add(historian_slot[2] < historian_slot[3])  # Holden < Jiang

# Now evaluate the multiple choice options
found_options = []

# Option A: The lithographs lecture is third
solver.push()
solver.add(topic_slot[0] == 3)  # Lithographs is index 0
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The oil paintings lecture is third
solver.push()
solver.add(topic_slot[1] == 3)  # OilPaintings is index 1
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The sculptures lecture is first
solver.push()
solver.add(topic_slot[2] == 1)  # Sculptures is index 2
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The sculptures lecture is second
solver.push()
solver.add(topic_slot[2] == 2)  # Sculptures is index 2
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The watercolors lecture is second
solver.push()
solver.add(topic_slot[3] == 2)  # Watercolors is index 3
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