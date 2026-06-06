from z3 import *

solver = Solver()

# Names and indices
hist_names = ['Farley','Garcia','Holden','Jiang']
topic_names = ['lithographs','oil','sculptures','watercolors']

# Indices
Farley_index, Garcia_index, Holden_index, Jiang_index = 0,1,2,3
lith_index, oil_index, sculpture_index, water_index = 0,1,2,3

# Variables
hist_topic = [Int(f"hist_topic_{name}") for name in hist_names]
# hist_topic[i] is the topic index (0-3) given by historian i

topic_pos = [Int(f"topic_pos_{name}") for name in topic_names]
# topic_pos[j] is the position (1-4) of topic j

hist_pos = [Int(f"hist_pos_{name}") for name in hist_names]
# hist_pos[i] is the position (1-4) of historian i's lecture

# Domain constraints
solver.add(And([hist_topic[i] >= 0, hist_topic[i] <= 3] for i in range(4)))
solver.add(And([topic_pos[j] >= 1, topic_pos[j] <= 4] for j in range(4)))
solver.add(And([hist_pos[i] >= 1, hist_pos[i] <= 4] for i in range(4)))

# Distinctness constraints
solver.add(Distinct(hist_topic))
solver.add(Distinct(topic_pos))
solver.add(Distinct(hist_pos))

# Mapping between historian position and topic position
for i in range(4):
    solver.add(hist_pos[i] == topic_pos[ hist_topic[i] ])

# Constraints from problem statement
# Oil and watercolors earlier than lithographs
solver.add(topic_pos[oil_index] < topic_pos[lith_index])
solver.add(topic_pos[water_index] < topic_pos[lith_index])

# Farley's lecture earlier than oil paintings
solver.add(hist_pos[Farley_index] < topic_pos[oil_index])

# Holden earlier than Garcia and Jiang
solver.add(hist_pos[Holden_index] < hist_pos[Garcia_index])
solver.add(hist_pos[Holden_index] < hist_pos[Jiang_index])

# Watercolors lecture is third
solver.add(topic_pos[water_index] == 3)

# Option constraints
opt_a_constr = hist_topic[Farley_index] == water_index
opt_b_constr = hist_topic[Garcia_index] == oil_index
opt_c_constr = hist_topic[Garcia_index] == sculpture_index
opt_d_constr = hist_topic[Holden_index] == sculpture_index
opt_e_constr = hist_topic[Jiang_index] == lith_index

# Evaluate options
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