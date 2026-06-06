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
# topic_of_historian[h] = topic assigned to historian h
# We represent this as an Int with a mapping to topic indices for simplicity
topic_of_historian = {h: Int(f'topic_of_{h}') for h in historians}

# Each time slot is assigned to exactly one historian and one topic
solver.add(Distinct(list(time_of_historian.values())))
solver.add(Distinct(list(time_of_topic.values())))
for h in historians:
    solver.add(time_of_historian[h] >= 1, time_of_historian[h] <= 4)
for t in topics:
    solver.add(time_of_topic[t] >= 1, time_of_topic[t] <= 4)

# Each historian is assigned to exactly one topic, and each topic is assigned to exactly one historian
solver.add(Distinct(list(topic_of_historian.values())))
for h in historians:
    solver.add(topic_of_historian[h] >= 0, topic_of_historian[h] < 4)

# Map topic names to indices for easier constraints
topic_to_idx = {t: i for i, t in enumerate(topics)}

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

# Additional constraint: The time of a historian's lecture is the time of the topic they are assigned to
for h in historians:
    topic_idx = topic_of_historian[h]
    # Use an Or-loop to map the topic index to the actual topic time
    solver.add(Or(
        And(topic_idx == topic_to_idx['lithographs'], time_of_historian[h] == time_of_topic['lithographs']),
        And(topic_idx == topic_to_idx['oil_paintings'], time_of_historian[h] == time_of_topic['oil_paintings']),
        And(topic_idx == topic_to_idx['sculptures'], time_of_historian[h] == time_of_topic['sculptures']),
        And(topic_idx == topic_to_idx['watercolors'], time_of_historian[h] == time_of_topic['watercolors'])
    ))

# Base constraints are set. Now test each option.

# Option A: Farley gives the lithographs lecture
# This means topic_of_historian['Farley'] == topic_to_idx['lithographs']
opt_a_constr = (topic_of_historian['Farley'] == topic_to_idx['lithographs'])

# Option B: Garcia gives the sculptures lecture
opt_b_constr = (topic_of_historian['Garcia'] == topic_to_idx['sculptures'])

# Option C: Garcia gives the watercolors lecture
opt_c_constr = (topic_of_historian['Garcia'] == topic_to_idx['watercolors'])

# Option D: Holden gives the oil paintings lecture
opt_d_constr = (topic_of_historian['Holden'] == topic_to_idx['oil_paintings'])

# Option E: Jiang gives the watercolors lecture
opt_e_constr = (topic_of_historian['Jiang'] == topic_to_idx['watercolors'])

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