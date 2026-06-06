from z3 import *

solver = Solver()

# Historians and topics
historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
# Topic mapping: lithographs=0, oil paintings=1, sculptures=2, watercolors=3
topic_map = {'lithographs':0, 'oil paintings':1, 'sculptures':2, 'watercolors':3}

# Variables for positions and topics
pos = {h: Int(f'pos_{h}') for h in historians}
topic = {h: Int(f'topic_{h}') for h in historians}

# Position bounds and distinctness
for h in historians:
    solver.add(pos[h] >= 1, pos[h] <= 4)
solver.add(Distinct([pos[h] for h in historians]))

# Topic bounds and distinctness
for h in historians:
    solver.add(topic[h] >= 0, topic[h] <= 3)
solver.add(Distinct([topic[h] for h in historians]))

# Variables for topic positions
pos_litho, pos_oil, pos_water, pos_sculpture = Ints('pos_litho pos_oil pos_water pos_sculpture')
for p in [pos_litho, pos_oil, pos_water, pos_sculpture]:
    solver.add(p >= 1, p <= 4)

# Link topic positions to historian positions
for h in historians:
    solver.add(Implies(topic[h] == topic_map['lithographs'], pos_litho == pos[h]))
    solver.add(Implies(topic[h] == topic_map['oil paintings'], pos_oil == pos[h]))
    solver.add(Implies(topic[h] == topic_map['watercolors'], pos_water == pos[h]))
    solver.add(Implies(topic[h] == topic_map['sculptures'], pos_sculpture == pos[h]))

# Ordering constraints
solver.add(pos_oil < pos_litho)
solver.add(pos_water < pos_litho)
solver.add(pos['Farley'] < pos_oil)
solver.add(pos['Holden'] < pos['Garcia'])
solver.add(pos['Holden'] < pos['Jiang'])

# Option constraints
opt_a_constr = And(
    pos['Farley'] == 1, topic['Farley'] == topic_map['sculptures'],
    pos['Holden'] == 2, topic['Holden'] == topic_map['lithographs'],
    pos['Garcia'] == 3, topic['Garcia'] == topic_map['oil paintings'],
    pos['Jiang'] == 4, topic['Jiang'] == topic_map['watercolors']
)
opt_b_constr = And(
    pos['Farley'] == 1, topic['Farley'] == topic_map['watercolors'],
    pos['Jiang'] == 2, topic['Jiang'] == topic_map['oil paintings'],
    pos['Holden'] == 3, topic['Holden'] == topic_map['sculptures'],
    pos['Garcia'] == 4, topic['Garcia'] == topic_map['lithographs']
)
opt_c_constr = And(
    pos['Garcia'] == 1, topic['Garcia'] == topic_map['sculptures'],
    pos['Farley'] == 2, topic['Farley'] == topic_map['watercolors'],
    pos['Holden'] == 3, topic['Holden'] == topic_map['oil paintings'],
    pos['Jiang'] == 4, topic['Jiang'] == topic_map['lithographs']
)
opt_d_constr = And(
    pos['Holden'] == 1, topic['Holden'] == topic_map['oil paintings'],
    pos['Jiang'] == 2, topic['Jiang'] == topic_map['watercolors'],
    pos['Farley'] == 3, topic['Farley'] == topic_map['lithographs'],
    pos['Garcia'] == 4, topic['Garcia'] == topic_map['sculptures']
)
opt_e_constr = And(
    pos['Holden'] == 1, topic['Holden'] == topic_map['sculptures'],
    pos['Farley'] == 2, topic['Farley'] == topic_map['watercolors'],
    pos['Jiang'] == 3, topic['Jiang'] == topic_map['oil paintings'],
    pos['Garcia'] == 4, topic['Garcia'] == topic_map['lithographs']
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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