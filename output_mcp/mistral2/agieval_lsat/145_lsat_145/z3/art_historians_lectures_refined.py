from z3 import *

solver = Solver()

# Encode topics as integers for easier handling
topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]
topic_to_int = {t: i for i, t in enumerate(topics)}

# Artists
artists = ["Farley", "Garcia", "Holden", "Jiang"]

# Assign a position (1-4) to each artist and topic
artist_pos = {a: Int(f"artist_pos_{a}") for a in artists}
topic_pos = {t: Int(f"topic_pos_{t}") for t in topics}

# Each artist and topic must be assigned to a unique position
solver.add(Distinct(list(artist_pos.values())))
solver.add(Distinct(list(topic_pos.values())))

# Constraints from the problem statement
# 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
solver.add(topic_pos["oil_paintings"] < topic_pos["lithographs"])
solver.add(topic_pos["watercolors"] < topic_pos["lithographs"])

# 2. Farley's lecture must be earlier than the oil paintings lecture.
solver.add(artist_pos["Farley"] < topic_pos["oil_paintings"])

# 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
solver.add(artist_pos["Holden"] < artist_pos["Garcia"])
solver.add(artist_pos["Holden"] < artist_pos["Jiang"])

# Link artists to topics: artist_topic[a] = topic assigned to artist a
artist_topic = {a: Int(f"artist_topic_{a}") for a in artists}
for a in artists:
    solver.add(artist_topic[a] >= 0, artist_topic[a] < 4)

# Each artist is assigned to a unique topic
solver.add(Distinct(list(artist_topic.values())))

# The position of an artist's lecture is the same as the position of the topic they are assigned to
for a in artists:
    for t in topics:
        solver.add(If(artist_topic[a] == topic_to_int[t], artist_pos[a] == topic_pos[t], True))

# Now, evaluate the multiple choice options

# Option A: Farley's lecture is earlier than the sculptures lecture.
opt_a_constr = (artist_pos["Farley"] < topic_pos["sculptures"])

# Option B: Holden's lecture is earlier than the lithographs lecture.
opt_b_constr = (artist_pos["Holden"] < topic_pos["lithographs"])

# Option C: The sculptures lecture is earlier than Garcia's lecture.
opt_c_constr = (topic_pos["sculptures"] < artist_pos["Garcia"])

# Option D: The sculptures lecture is earlier than Jiang's lecture.
opt_d_constr = (topic_pos["sculptures"] < artist_pos["Jiang"])

# Option E: The watercolors lecture is earlier than Garcia's lecture.
opt_e_constr = (topic_pos["watercolors"] < artist_pos["Garcia"])

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