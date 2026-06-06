from z3 import *

solver = Solver()
# Historians
hist = ['F', 'G', 'Ho', 'J']
# Position variables
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_Ho = Int('pos_Ho')
pos_J = Int('pos_J')
positions = [pos_F, pos_G, pos_Ho, pos_J]
for p in positions:
    solver.add(p >= 1, p <= 4)
solver.add(Distinct(*positions))
# Topic variables: 0 lithographs,1 oil,2 sculptures,3 watercolors
topic_F = Int('topic_F')
topic_G = Int('topic_G')
topic_Ho = Int('topic_Ho')
topic_J = Int('topic_J')
topics = [topic_F, topic_G, topic_Ho, topic_J]
for t in topics:
    solver.add(t >= 0, t <= 3)
solver.add(Distinct(*topics))
# Helper to get position of a given topic index
def pos_of_topic(idx):
    return Sum([
        If(topic_F == idx, pos_F, 0),
        If(topic_G == idx, pos_G, 0),
        If(topic_Ho == idx, pos_Ho, 0),
        If(topic_J == idx, pos_J, 0)
    ])
# Topic indices
LITH = 0
OIL = 1
SCUL = 2
WATER = 3
pos_lith = pos_of_topic(LITH)
pos_oil = pos_of_topic(OIL)
pos_scul = pos_of_topic(SCUL)
pos_water = pos_of_topic(WATER)
# Base constraints
solver.add(pos_oil < pos_lith)
solver.add(pos_water < pos_lith)
solver.add(pos_F < pos_oil)
solver.add(pos_Ho < pos_G)
solver.add(pos_Ho < pos_J)
# Option constraints
opt_a = pos_F < pos_scul
opt_b = pos_Ho < pos_lith
opt_c = pos_scul < pos_G
opt_d = pos_scul < pos_J
opt_e = pos_water < pos_G
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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