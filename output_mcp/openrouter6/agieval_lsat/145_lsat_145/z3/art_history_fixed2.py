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
        # Convert Z3 values to Python ints
        t_val = m.eval(time[i], model_completion=True)
        sol[f"time_{i}"] = int(str(t_val))  # Convert to int via string
        topic_val = m.eval(topic[i], model_completion=True)
        sol[f"topic_{i}"] = int(str(topic_val))
    solutions.append(sol)
    # Blocking clause: at least one time or topic differs
    block = []
    for i in range(4):
        block.append(time[i] != sol[f"time_{i}"])
        block.append(topic[i] != sol[f"topic_{i}"])
    solver.add(Or(block))

print(f"Total models found: {len(solutions)}")

# For each model, compute truth values
must_true = {letter: True for letter in ["A", "B", "C", "D", "E"]}
for sol in solutions:
    # Extract times
    t_F = sol["time_0"]  # Farley index 0
    t_G = sol["time_1"]  # Garcia index 1
    t_H = sol["time_2"]  # Holden index 2
    t_J = sol["time_3"]  # Jiang index 3
    # Extract topics and compute topic times
    # Build mapping from topic to time
    topic_to_time = {}
    for i in range(4):
        t = sol[f"topic_{i}"]
        topic_to_time[t] = sol[f"time_{i}"]
    # Ensure all topics present
    if len(topic_to_time) != 4:
        print("ERROR: Not all topics assigned")
        continue
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

# Now use the skeleton for multiple choice evaluation
# We'll define opt_a_constr as the statement that must be true? Actually, we'll define as the statement itself.
# But we already know which must be true. We'll just run the skeleton to satisfy the requirement.
solver2 = Solver()
# Add base constraints again
for i in range(4):
    solver2.add(time[i] >= 1, time[i] <= 4)
solver2.add(Distinct(time))
for i in range(4):
    solver2.add(topic[i] >= 0, topic[i] <= 3)
solver2.add(Distinct(topic))
solver2.add(topic_time(oil) < topic_time(lith))
solver2.add(topic_time(water) < topic_time(lith))
solver2.add(time[h_index["Farley"]] < topic_time(oil))
solver2.add(time[h_index["Holden"]] < time[h_index["Garcia"]])
solver2.add(time[h_index["Holden"]] < time[h_index["Jiang"]])

# Define option constraints
# We need to define opt_a_constr, etc. as Z3 expressions.
# For each option, we need to express it in terms of the variables.
# But we already have the statements in terms of times and topics.
# We'll define them using the same variables.
# However, note that the variables are the same as before, but we are using a new solver instance.
# We'll define the option constraints using the same time and topic variables.
# But we need to be careful: the variables are already declared, but we are using the same names.
# That's fine.

# Option A: Farley's lecture earlier than sculptures lecture
# We need to express sculptures lecture time: topic_time(t_index["sculptures"])
opt_a_constr = (time[h_index["Farley"]] < topic_time(t_index["sculptures"]))
# Option B: Holden's lecture earlier than lithographs lecture
opt_b_constr = (time[h_index["Holden"]] < topic_time(t_index["lithographs"]))
# Option C: sculptures lecture earlier than Garcia's lecture
opt_c_constr = (topic_time(t_index["sculptures"]) < time[h_index["Garcia"]])
# Option D: sculptures lecture earlier than Jiang's lecture
opt_d_constr = (topic_time(t_index["sculptures"]) < time[h_index["Jiang"]])
# Option E: watercolors lecture earlier than Garcia's lecture
opt_e_constr = (topic_time(t_index["watercolors"]) < time[h_index["Garcia"]])

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver2.push()
    solver2.add(constr)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

print(f"Found options (possible): {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")