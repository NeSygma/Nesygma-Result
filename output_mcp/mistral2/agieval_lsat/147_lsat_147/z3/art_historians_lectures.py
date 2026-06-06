from z3 import *

# Initialize solver
solver = Solver()

# Define entities
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["Lithographs", "Oil Paintings", "Sculptures", "Watercolors"]

# Time slots: 1 (earliest) to 4 (latest)
time_slots = list(range(1, 5))

# Declare variables
historian_order = {h: Int(f"historian_order_{h}") for h in historians}
topic_order = {t: Int(f"topic_order_{t}") for t in topics}
historian_topic = {h: Int(f"historian_topic_{h}") for h in historians}
topic_historian = {t: Int(f"topic_historian_{t}") for t in topics}

# Helper: Map topics to their indices for easier handling
topic_to_idx = {t: i for i, t in enumerate(topics)}
historian_to_idx = {h: i for i, h in enumerate(historians)}

# Constraint: All historians have distinct time slots
solver.add(Distinct(list(historian_order.values())))

# Constraint: All topics have distinct time slots
solver.add(Distinct(list(topic_order.values())))

# Constraint: All historians are assigned distinct topics
solver.add(Distinct(list(historian_topic.values())))

# Constraint: All topics are assigned to distinct historians
solver.add(Distinct(list(topic_historian.values())))

# Constraint: Historian-topic assignment consistency
for h in historians:
    for t in topics:
        solver.add(historian_topic[h] == topic_to_idx[t])
        solver.add(topic_historian[t] == historian_to_idx[h])

# Constraint: Ordering constraints
solver.add(topic_order["Oil Paintings"] < topic_order["Lithographs"])
solver.add(topic_order["Watercolors"] < topic_order["Lithographs"])
solver.add(historian_order["Farley"] < topic_order["Oil Paintings"])
solver.add(historian_order["Holden"] < historian_order["Garcia"])
solver.add(historian_order["Holden"] < historian_order["Jiang"])

# Base constraints for time slots (1 to 4)
for h in historians:
    solver.add(historian_order[h] >= 1, historian_order[h] <= 4)
for t in topics:
    solver.add(topic_order[t] >= 1, topic_order[t] <= 4)

# Base constraints for topic indices (0 to 3)
for h in historians:
    solver.add(historian_topic[h] >= 0, historian_topic[h] <= 3)
for t in topics:
    solver.add(topic_historian[t] >= 0, topic_historian[t] <= 3)

# Define the options as constraints
options = {
    "A": historian_topic["Farley"] == topic_to_idx["Lithographs"],
    "B": historian_topic["Garcia"] == topic_to_idx["Sculptures"],
    "C": historian_topic["Garcia"] == topic_to_idx["Watercolors"],
    "D": historian_topic["Holden"] == topic_to_idx["Oil Paintings"],
    "E": historian_topic["Jiang"] == topic_to_idx["Watercolors"],
}

# Evaluate each option
found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")