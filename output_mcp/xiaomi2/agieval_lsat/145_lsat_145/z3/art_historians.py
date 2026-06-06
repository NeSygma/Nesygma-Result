from z3 import *

solver = Solver()

# Historians: Farley=0, Garcia=1, Holden=2, Jiang=3
# Topics: lithographs=0, oil_paintings=1, sculptures=2, watercolors=3
# Time slots: 1, 2, 3, 4

# Position of each historian's lecture (time slot)
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')

# Topic assigned to each historian
topic_F = Int('topic_F')
topic_G = Int('topic_G')
topic_H = Int('topic_H')
topic_J = Int('topic_J')

# Domain constraints: positions 1-4, topics 0-3
for p in [pos_F, pos_G, pos_H, pos_J]:
    solver.add(p >= 1, p <= 4)
for t in [topic_F, topic_G, topic_H, topic_J]:
    solver.add(t >= 0, t <= 3)

# All positions distinct, all topics distinct
solver.add(Distinct(pos_F, pos_G, pos_H, pos_J))
solver.add(Distinct(topic_F, topic_G, topic_H, topic_J))

# Position of each topic = position of the historian assigned to that topic
# Using If-chain to avoid symbolic indexing
pos_lith = If(topic_F == 0, pos_F, If(topic_G == 0, pos_G, If(topic_H == 0, pos_H, pos_J)))
pos_oil  = If(topic_F == 1, pos_F, If(topic_G == 1, pos_G, If(topic_H == 1, pos_H, pos_J)))
pos_sculp = If(topic_F == 2, pos_F, If(topic_G == 2, pos_G, If(topic_H == 2, pos_H, pos_J)))
pos_water = If(topic_F == 3, pos_F, If(topic_G == 3, pos_G, If(topic_H == 3, pos_H, pos_J)))

# Constraint 1: Oil paintings earlier than lithographs
solver.add(pos_oil < pos_lith)

# Constraint 2: Watercolors earlier than lithographs
solver.add(pos_water < pos_lith)

# Constraint 3: Farley's lecture earlier than oil paintings lecture
solver.add(pos_F < pos_oil)

# Constraint 4: Holden's lecture earlier than Garcia's lecture
solver.add(pos_H < pos_G)

# Constraint 5: Holden's lecture earlier than Jiang's lecture
solver.add(pos_H < pos_J)

# Define the options as constraints
opt_a = (pos_F < pos_sculp)       # Farley earlier than sculptures
opt_b = (pos_H < pos_lith)        # Holden earlier than lithographs
opt_c = (pos_sculp < pos_G)       # Sculptures earlier than Garcia
opt_d = (pos_sculp < pos_J)       # Sculptures earlier than Jiang
opt_e = (pos_water < pos_G)       # Watercolors earlier than Garcia

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e),
]

# For "must be true": check if NOT(option) is UNSAT with base constraints
found_options = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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