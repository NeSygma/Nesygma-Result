from z3 import *

# Define historians and topics
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil", "sculptures", "watercolors"]
# Map names to indices
h_index = {name: i for i, name in enumerate(historians)}
t_index = {name: i for i, name in enumerate(topics)}

# Variables: time slot for each historian (1..4)
time = [Int(f"time_{i}") for i in range(4)]
# Variables: topic assigned to each historian (0..3)
topic = [Int(f"topic_{i}") for i in range(4)]

solver = Solver()

# All times distinct and in 1..4
for i in range(4):
    solver.add(time[i] >= 1, time[i] <= 4)
solver.add(Distinct(time))

# All topics distinct and in 0..3
for i in range(4):
    solver.add(topic[i] >= 0, topic[i] <= 3)
solver.add(Distinct(topic))

# Function to get time of a topic
def topic_time(t):
    # Sum of time[i] where topic[i] == t, exactly one will be non-zero
    return Sum([If(topic[i] == t, time[i], 0) for i in range(4)])

# Constraint 1: oil and watercolors earlier than lithographs
oil = t_index["oil"]
lith = t_index["lithographs"]
water = t_index["watercolors"]
solver.add(topic_time(oil) < topic_time(lith))
solver.add(topic_time(water) < topic_time(lith))

# Constraint 2: Farley earlier than oil
solver.add(time[h_index["Farley"]] < topic_time(oil))

# Constraint 3: Holden earlier than Garcia and Jiang
solver.add(time[h_index["Holden"]] < time[h_index["Garcia"]])
solver.add(time[h_index["Holden"]] < time[h_index["Jiang"]])

# Now enumerate all models
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {}
    for i in range(4):
        sol[f"time_{i}"] = m.eval(time[i], model_completion=True)
        sol[f"topic_{i}"] = m.eval(topic[i], model_completion=True)
    solutions.append(sol)
    # Blocking clause: at least one time or topic differs
    block = []
    for i in range(4):
        block.append(time[i] != sol[f"time_{i}"])
        block.append(topic[i] != sol[f"topic_{i}"])
    solver.add(Or(block))

print(f"Total models found: {len(solutions)}")

# Evaluate each option across all models
options = {
    "A": "Farley's lecture is earlier than the sculptures lecture.",
    "B": "Holden's lecture is earlier than the lithographs lecture.",
    "C": "The sculptures lecture is earlier than Garcia's lecture.",
    "D": "The sculptures lecture is earlier than Jiang's lecture.",
    "E": "The watercolors lecture is earlier than Garcia's lecture."
}

# For each model, compute truth values
must_true = {letter: True for letter in options}
for sol in solutions:
    # Extract times
    t_F = sol["time_0"]  # Farley index 0
    t_G = sol["time_1"]  # Garcia index 1
    t_H = sol["time_2"]  # Holden index 2
    t_J = sol["time_3"]  # Jiang index 3
    # Extract topics and compute topic times
    # topic[i] is integer 0..3
    # We need to find which historian has which topic
    # Build mapping from topic to time
    topic_to_time = {}
    for i in range(4):
        t = sol[f"topic_{i}"]
        topic_to_time[t] = sol[f"time_{i}"]
    t_lith = topic_to_time[t_index["lithographs"]]
    t_oil = topic_to_time[t_index["oil"]]
    t_sculpt = topic_to_time[t_index["sculptures"]]
    t_water = topic_to_time[t_index["watercolors"]]
    
    # Evaluate each option
    # A: Farley's lecture earlier than sculptures lecture
    A = (t_F < t_sculpt)
    # B: Holden's lecture earlier than lithographs lecture
    B = (t_H < t_lith)
    # C: sculptures lecture earlier than Garcia's lecture
    C = (t_sculpt < t_G)
    # D: sculptures lecture earlier than Jiang's lecture
    D = (t_sculpt < t_J)
    # E: watercolors lecture earlier than Garcia's lecture
    E = (t_water < t_G)
    
    # Update must_true
    if not A: must_true["A"] = False
    if not B: must_true["B"] = False
    if not C: must_true["C"] = False
    if not D: must_true["D"] = False
    if not E: must_true["E"] = False

# Determine which options must be true
must_true_list = [letter for letter, val in must_true.items() if val]
print(f"Options that must be true: {must_true_list}")

if len(must_true_list) == 1:
    print("STATUS: sat")
    print(f"answer:{must_true_list[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Expected exactly one must-true option, found {must_true_list}")