from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the entities
Historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
Topics = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']

# Create a solver
solver = Solver()

# Positions are 1, 2, 3, 4 (1-based)
# Declare historian_pos and topic_pos as Int variables
historian_pos = {h: Int(f'historian_pos_{h}') for h in Historians}
topic_pos = {t: Int(f'topic_pos_{t}') for t in Topics}

# Add constraints for distinct positions
solver.add(Distinct(list(historian_pos.values())))
solver.add(Distinct(list(topic_pos.values())))

# Add domain constraints (positions are 1, 2, 3, 4)
for h in Historians:
    solver.add(historian_pos[h] >= 1, historian_pos[h] <= 4)
for t in Topics:
    solver.add(topic_pos[t] >= 1, topic_pos[t] <= 4)

# Constraint: Watercolors is third (position 3)
solver.add(topic_pos['watercolors'] == 3)

# Constraint: Oil paintings and watercolors must both be earlier than lithographs
solver.add(topic_pos['oil_paintings'] < topic_pos['lithographs'])
solver.add(topic_pos['watercolors'] < topic_pos['lithographs'])

# Constraint: Farley's lecture must be earlier than the oil paintings lecture
solver.add(historian_pos['Farley'] < topic_pos['oil_paintings'])

# Constraint: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(historian_pos['Holden'] < historian_pos['Garcia'])
solver.add(historian_pos['Holden'] < historian_pos['Jiang'])

# Now evaluate each option
found_options = []

# Option A: Farley gives the watercolors lecture
# Watercolors is at position 3, so Farley must be at position 3
opt_a_constr = (historian_pos['Farley'] == 3)
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia gives the oil paintings lecture
# Oil paintings must be at some position before lithographs (which is after position 3)
# Garcia's position must equal the position of oil paintings
opt_b_constr = (historian_pos['Garcia'] == topic_pos['oil_paintings'])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Garcia gives the sculptures lecture
# Garcia's position must equal the position of sculptures
opt_c_constr = (historian_pos['Garcia'] == topic_pos['sculptures'])
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Holden gives the sculptures lecture
# Holden's position must equal the position of sculptures
opt_d_constr = (historian_pos['Holden'] == topic_pos['sculptures'])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Jiang gives the lithographs lecture
# Lithographs is after position 3, so position 4
opt_e_constr = (historian_pos['Jiang'] == topic_pos['lithographs'])
solver.push()
solver.add(opt_e_constr)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")