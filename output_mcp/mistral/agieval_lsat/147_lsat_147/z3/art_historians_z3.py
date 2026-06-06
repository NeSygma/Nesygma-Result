from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare historians and topics
historians = ['Farley', 'Garcia', 'Holden', 'Jiang']
topics = ['lithographs', 'oil_paintings', 'sculptures', 'watercolors']

# Time slots: 1, 2, 3, 4 (earlier to later)
time_slots = [1, 2, 3, 4]

# Create solver
solver = Solver()

# Decision variables:
# historian_at_time[t] = historian at time t
historian_at_time = [Int(f'historian_at_time_{t}') for t in time_slots]
# topic_at_time[t] = topic at time t
topic_at_time = [Int(f'topic_at_time_{t}') for t in time_slots]

# Helper: Map historians and topics to Int values for easier constraints
historian_to_int = {h: i for i, h in enumerate(historians)}
int_to_historian = {i: h for i, h in enumerate(historians)}
topic_to_int = {t: i for i, t in enumerate(topics)}
int_to_topic = {i: t for i, t in enumerate(topics)}

# Each time slot has exactly one historian and one topic
for t in time_slots:
    solver.add(historian_at_time[t-1] >= 0, historian_at_time[t-1] < 4)
    solver.add(topic_at_time[t-1] >= 0, topic_at_time[t-1] < 4)

# All historians are distinct
solver.add(Distinct(historian_at_time))

# All topics are distinct
solver.add(Distinct(topic_at_time))

# Helper function to get time of a historian
def get_time_of_historian(h):
    for t in time_slots:
        solver.add(historian_at_time[t-1] == historian_to_int[h])
        # This is a trick; we need to encode it differently
    # Instead, we will encode constraints directly using the historian's assigned time
    pass

# Instead of helper functions, we will encode constraints directly
# Constraint: Oil paintings must be earlier than lithographs
# Find time of oil paintings and lithographs
solver.add(Or([And(topic_at_time[t-1] == topic_to_int['oil_paintings'], 
                   topic_at_time[s-1] == topic_to_int['lithographs'], 
                   t < s) for t in time_slots for s in time_slots]))

# Constraint: Watercolors must be earlier than lithographs
solver.add(Or([And(topic_at_time[t-1] == topic_to_int['watercolors'], 
                   topic_at_time[s-1] == topic_to_int['lithographs'], 
                   t < s) for t in time_slots for s in time_slots]))

# Constraint: Farley's lecture must be earlier than the oil paintings lecture
# Find time of Farley and oil paintings
solver.add(Or([And(historian_at_time[t-1] == historian_to_int['Farley'], 
                   topic_at_time[s-1] == topic_to_int['oil_paintings'], 
                   t < s) for t in time_slots for s in time_slots]))

# Constraint: Holden's lecture must be earlier than Garcia's lecture
solver.add(Or([And(historian_at_time[t-1] == historian_to_int['Holden'], 
                   historian_at_time[s-1] == historian_to_int['Garcia'], 
                   t < s) for t in time_slots for s in time_slots]))

# Constraint: Holden's lecture must be earlier than Jiang's lecture
solver.add(Or([And(historian_at_time[t-1] == historian_to_int['Holden'], 
                   historian_at_time[s-1] == historian_to_int['Jiang'], 
                   t < s) for t in time_slots for s in time_slots]))

# Base constraints are set. Now test each option.

# Option A: Farley gives the lithographs lecture
# This means at some time t, historian_at_time[t] == Farley and topic_at_time[t] == lithographs
opt_a_constr = Or([And(historian_at_time[t-1] == historian_to_int['Farley'], 
                       topic_at_time[t-1] == topic_to_int['lithographs']) for t in time_slots])

# Option B: Garcia gives the sculptures lecture
opt_b_constr = Or([And(historian_at_time[t-1] == historian_to_int['Garcia'], 
                       topic_at_time[t-1] == topic_to_int['sculptures']) for t in time_slots])

# Option C: Garcia gives the watercolors lecture
opt_c_constr = Or([And(historian_at_time[t-1] == historian_to_int['Garcia'], 
                       topic_at_time[t-1] == topic_to_int['watercolors']) for t in time_slots])

# Option D: Holden gives the oil paintings lecture
opt_d_constr = Or([And(historian_at_time[t-1] == historian_to_int['Holden'], 
                       topic_at_time[t-1] == topic_to_int['oil_paintings']) for t in time_slots])

# Option E: Jiang gives the watercolors lecture
opt_e_constr = Or([And(historian_at_time[t-1] == historian_to_int['Jiang'], 
                       topic_at_time[t-1] == topic_to_int['watercolors']) for t in time_slots])

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