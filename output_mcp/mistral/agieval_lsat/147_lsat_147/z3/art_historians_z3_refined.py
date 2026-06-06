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
# historian_at_time[t] = historian at time t (0-indexed for Z3)
historian_at_time = [Int(f'historian_at_time_{t}') for t in range(4)]
# topic_at_time[t] = topic at time t (0-indexed for Z3)
topic_at_time = [Int(f'topic_at_time_{t}') for t in range(4)]

# Helper: Map historians and topics to Int values for easier constraints
historian_to_int = {h: i for i, h in enumerate(historians)}
int_to_historian = {i: h for i, h in enumerate(historians)}
topic_to_int = {t: i for i, t in enumerate(topics)}
int_to_topic = {i: t for i, t in enumerate(topics)}

# Each time slot has exactly one historian and one topic
for t in range(4):
    solver.add(historian_at_time[t] >= 0, historian_at_time[t] < 4)
    solver.add(topic_at_time[t] >= 0, topic_at_time[t] < 4)

# All historians are distinct
solver.add(Distinct(historian_at_time))

# All topics are distinct
solver.add(Distinct(topic_at_time))

# Helper function to get the time index of a topic or historian
# We will encode constraints directly using the time index

# Constraint: Oil paintings must be earlier than lithographs
# Find the time index of oil_paintings and lithographs
for t in range(4):
    for s in range(4):
        if t != s:
            solver.add(Implies(topic_at_time[t] == topic_to_int['oil_paintings'], 
                               Implies(topic_at_time[s] == topic_to_int['lithographs'], 
                                       t < s)))
            solver.add(Implies(topic_at_time[t] == topic_to_int['watercolors'], 
                               Implies(topic_at_time[s] == topic_to_int['lithographs'], 
                                       t < s)))

# Constraint: Farley's lecture must be earlier than the oil paintings lecture
for t in range(4):
    for s in range(4):
        if t != s:
            solver.add(Implies(historian_at_time[t] == historian_to_int['Farley'], 
                               Implies(topic_at_time[s] == topic_to_int['oil_paintings'], 
                                       t < s)))

# Constraint: Holden's lecture must be earlier than Garcia's lecture
for t in range(4):
    for s in range(4):
        if t != s:
            solver.add(Implies(historian_at_time[t] == historian_to_int['Holden'], 
                               Implies(historian_at_time[s] == historian_to_int['Garcia'], 
                                       t < s)))

# Constraint: Holden's lecture must be earlier than Jiang's lecture
for t in range(4):
    for s in range(4):
        if t != s:
            solver.add(Implies(historian_at_time[t] == historian_to_int['Holden'], 
                               Implies(historian_at_time[s] == historian_to_int['Jiang'], 
                                       t < s)))

# Base constraints are set. Now test each option.

# Option A: Farley gives the lithographs lecture
# This means at some time t, historian_at_time[t] == Farley and topic_at_time[t] == lithographs
opt_a_constr = Or([And(historian_at_time[t] == historian_to_int['Farley'], 
                       topic_at_time[t] == topic_to_int['lithographs']) for t in range(4)])

# Option B: Garcia gives the sculptures lecture
opt_b_constr = Or([And(historian_at_time[t] == historian_to_int['Garcia'], 
                       topic_at_time[t] == topic_to_int['sculptures']) for t in range(4)])

# Option C: Garcia gives the watercolors lecture
opt_c_constr = Or([And(historian_at_time[t] == historian_to_int['Garcia'], 
                       topic_at_time[t] == topic_to_int['watercolors']) for t in range(4)])

# Option D: Holden gives the oil paintings lecture
opt_d_constr = Or([And(historian_at_time[t] == historian_to_int['Holden'], 
                       topic_at_time[t] == topic_to_int['oil_paintings']) for t in range(4)])

# Option E: Jiang gives the watercolors lecture
opt_e_constr = Or([And(historian_at_time[t] == historian_to_int['Jiang'], 
                       topic_at_time[t] == topic_to_int['watercolors']) for t in range(4)])

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