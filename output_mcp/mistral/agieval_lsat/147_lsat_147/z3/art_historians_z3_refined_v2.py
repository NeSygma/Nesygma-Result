from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare historians and topics
historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
topics = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']

# Create solver
solver = Solver()

# Decision variables:
# time_of_historian[h] = time slot (1-4) for historian h
time_of_historian = {h: Int(f'time_of_{h}') for h in historians}
# time_of_topic[t] = time slot (1-4) for topic t
time_of_topic = {t: Int(f'time_of_{t}') for t in topics}

# Each time slot is assigned to exactly one historian and one topic
# We enforce this by ensuring all time_of_historian and time_of_topic values are distinct and in 1..4
solver.add(Distinct(list(time_of_historian.values())))
solver.add(Distinct(list(time_of_topic.values())))
for h in historians:
    solver.add(time_of_historian[h] >= 1, time_of_historian[h] <= 4)
for t in topics:
    solver.add(time_of_topic[t] >= 1, time_of_topic[t] <= 4)

# Constraint: Oil paintings must be earlier than lithographs
oil_time = time_of_topic['oil_paintings']
lith_time = time_of_topic['lithographs']
solver.add(oil_time < lith_time)

# Constraint: Watercolors must be earlier than lithographs
water_time = time_of_topic['watercolors']
solver.add(water_time < lith_time)

# Constraint: Farley's lecture must be earlier than the oil paintings lecture
farley_time = time_of_historian['Farley']
solver.add(farley_time < oil_time)

# Constraint: Holden's lecture must be earlier than Garcia's lecture
holden_time = time_of_historian['Holden']
garcia_time = time_of_historian['Garcia']
solver.add(holden_time < garcia_time)

# Constraint: Holden's lecture must be earlier than Jiang's lecture
jiang_time = time_of_historian['Jiang']
solver.add(holden_time < jiang_time)

# Base constraints are set. Now test each option.

# Option A: Farley gives the lithographs lecture
# This means time_of_historian['Farley'] == time_of_topic['lithographs']
opt_a_constr = (time_of_historian['Farley'] == time_of_topic['lithographs'])

# Option B: Garcia gives the sculptures lecture
opt_b_constr = (time_of_historian['Garcia'] == time_of_topic['sculptures'])

# Option C: Garcia gives the watercolors lecture
opt_c_constr = (time_of_historian['Garcia'] == time_of_topic['watercolors'])

# Option D: Holden gives the oil paintings lecture
opt_d_constr = (time_of_historian['Holden'] == time_of_topic['oil_paintings'])

# Option E: Jiang gives the watercolors lecture
opt_e_constr = (time_of_historian['Jiang'] == time_of_topic['watercolors'])

# Test each option
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