from z3 import *

# Initialize solver
solver = Solver()

# Define entities
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["Lithographs", "Oil Paintings", "Sculptures", "Watercolors"]

# Time slots: 1 (earliest) to 4 (latest)
# Each historian and topic is assigned a unique time slot

# Declare variables: historian -> time slot
historian_time = {h: Int(f"historian_time_{h}") for h in historians}
# Declare variables: topic -> time slot
topic_time = {t: Int(f"topic_time_{t}") for t in topics}

# Constraint: All historians have distinct time slots
solver.add(Distinct(list(historian_time.values())))

# Constraint: All topics have distinct time slots
solver.add(Distinct(list(topic_time.values())))

# Constraint: Oil paintings and watercolors must be earlier than lithographs
solver.add(topic_time["Oil Paintings"] < topic_time["Lithographs"])
solver.add(topic_time["Watercolors"] < topic_time["Lithographs"])

# Constraint: Farley's lecture must be earlier than the oil paintings lecture
solver.add(historian_time["Farley"] < topic_time["Oil Paintings"])

# Constraint: Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(historian_time["Holden"] < historian_time["Garcia"])
solver.add(historian_time["Holden"] < historian_time["Jiang"])

# Base constraints for time slots (1 to 4)
for h in historians:
    solver.add(historian_time[h] >= 1, historian_time[h] <= 4)
for t in topics:
    solver.add(topic_time[t] >= 1, topic_time[t] <= 4)

# Define the assignment: historian -> topic
# Use a function to map historians to topics
assignment = Function("assignment", StringSort(), StringSort(), BoolSort())

# Constraint: Each historian gives exactly one topic
for h in historians:
    solver.add(Or([assignment(h, t) for t in topics]))
    for t1 in topics:
        for t2 in topics:
            if t1 != t2:
                solver.add(Implies(assignment(h, t1), Not(assignment(h, t2))))

# Constraint: Each topic is given by exactly one historian
for t in topics:
    solver.add(Or([assignment(h, t) for h in historians]))
    for h1 in historians:
        for h2 in historians:
            if h1 != h2:
                solver.add(Implies(assignment(h1, t), Not(assignment(h2, t))))

# Constraint: Historian's time slot matches the topic's time slot if assigned
for h in historians:
    for t in topics:
        solver.add(Implies(assignment(h, t), historian_time[h] == topic_time[t]))

# Define the options as constraints
options = {
    "A": assignment("Farley", "Lithographs"),
    "B": assignment("Garcia", "Sculptures"),
    "C": assignment("Garcia", "Watercolors"),
    "D": assignment("Holden", "Oil Paintings"),
    "E": assignment("Jiang", "Watercolors"),
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