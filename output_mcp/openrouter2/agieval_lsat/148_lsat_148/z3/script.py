from z3 import *

solver = Solver()

# Historians and topics
historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
topics = ['lithographs', 'oil', 'sculptures', 'water']

# Variables
historian_topic = {h: Int(f"topic_{h}") for h in historians}
historian_pos   = {h: Int(f"pos_{h}")   for h in historians}
topic_pos       = {t: Int(f"pos_{t}")   for t in topics}

# Domain constraints
for h in historians:
    solver.add(historian_topic[h] >= 0, historian_topic[h] <= 3)
    solver.add(historian_pos[h]   >= 1, historian_pos[h]   <= 4)
for t in topics:
    solver.add(topic_pos[t] >= 1, topic_pos[t] <= 4)

# Distinctness
solver.add(Distinct([historian_topic[h] for h in historians]))
solver.add(Distinct([historian_pos[h]   for h in historians]))

# Mapping between historian's topic and topic position
for h in historians:
    solver.add(Or([And(historian_topic[h] == i, topic_pos[topics[i]] == historian_pos[h]) for i in range(4)]))

# Base constraints
# 1. Oil paintings (topic[1]) and watercolors (topic[3]) earlier than lithographs (topic[0])
solver.add(topic_pos['oil'] < topic_pos['lithographs'])
solver.add(topic_pos['water'] < topic_pos['lithographs'])
# 2. Farley's lecture earlier than oil paintings
solver.add(historian_pos['Farley'] < topic_pos['oil'])
# 3. Holden earlier than both Garcia and Jiang
solver.add(historian_pos['Holden'] < historian_pos['Garcia'])
solver.add(historian_pos['Holden'] < historian_pos['Jiang'])
# 4. Garcia gives sculptures
solver.add(historian_topic['Garcia'] == 2)  # sculptures index 2

# Option constraints
opt_a_constr = topic_pos['lithographs'] == 3
opt_b_constr = topic_pos['oil'] == 3
opt_c_constr = topic_pos['sculptures'] == 1
opt_d_constr = topic_pos['sculptures'] == 2
opt_e_constr = topic_pos['water'] == 2

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