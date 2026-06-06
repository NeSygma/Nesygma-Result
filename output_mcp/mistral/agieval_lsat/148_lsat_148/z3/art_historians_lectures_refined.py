from z3 import *

# BENCHMARK_MODE: ON (model-finding with single correct answer)
BENCHMARK_MODE = True

# Declare entities
Historians = ["Farley", "Garcia", "Holden", "Jiang"]
Topics = ["lithographs", "oil_paintings", "sculptures", "watercolors"]

# Create a solver
solver = Solver()

# Position of each historian (1 to 4)
h_pos = {h: Int(f"hpos_{h}") for h in Historians}

# Position of each topic (1 to 4)
t_pos = {t: Int(f"tpos_{t}") for t in Topics}

# Assignment of topics to historians: topic_of[h] = t means historian h gives topic t
topic_of = {h: String(f"topic_{h}") for h in Historians}

# All historian positions are distinct
solver.add(Distinct(list(h_pos.values())))

# All topic positions are distinct
solver.add(Distinct(list(t_pos.values())))

# All topics are assigned and distinct
solver.add(Distinct(list(topic_of.values())))

# Each historian's position matches the position of their assigned topic
for h in Historians:
    for t in Topics:
        solver.add(Implies(topic_of[h] == t, h_pos[h] == t_pos[t]))

# Constraints from the problem statement
# 1. Oil paintings and watercolors must both be earlier than lithographs
solver.add(t_pos["oil_paintings"] < t_pos["lithographs"])
solver.add(t_pos["watercolors"] < t_pos["lithographs"])

# 2. Farley's lecture must be earlier than the oil paintings lecture
solver.add(h_pos["Farley"] < t_pos["oil_paintings"])

# 3. Holden's lecture must be earlier than both Garcia's and Jiang's lectures
solver.add(h_pos["Holden"] < h_pos["Garcia"])
solver.add(h_pos["Holden"] < h_pos["Jiang"])

# Additional condition: Garcia gives the sculptures lecture
solver.add(topic_of["Garcia"] == "sculptures")

# Helper function to check satisfiability of an option
def check_option(letter, constraint):
    solver.push()
    solver.add(constraint)
    result = solver.check()
    solver.pop()
    return result == sat

# Define the options as constraints on topic positions
# (A) The lithographs lecture is third
opt_a_constr = (t_pos["lithographs"] == 3)

# (B) The oil paintings lecture is third
opt_b_constr = (t_pos["oil_paintings"] == 3)

# (C) The sculptures lecture is first
opt_c_constr = (t_pos["sculptures"] == 1)

# (D) The sculptures lecture is second
opt_d_constr = (t_pos["sculptures"] == 2)

# (E) The watercolors lecture is second
opt_e_constr = (t_pos["watercolors"] == 2)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    if check_option(letter, constr):
        found_options.append(letter)

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