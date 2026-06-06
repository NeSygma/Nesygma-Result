from z3 import *

# Constants for topics
LIT = 0
OIL = 1
SCUL = 2
WATER = 3

# Historians: Farley, Garcia, Holden, Jiang
# Position variables (1..4)
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
# Topic assignment variables (0..3)
t_F = Int('t_F')
t_G = Int('t_G')
t_H = Int('t_H')
t_J = Int('t_J')

solver = Solver()
# Domain constraints
for v in [pos_F, pos_G, pos_H, pos_J]:
    solver.add(v >= 1, v <= 4)
for t in [t_F, t_G, t_H, t_J]:
    solver.add(t >= 0, t <= 3)
# All positions distinct
solver.add(Distinct(pos_F, pos_G, pos_H, pos_J))
# All topics distinct
solver.add(Distinct(t_F, t_G, t_H, t_J))

# Helper to get position of a given topic
def pos_of_topic(topic_val):
    return Sum([
        If(t_F == topic_val, pos_F, 0),
        If(t_G == topic_val, pos_G, 0),
        If(t_H == topic_val, pos_H, 0),
        If(t_J == topic_val, pos_J, 0)
    ])

pos_oil = pos_of_topic(OIL)
pos_water = pos_of_topic(WATER)
pos_lith = pos_of_topic(LIT)

# Constraints from problem
solver.add(pos_oil < pos_lith)
solver.add(pos_water < pos_lith)
solver.add(pos_F < pos_oil)  # Farley earlier than oil
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)
# Watercolors lecture is third
solver.add(pos_water == 3)

# Define option constraints
opt_a_constr = (t_F == WATER)  # Farley gives watercolors
opt_b_constr = (t_G == OIL)    # Garcia gives oil paintings
opt_c_constr = (t_G == SCUL)   # Garcia gives sculptures
opt_d_constr = (t_H == SCUL)   # Holden gives sculptures
opt_e_constr = (t_J == LIT)    # Jiang gives lithographs

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