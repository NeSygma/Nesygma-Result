from z3 import *

# Create solver
solver = Solver()

# Define people and topics
people = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]

# Create variables: person_to_topic[person] = topic index (0-3)
person_to_topic = {p: Int(f"topic_{p}") for p in people}

# Create a Z3 Array for topic_to_time: topic index -> time slot (1-4)
topic_to_time = Array('topic_to_time', IntSort(), IntSort())

# Domain constraints: each person gets exactly one topic (0-3)
for p in people:
    solver.add(Or([person_to_topic[p] == i for i in range(4)]))

# All people have different topics
solver.add(Distinct([person_to_topic[p] for p in people]))

# Each topic gets exactly one time slot (1-4)
# We'll use a different approach: create time variables for each topic index
time_for_topic = [Int(f"time_{i}") for i in range(4)]
for i in range(4):
    solver.add(Or([time_for_topic[i] == j for j in range(1, 5)]))
solver.add(Distinct(time_for_topic))

# Map topic names to indices
topic_indices = {t: i for i, t in enumerate(topics)}

# Constraint 1: Oil paintings and watercolors must both be earlier than lithographs
solver.add(time_for_topic[topic_indices["oil_paintings"]] < time_for_topic[topic_indices["lithographs"]])
solver.add(time_for_topic[topic_indices["watercolors"]] < time_for_topic[topic_indices["lithographs"]])

# Constraint 2: Farley's lecture must be earlier than oil paintings lecture
# For each possible topic Farley could have, if he has that topic, then that topic's time < oil paintings time
for t_idx in range(4):
    solver.add(Implies(person_to_topic["Farley"] == t_idx,
                      time_for_topic[t_idx] < time_for_topic[topic_indices["oil_paintings"]]))

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
# We need to find which topic Holden has, and which topics Garcia and Jiang have
# Use Or-Loop pattern to avoid symbolic indexing
for h_idx in range(4):  # Holden's topic
    for g_idx in range(4):  # Garcia's topic
        for j_idx in range(4):  # Jiang's topic
            solver.add(Implies(
                And(person_to_topic["Holden"] == h_idx,
                    person_to_topic["Garcia"] == g_idx,
                    person_to_topic["Jiang"] == j_idx),
                And(time_for_topic[h_idx] < time_for_topic[g_idx],
                    time_for_topic[h_idx] < time_for_topic[j_idx])
            ))

# Now test each option
# Option A: Farley gives the lithographs lecture
opt_a_constr = (person_to_topic["Farley"] == topic_indices["lithographs"])

# Option B: Garcia gives the sculptures lecture
opt_b_constr = (person_to_topic["Garcia"] == topic_indices["sculptures"])

# Option C: Garcia gives the watercolors lecture
opt_c_constr = (person_to_topic["Garcia"] == topic_indices["watercolors"])

# Option D: Holden gives the oil paintings lecture
opt_d_constr = (person_to_topic["Holden"] == topic_indices["oil_paintings"])

# Option E: Jiang gives the watercolors lecture
opt_e_constr = (person_to_topic["Jiang"] == topic_indices["watercolors"])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                      ("D", opt_d_constr), ("E", opt_e_constr)]:
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