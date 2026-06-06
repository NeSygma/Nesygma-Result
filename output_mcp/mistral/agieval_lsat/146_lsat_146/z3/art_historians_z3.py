from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare the entities
Historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
Topics = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']

# Create a solver
solver = Solver()

# Positions are 1, 2, 3, 4 (1-based)
# Declare historian and topic variables for each position
# Using IntSort for simplicity, with values mapped to indices
historian = [Int(f'historian_{i}') for i in range(1, 5)]
topic = [Int(f'topic_{i}') for i in range(1, 5)]

# Helper: Map names to indices for constraints
hist_map = {h: i for i, h in enumerate(Historians)}
topic_map = {t: i for i, t in enumerate(Topics)}

# Add constraints for distinct historians and topics
solver.add(Distinct(historian))
solver.add(Distinct(topic))

# Constraint: Watercolors is third (position 3)
solver.add(topic[2] == topic_map['watercolors'])

# Constraint: Oil paintings and watercolors must both be earlier than lithographs
# Oil paintings < lithographs
# Watercolors < lithographs (already ensured by watercolors being third and lithographs must be after third)
solver.add(topic[0] != topic_map['lithographs'])
solver.add(topic[1] != topic_map['lithographs'])
solver.add(topic[2] != topic_map['lithographs'])
# Lithographs must be at position 4 (since watercolors is 3 and lithographs must be after both oil and watercolors)
solver.add(topic[3] == topic_map['lithographs'])

# Oil paintings must be earlier than lithographs (already ensured by lithographs at 4 and oil < lithographs)
# Add constraint: oil_paintings must be at position 0, 1, or 2
solver.add(Or(topic[0] == topic_map['oil_paintings'], 
              topic[1] == topic_map['oil_paintings'], 
              topic[2] == topic_map['oil_paintings']))

# Farley's lecture must be earlier than the oil paintings lecture
# Find position of Farley and oil paintings
farley_pos = [i for i in range(4) if historian[i] == hist_map['Farley']][0]
oil_pos = [i for i in range(4) if topic[i] == topic_map['oil_paintings']][0]
solver.add(farley_pos < oil_pos)

# Holden's lecture must be earlier than both Garcia's and Jiang's lectures
# Find positions of Holden, Garcia, Jiang
holden_pos = [i for i in range(4) if historian[i] == hist_map['Holden']][0]
garcia_pos = [i for i in range(4) if historian[i] == hist_map['Garcia']][0]
jiang_pos = [i for i in range(4) if historian[i] == hist_map['Jiang']][0]
solver.add(holden_pos < garcia_pos)
solver.add(holden_pos < jiang_pos)

# Now evaluate each option
found_options = []

# Option A: Farley gives the watercolors lecture
# Watercolors is at position 3 (index 2), so Farley must be at position 3
opt_a_constr = (historian[2] == hist_map['Farley'])
solver.push()
solver.add(opt_a_constr)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Garcia gives the oil paintings lecture
# Oil paintings must be at some position before lithographs (position 4)
# Find oil paintings position
opt_b_constr = (historian[[i for i in range(4) if topic[i] == topic_map['oil_paintings']][0]] == hist_map['Garcia'])
solver.push()
solver.add(opt_b_constr)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Garcia gives the sculptures lecture
# Sculptures can be at any position except where constrained otherwise
opt_c_constr = (historian[[i for i in range(4) if topic[i] == topic_map['sculptures']][0]] == hist_map['Garcia'])
solver.push()
solver.add(opt_c_constr)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Holden gives the sculptures lecture
opt_d_constr = (historian[[i for i in range(4) if topic[i] == topic_map['sculptures']][0]] == hist_map['Holden'])
solver.push()
solver.add(opt_d_constr)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Jiang gives the lithographs lecture
# Lithographs is at position 4 (index 3)
opt_e_constr = (historian[3] == hist_map['Jiang'])
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