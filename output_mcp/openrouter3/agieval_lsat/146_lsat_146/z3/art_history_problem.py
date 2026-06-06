from z3 import *

# Create solver
solver = Solver()

# Define time slots (1-4)
time_slots = [1, 2, 3, 4]

# Define people and topics
people = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]

# Create variables: person_to_time[person] = time slot when that person gives lecture
# and topic_to_time[topic] = time slot when that topic is lectured
person_to_time = {p: Int(f"time_{p}") for p in people}
topic_to_time = {t: Int(f"time_{t}") for t in topics}

# Each person gives exactly one lecture at a unique time
for p in people:
    solver.add(person_to_time[p] >= 1)
    solver.add(person_to_time[p] <= 4)
solver.add(Distinct([person_to_time[p] for p in people]))

# Each topic is lectured at exactly one unique time
for t in topics:
    solver.add(topic_to_time[t] >= 1)
    solver.add(topic_to_time[t] <= 4)
solver.add(Distinct([topic_to_time[t] for t in topics]))

# Each person gives exactly one topic (bijection between people and topics)
# We need to ensure that each person is assigned to exactly one topic
# and each topic is assigned to exactly one person
# We'll create assignment variables: person_topic[p] = topic that person p lectures on
person_topic = {}
for p in people:
    # Create a variable for each person's topic
    person_topic[p] = Int(f"topic_{p}")
    solver.add(person_topic[p] >= 0)
    solver.add(person_topic[p] <= 3)  # 4 topics indexed 0-3

# Map topic names to indices for easier constraint writing
topic_index = {"lithographs": 0, "oil_paintings": 1, "sculptures": 2, "watercolors": 3}

# Each person gives a different topic
solver.add(Distinct([person_topic[p] for p in people]))

# The time when a person gives a lecture equals the time when their topic is lectured
for p in people:
    # For each topic, if person p is giving that topic, then person's time = topic's time
    constraints = []
    for t in topics:
        t_idx = topic_index[t]
        constraints.append(Implies(person_topic[p] == t_idx, person_to_time[p] == topic_to_time[t]))
    solver.add(Or(constraints))

# Constraint: watercolors lecture is third
solver.add(topic_to_time["watercolors"] == 3)

# Constraint 1: oil paintings and watercolors must both be earlier than lithographs
solver.add(topic_to_time["oil_paintings"] < topic_to_time["lithographs"])
solver.add(topic_to_time["watercolors"] < topic_to_time["lithographs"])

# Constraint 2: Farley's lecture must be earlier than oil paintings lecture
solver.add(person_to_time["Farley"] < topic_to_time["oil_paintings"])

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(person_to_time["Holden"] < person_to_time["Garcia"])
solver.add(person_to_time["Holden"] < person_to_time["Jiang"])

# Now evaluate each option
# Option A: Farley gives the watercolors lecture
opt_a_constr = (person_topic["Farley"] == topic_index["watercolors"])

# Option B: Garcia gives the oil paintings lecture
opt_b_constr = (person_topic["Garcia"] == topic_index["oil_paintings"])

# Option C: Garcia gives the sculptures lecture
opt_c_constr = (person_topic["Garcia"] == topic_index["sculptures"])

# Option D: Holden gives the sculptures lecture
opt_d_constr = (person_topic["Holden"] == topic_index["sculptures"])

# Option E: Jiang gives the lithographs lecture
opt_e_constr = (person_topic["Jiang"] == topic_index["lithographs"])

# Test each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")