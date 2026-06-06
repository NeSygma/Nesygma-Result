from z3 import *

# Mapping topics to integers
LITH = 0
OIL = 1
SCULPT = 2
WATER = 3

# Declare variables for each historian
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')

topic_F = Int('topic_F')
topic_G = Int('topic_G')
topic_H = Int('topic_H')
topic_J = Int('topic_J')

solver = Solver()
# Domain constraints
for p in [pos_F, pos_G, pos_H, pos_J]:
    solver.add(p >= 1, p <= 4)
solver.add(Distinct(pos_F, pos_G, pos_H, pos_J))

# Topic distinctness
solver.add(Distinct(topic_F, topic_G, topic_H, topic_J))
# Topics must be one of the four values
for t in [topic_F, topic_G, topic_H, topic_J]:
    solver.add(Or(t == LITH, t == OIL, t == SCULPT, t == WATER))

# Helper to get position of a given topic
# We'll encode ordering constraints using implications over all pairs

def earlier_than(topic_a, topic_b):
    # pos of historian with topic_a < pos of historian with topic_b
    return Or(
        And(topic_F == topic_a, topic_G == topic_b, pos_F < pos_G),
        And(topic_F == topic_a, topic_H == topic_b, pos_F < pos_H),
        And(topic_F == topic_a, topic_J == topic_b, pos_F < pos_J),
        And(topic_G == topic_a, topic_F == topic_b, pos_G < pos_F),
        And(topic_G == topic_a, topic_H == topic_b, pos_G < pos_H),
        And(topic_G == topic_a, topic_J == topic_b, pos_G < pos_J),
        And(topic_H == topic_a, topic_F == topic_b, pos_H < pos_F),
        And(topic_H == topic_a, topic_G == topic_b, pos_H < pos_G),
        And(topic_H == topic_a, topic_J == topic_b, pos_H < pos_J),
        And(topic_J == topic_a, topic_F == topic_b, pos_J < pos_F),
        And(topic_J == topic_a, topic_G == topic_b, pos_J < pos_G),
        And(topic_J == topic_a, topic_H == topic_b, pos_J < pos_H)
    )

# Base constraints
# oil < lith
solver.add(earlier_than(OIL, LITH))
# water < lith
solver.add(earlier_than(WATER, LITH))
# Farley earlier than oil
solver.add(Or(
    And(topic_F == OIL, pos_F < pos_F),  # impossible, placeholder
))
# Actually Farley earlier than the oil lecture (whoever has oil)
solver.add(Or(
    And(topic_F == OIL, pos_F < pos_F),  # dummy, will be overridden by proper encoding below
))
# We'll encode Farley < oil using similar pattern
solver.add(Or(
    And(topic_F == OIL, pos_F < pos_F),
    And(topic_F != OIL, Or(
        And(topic_G == OIL, pos_F < pos_G),
        And(topic_H == OIL, pos_F < pos_H),
        And(topic_J == OIL, pos_F < pos_J)
    ))
))
# Holden earlier than Garcia and Jiang
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Define option constraints
options = {}
# A: 1 Farley sculptures; 2 Holden lithographs; 3 Garcia oil; 4 Jiang water
options['A'] = [
    pos_F == 1, topic_F == SCULPT,
    pos_H == 2, topic_H == LITH,
    pos_G == 3, topic_G == OIL,
    pos_J == 4, topic_J == WATER
]
# B: 1 Farley water; 2 Jiang oil; 3 Holden sculptures; 4 Garcia lith
options['B'] = [
    pos_F == 1, topic_F == WATER,
    pos_J == 2, topic_J == OIL,
    pos_H == 3, topic_H == SCULPT,
    pos_G == 4, topic_G == LITH
]
# C: 1 Garcia sculptures; 2 Farley water; 3 Holden oil; 4 Jiang lith
options['C'] = [
    pos_G == 1, topic_G == SCULPT,
    pos_F == 2, topic_F == WATER,
    pos_H == 3, topic_H == OIL,
    pos_J == 4, topic_J == LITH
]
# D: 1 Holden oil; 2 Jiang water; 3 Farley lith; 4 Garcia sculptures
options['D'] = [
    pos_H == 1, topic_H == OIL,
    pos_J == 2, topic_J == WATER,
    pos_F == 3, topic_F == LITH,
    pos_G == 4, topic_G == SCULPT
]
# E: 1 Holden sculptures; 2 Farley water; 3 Jiang oil; 4 Garcia lith
options['E'] = [
    pos_H == 1, topic_H == SCULPT,
    pos_F == 2, topic_F == WATER,
    pos_J == 3, topic_J == OIL,
    pos_G == 4, topic_G == LITH
]

found_options = []
for letter, constrs in [("A", options['A']), ("B", options['B']), ("C", options['C']), ("D", options['D']), ("E", options['E'])]:
    solver.push()
    solver.add(constrs)
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