from z3 import *

# Create solver
solver = Solver()

# Define entities
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil", "sculptures", "watercolors"]
time_slots = [1, 2, 3, 4]  # 1 = earliest

# Create variables
# topic_of[historian] = which topic they lecture on
topic_of = {h: Int(f"topic_of_{h}") for h in historians}
# time_of[topic] = which time slot the topic is scheduled in
time_of = {t: Int(f"time_of_{t}") for t in topics}

# Domain constraints: each historian gets exactly one topic, each topic exactly one historian
# Each historian gets a topic between 0 and 3 (representing the 4 topics)
for h in historians:
    solver.add(topic_of[h] >= 0, topic_of[h] <= 3)

# Each topic gets a time slot between 1 and 4
for t in topics:
    solver.add(time_of[t] >= 1, time_of[t] <= 4)

# All historians have different topics (bijection)
historian_topics = [topic_of[h] for h in historians]
solver.add(Distinct(historian_topics))

# All topics have different times (bijection)
topic_times = [time_of[t] for t in topics]
solver.add(Distinct(topic_times))

# Map topic names to indices for easier constraint writing
topic_index = {"lithographs": 0, "oil": 1, "sculptures": 2, "watercolors": 3}

# Constraint 1: Oil paintings and watercolors must both be earlier than lithographs
solver.add(time_of["oil"] < time_of["lithographs"])
solver.add(time_of["watercolors"] < time_of["lithographs"])

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture
# Farley's lecture time = time_of[topic_of[Farley]]
# We need to express: time_of[topic_of[Farley]] < time_of["oil"]
# Since topic_of[Farley] is a Z3 variable, we need to use an Or-loop pattern
for topic_idx in range(4):
    solver.add(Implies(topic_of["Farley"] == topic_idx, 
                       time_of[topics[topic_idx]] < time_of["oil"]))

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
# Similar pattern: time_of[topic_of[Holden]] < time_of[topic_of[Garcia]] and time_of[topic_of[Holden]] < time_of[topic_of[Jiang]]
for h1_idx in range(4):  # Holden's topic
    for h2_idx in range(4):  # Garcia's topic
        for h3_idx in range(4):  # Jiang's topic
            solver.add(Implies(And(topic_of["Holden"] == h1_idx,
                                   topic_of["Garcia"] == h2_idx,
                                   topic_of["Jiang"] == h3_idx),
                               And(time_of[topics[h1_idx]] < time_of[topics[h2_idx]],
                                    time_of[topics[h1_idx]] < time_of[topics[h3_idx]])))

# Now test each answer choice using the required skeleton
found_options = []

# Option A: Farley's lecture is earlier than the sculptures lecture
opt_a_constr = Or([And(topic_of["Farley"] == topic_idx,
                       time_of[topics[topic_idx]] < time_of["sculptures"])
                   for topic_idx in range(4)])

# Option B: Holden's lecture is earlier than the lithographs lecture
opt_b_constr = Or([And(topic_of["Holden"] == topic_idx,
                       time_of[topics[topic_idx]] < time_of["lithographs"])
                   for topic_idx in range(4)])

# Option C: The sculptures lecture is earlier than Garcia's lecture
opt_c_constr = Or([And(topic_of["Garcia"] == topic_idx,
                       time_of["sculptures"] < time_of[topics[topic_idx]])
                   for topic_idx in range(4)])

# Option D: The sculptures lecture is earlier than Jiang's lecture
opt_d_constr = Or([And(topic_of["Jiang"] == topic_idx,
                       time_of["sculptures"] < time_of[topics[topic_idx]])
                   for topic_idx in range(4)])

# Option E: The watercolors lecture is earlier than Garcia's lecture
opt_e_constr = Or([And(topic_of["Garcia"] == topic_idx,
                       time_of["watercolors"] < time_of[topics[topic_idx]])
                   for topic_idx in range(4)])

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), 
                       ("C", opt_c_constr), ("D", opt_d_constr), 
                       ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results according to the required format
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")