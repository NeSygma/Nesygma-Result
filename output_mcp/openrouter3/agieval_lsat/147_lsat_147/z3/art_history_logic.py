from z3 import *

# Create solver
solver = Solver()

# Define people and topics
people = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]
time_slots = [1, 2, 3, 4]

# Create variables: person_to_topic[person] = topic
person_to_topic = {p: Int(f"topic_{p}") for p in people}
# Create variables: topic_to_time[topic] = time slot
topic_to_time = {t: Int(f"time_{t}") for t in topics}

# Domain constraints: each person gets exactly one topic, each topic assigned to exactly one person
for p in people:
    solver.add(Or([person_to_topic[p] == i for i in range(4)]))
for t in topics:
    solver.add(Or([topic_to_time[t] == i for i in range(4)]))

# All people have different topics
solver.add(Distinct([person_to_topic[p] for p in people]))
# All topics have different times
solver.add(Distinct([topic_to_time[t] for t in topics]))

# Map topic names to indices for easier constraint writing
topic_indices = {t: i for i, t in enumerate(topics)}
people_indices = {p: i for i, p in enumerate(people)}

# Constraint 1: Oil paintings and watercolors must both be earlier than lithographs
solver.add(topic_to_time["oil_paintings"] < topic_to_time["lithographs"])
solver.add(topic_to_time["watercolors"] < topic_to_time["lithographs"])

# Constraint 2: Farley's lecture must be earlier than oil paintings lecture
# We need to find which topic Farley gives, then compare times
# Farley's topic time < oil paintings time
for p in people:
    if p == "Farley":
        # Farley's topic time must be less than oil paintings time
        # We need to express: time_of_topic(person_to_topic["Farley"]) < time_of_oil_paintings
        # This requires indirect constraint: for each possible topic Farley could have
        for t_idx, t in enumerate(topics):
            solver.add(Implies(person_to_topic["Farley"] == t_idx, 
                              topic_to_time[t] < topic_to_time["oil_paintings"]))

# Constraint 3: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
# Similar indirect constraint
for p in people:
    if p == "Holden":
        for t_idx, t in enumerate(topics):
            solver.add(Implies(person_to_topic["Holden"] == t_idx,
                              And(topic_to_time[t] < topic_to_time[person_to_topic["Garcia"]],
                                  topic_to_time[t] < topic_to_time[person_to_topic["Jiang"]])))

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