from z3 import *

solver = Solver()

# Declare position variables for each accomplice
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]
pos = {name: Int(f"pos_{name}") for name in names}

# Base constraints from the problem
# 1. Stanton and Tao are not adjacent (neither immediately before nor after)
solver.add(Or(pos["Stanton"] != pos["Tao"] + 1, pos["Stanton"] != pos["Tao"] - 1))
# Actually, we need to ensure the absolute difference is not 1.
# We can do: |pos_Stanton - pos_Tao| != 1
solver.add(Abs(pos["Stanton"] - pos["Tao"]) != 1)

# 2. Quinn earlier than Rovero
solver.add(pos["Quinn"] < pos["Rovero"])

# 3. Villas immediately before White
solver.add(pos["Villas"] + 1 == pos["White"])

# 4. Peters is fourth
solver.add(pos["Peters"] == 4)

# All positions are between 1 and 7 and distinct
for name in names:
    solver.add(pos[name] >= 1, pos[name] <= 7)
solver.add(Distinct([pos[name] for name in names]))

# Define the options
options = [
    ("A", ["Quinn", "Tao", "Stanton", "Peters", "Villas", "White", "Rovero"]),
    ("B", ["Quinn", "White", "Rovero", "Peters", "Stanton", "Villas", "Tao"]),
    ("C", ["Villas", "White", "Quinn", "Stanton", "Peters", "Tao", "Rovero"]),
    ("D", ["Villas", "White", "Stanton", "Peters", "Quinn", "Tao", "Rovero"]),
    ("E", ["Villas", "White", "Stanton", "Peters", "Rovero", "Tao", "Quinn"])
]

found_options = []
for letter, order in options:
    solver.push()
    # Add constraints that the positions match the given order
    for idx, name in enumerate(order):
        solver.add(pos[name] == idx + 1)
    # Check if this option satisfies all constraints
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