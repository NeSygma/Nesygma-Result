from z3 import *

# Create solver
solver = Solver()

# Define entities and topics
historians = ["Farley", "Garcia", "Holden", "Jiang"]
topics = ["lithographs", "oil paintings", "sculptures", "watercolors"]

# Create position variables for each historian (1-4)
pos = {h: Int(f"pos_{h}") for h in historians}

# Create topic variables for each historian
topic = {h: Int(f"topic_{h}") for h in historians}

# Base constraints: each historian gets a unique position (1-4)
for h in historians:
    solver.add(pos[h] >= 1, pos[h] <= 4)
solver.add(Distinct([pos[h] for h in historians]))

# Base constraints: each historian gets a unique topic
for h in historians:
    solver.add(topic[h] >= 0, topic[h] <= 3)  # 0=lithographs, 1=oil paintings, 2=sculptures, 3=watercolors
solver.add(Distinct([topic[h] for h in historians]))

# Topic mapping for readability
LITHOGRAPHS, OIL_PAINTINGS, SCULPTURES, WATERCOLORS = 0, 1, 2, 3

# Constraint 1: The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
# This means: position(oil paintings) < position(lithographs) AND position(watercolors) < position(lithographs)
# We need to find which historian gives oil paintings and which gives watercolors
oil_historian = Int('oil_historian')
water_historian = Int('water_historian')
litho_historian = Int('litho_historian')

# Oil historian constraint
solver.add(Or([oil_historian == i for i in range(4)]))
solver.add(Or([And(oil_historian == i, topic[historians[i]] == OIL_PAINTINGS) for i in range(4)]))

# Water historian constraint  
solver.add(Or([water_historian == i for i in range(4)]))
solver.add(Or([And(water_historian == i, topic[historians[i]] == WATERCOLORS) for i in range(4)]))

# Litho historian constraint
solver.add(Or([litho_historian == i for i in range(4)]))
solver.add(Or([And(litho_historian == i, topic[historians[i]] == LITHOGRAPHS) for i in range(4)]))

# All three must be different
solver.add(Distinct([oil_historian, water_historian, litho_historian]))

# Position constraints for constraint 1
solver.add(pos[historians[oil_historian]] < pos[historians[litho_historian]])
solver.add(pos[historians[water_historian]] < pos[historians[litho_historian]])

# Constraint 2: Farley's lecture must be earlier than the oil paintings lecture
solver.add(pos["Farley"] < pos[historians[oil_historian]])

# Constraint 3: Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture
solver.add(pos["Holden"] < pos["Garcia"])
solver.add(pos["Holden"] < pos["Jiang"])

# Now test each answer choice
found_options = []

# Option A: Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
opt_a = And(
    topic["Farley"] == SCULPTURES,
    topic["Holden"] == LITHOGRAPHS,
    topic["Garcia"] == OIL_PAINTINGS,
    topic["Jiang"] == WATERCOLORS,
    pos["Farley"] < pos["Holden"],  # Farley first
    pos["Holden"] < pos["Garcia"],  # Holden second
    pos["Garcia"] < pos["Jiang"]    # Garcia third, Jiang fourth
)

# Option B: Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
opt_b = And(
    topic["Farley"] == WATERCOLORS,
    topic["Jiang"] == OIL_PAINTINGS,
    topic["Holden"] == SCULPTURES,
    topic["Garcia"] == LITHOGRAPHS,
    pos["Farley"] < pos["Jiang"],
    pos["Jiang"] < pos["Holden"],
    pos["Holden"] < pos["Garcia"]
)

# Option C: Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
opt_c = And(
    topic["Garcia"] == SCULPTURES,
    topic["Farley"] == WATERCOLORS,
    topic["Holden"] == OIL_PAINTINGS,
    topic["Jiang"] == LITHOGRAPHS,
    pos["Garcia"] < pos["Farley"],
    pos["Farley"] < pos["Holden"],
    pos["Holden"] < pos["Jiang"]
)

# Option D: Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
opt_d = And(
    topic["Holden"] == OIL_PAINTINGS,
    topic["Jiang"] == WATERCOLORS,
    topic["Farley"] == LITHOGRAPHS,
    topic["Garcia"] == SCULPTURES,
    pos["Holden"] < pos["Jiang"],
    pos["Jiang"] < pos["Farley"],
    pos["Farley"] < pos["Garcia"]
)

# Option E: Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs
opt_e = And(
    topic["Holden"] == SCULPTURES,
    topic["Farley"] == WATERCOLORS,
    topic["Jiang"] == OIL_PAINTINGS,
    topic["Garcia"] == LITHOGRAPHS,
    pos["Holden"] < pos["Farley"],
    pos["Farley"] < pos["Jiang"],
    pos["Jiang"] < pos["Garcia"]
)

# Test each option
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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