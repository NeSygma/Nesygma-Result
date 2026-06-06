from z3 import *

solver = Solver()

# Define topic indices
LITHO = 0
OIL = 1
SCULPT = 2
WATER = 3

# Historians
topic_F = Int('topic_F')
topic_G = Int('topic_G')
topic_H = Int('topic_H')
topic_J = Int('topic_J')

# Array mapping topic -> position (1-4)
pos = Array('pos', IntSort(), IntSort())

# Positions for each historian (derived)
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')

# Base constraints
# Each topic position between 1 and 4
for i in range(4):
    solver.add(Select(pos, i) >= 1, Select(pos, i) <= 4)
# All topic positions distinct
solver.add(Distinct([Select(pos, i) for i in range(4)]))

# Each historian's topic between 0 and 3
solver.add(topic_F >= 0, topic_F <= 3)
solver.add(topic_G >= 0, topic_G <= 3)
solver.add(topic_H >= 0, topic_H <= 3)
solver.add(topic_J >= 0, topic_J <= 3)
# All historians have distinct topics
solver.add(Distinct([topic_F, topic_G, topic_H, topic_J]))

# Link historian positions to topic positions using Or-loop pattern
# pos_F == Select(pos, topic_F)
# We'll use an Or over possible topics
solver.add(Or([And(topic_F == i, pos_F == Select(pos, i)) for i in range(4)]))
solver.add(Or([And(topic_G == i, pos_G == Select(pos, i)) for i in range(4)]))
solver.add(Or([And(topic_H == i, pos_H == Select(pos, i)) for i in range(4)]))
solver.add(Or([And(topic_J == i, pos_J == Select(pos, i)) for i in range(4)]))

# Given: Garcia gives sculptures lecture
solver.add(topic_G == SCULPT)

# Constraint 1: oil and watercolors earlier than lithographs
solver.add(Select(pos, OIL) < Select(pos, LITHO))
solver.add(Select(pos, WATER) < Select(pos, LITHO))

# Constraint 2: Farley earlier than oil paintings
solver.add(pos_F < Select(pos, OIL))

# Constraint 3: Holden earlier than Garcia and Jiang
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Now test each option
options = [
    ("A", Select(pos, LITHO) == 3),
    ("B", Select(pos, OIL) == 3),
    ("C", Select(pos, SCULPT) == 1),
    ("D", Select(pos, SCULPT) == 2),
    ("E", Select(pos, WATER) == 2)
]

found_options = []
for letter, constr in options:
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