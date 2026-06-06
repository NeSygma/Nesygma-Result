from z3 import *

# Create solver
solver = Solver()

# Define time slots (1-4)
time_slots = [1, 2, 3, 4]

# Define people and topics
people = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]

# Create variables: person_to_time[person] = time slot when that person gives lecture
person_to_time = {p: Int(f"time_{p}") for p in people}

# Create variables: topic_to_time[topic] = time slot when that topic is lectured
topic_to_time = {t: Int(f"time_{t}") for t in topics}

# Create variables: person_gives_topic[person] = topic that person gives
# We'll use an integer encoding: 0=lithographs, 1=oil_paintings, 2=sculptures, 3=watercolors
person_gives_topic = {p: Int(f"topic_{p}") for p in people}

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

# Each person gives exactly one topic (0-3)
for p in people:
    solver.add(person_gives_topic[p] >= 0)
    solver.add(person_gives_topic[p] <= 3)
solver.add(Distinct([person_gives_topic[p] for p in people]))

# The time when a person gives a lecture equals the time when their topic is lectured
# For each person, their time equals the time of the topic they give
for p in people:
    # For each topic index, if person gives that topic, then their time equals topic's time
    constraints = []
    for topic_idx, topic in enumerate(topics):
        constraints.append(Implies(person_gives_topic[p] == topic_idx, 
                                   person_to_time[p] == topic_to_time[topic]))
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
# Option A: Farley gives the watercolors lecture (watercolors = index 3)
opt_a_constr = (person_gives_topic["Farley"] == 3)

# Option B: Garcia gives the oil paintings lecture (oil_paintings = index 1)
opt_b_constr = (person_gives_topic["Garcia"] == 1)

# Option C: Garcia gives the sculptures lecture (sculptures = index 2)
opt_c_constr = (person_gives_topic["Garcia"] == 2)

# Option D: Holden gives the sculptures lecture (sculptures = index 2)
opt_d_constr = (person_gives_topic["Holden"] == 2)

# Option E: Jiang gives the lithographs lecture (lithographs = index 0)
opt_e_constr = (person_gives_topic["Jiang"] == 0)

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