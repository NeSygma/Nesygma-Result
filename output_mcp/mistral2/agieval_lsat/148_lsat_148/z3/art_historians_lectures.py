from z3 import *

# Declare historians and topics
Historians = EnumSort('Historians', ['Farley', 'Garcia', 'Holden', 'Jiang'])
Topics = EnumSort('Topics', ['Lithographs', 'OilPaintings', 'Sculptures', 'Watercolors'])

# Extract values for convenience
Farley, Garcia, Holden, Jiang = Historians
Lithographs, OilPaintings, Sculptures, Watercolors = Topics

# Declare slot positions (1 to 4)
Slot = IntSort()

# Create solver
solver = Solver()

# Decision variables:
# historian_to_topic[h] = topic assigned to historian h
# historian_to_slot[h] = slot assigned to historian h
# topic_to_slot[t] = slot assigned to topic t

# Use arrays to map historians to topics and slots, and topics to slots
historian_to_topic = Function('historian_to_topic', Historians, Topics)
historian_to_slot = Function('historian_to_slot', Historians, Slot)
topic_to_slot = Function('topic_to_slot', Topics, Slot)

# Each historian gives exactly one lecture (one topic and one slot)
for h in [Farley, Garcia, Holden, Jiang]:
    # Historian h is assigned exactly one topic
    solver.add(Exists([t], historian_to_topic(h) == t))
    # Historian h is assigned exactly one slot
    solver.add(historian_to_slot(h) >= 1, historian_to_slot(h) <= 4)

# Each topic is given by exactly one historian and in exactly one slot
for t in [Lithographs, OilPaintings, Sculptures, Watercolors]:
    # Topic t is assigned to exactly one historian
    solver.add(Exists([h], historian_to_topic(h) == t))
    # Topic t is assigned to exactly one slot
    solver.add(topic_to_slot(t) >= 1, topic_to_slot(t) <= 4)

# Each slot has exactly one historian and one topic
for s in range(1, 5):
    # Exactly one historian is assigned to slot s
    solver.add(Exists([h], historian_to_slot(h) == s))
    # Exactly one topic is assigned to slot s
    solver.add(Exists([t], topic_to_slot(t) == s))

# Constraint: Garcia gives the Sculptures lecture
solver.add(historian_to_topic(Garcia) == Sculptures)

# Ordering constraints
# Oil Paintings < Lithographs
solver.add(Implies(
    And(Exists([h], And(historian_to_topic(h) == OilPaintings, historian_to_slot(h) == s1)),
        Exists([h2], And(historian_to_topic(h2) == Lithographs, historian_to_slot(h2) == s2))),
    s1 < s2
))

# Watercolors < Lithographs
solver.add(Implies(
    And(Exists([h], And(historian_to_topic(h) == Watercolors, historian_to_slot(h) == s1)),
        Exists([h2], And(historian_to_topic(h2) == Lithographs, historian_to_slot(h2) == s2))),
    s1 < s2
))

# Farley's lecture < Oil Paintings lecture
solver.add(Implies(
    And(Exists([h], And(historian_to_topic(h) == Farley, historian_to_slot(h) == s1)),
        Exists([h2], And(historian_to_topic(h2) == OilPaintings, historian_to_slot(h2) == s2))),
    s1 < s2
))

# Holden's lecture < Garcia's lecture
solver.add(Implies(
    And(Exists([h], And(historian_to_topic(h) == Holden, historian_to_slot(h) == s1)),
        Exists([h2], And(historian_to_topic(h2) == Garcia, historian_to_slot(h2) == s2))),
    s1 < s2
))

# Holden's lecture < Jiang's lecture
solver.add(Implies(
    And(Exists([h], And(historian_to_topic(h) == Holden, historian_to_slot(h) == s1)),
        Exists([h2], And(historian_to_topic(h2) == Jiang, historian_to_slot(h2) == s2))),
    s1 < s2
))

# Ensure all historians and topics are assigned uniquely
# Each historian has a unique topic
solver.add(Distinct([historian_to_topic(h) for h in [Farley, Garcia, Holden, Jiang]]))
# Each historian has a unique slot
solver.add(Distinct([historian_to_slot(h) for h in [Farley, Garcia, Holden, Jiang]]))
# Each topic has a unique slot
solver.add(Distinct([topic_to_slot(t) for t in [Lithographs, OilPaintings, Sculptures, Watercolors]]))

# Now evaluate the multiple choice options
found_options = []

# Option A: The lithographs lecture is third
solver.push()
solver.add(topic_to_slot(Lithographs) == 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The oil paintings lecture is third
solver.push()
solver.add(topic_to_slot(OilPaintings) == 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: The sculptures lecture is first
solver.push()
solver.add(topic_to_slot(Sculptures) == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The sculptures lecture is second
solver.push()
solver.add(topic_to_slot(Sculptures) == 2)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The watercolors lecture is second
solver.push()
solver.add(topic_to_slot(Watercolors) == 2)
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