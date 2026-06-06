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

# Positions for each topic (1-4)
pos = [Int(f'pos_{i}') for i in range(4)]  # index 0=litho,1=oil,2=sculptures,3=watercolors

# Positions for each historian (derived)
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')

# Base constraints
# Each topic position between 1 and 4
for p in pos:
    solver.add(p >= 1, p <= 4)
# All topic positions distinct
solver.add(Distinct(pos))

# Each historian's topic between 0 and 3
solver.add(topic_F >= 0, topic_F <= 3)
solver.add(topic_G >= 0, topic_G <= 3)
solver.add(topic_H >= 0, topic_H <= 3)
solver.add(topic_J >= 0, topic_J <= 3)
# All historians have distinct topics
solver.add(Distinct([topic_F, topic_G, topic_H, topic_J]))

# Link historian positions to topic positions
solver.add(pos_F == pos[topic_F])
solver.add(pos_G == pos[topic_G])
solver.add(pos_H == pos[topic_H])
solver.add(pos_J == pos[topic_J])

# Given: Garcia gives sculptures lecture
solver.add(topic_G == SCULPT)

# Constraint 1: oil and watercolors earlier than lithographs
solver.add(pos[OIL] < pos[LITHO])
solver.add(pos[WATER] < pos[LITHO])

# Constraint 2: Farley earlier than oil paintings
solver.add(pos_F < pos[OIL])

# Constraint 3: Holden earlier than Garcia and Jiang
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Now test each option
options = [
    ("A", pos[LITHO] == 3),
    ("B", pos[OIL] == 3),
    ("C", pos[SCULPT] == 1),
    ("D", pos[SCULPT] == 2),
    ("E", pos[WATER] == 2)
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