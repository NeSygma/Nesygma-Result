from z3 import *

solver = Solver()

# Student indices: 0=Louis, 1=Mollie, 2=Onyx, 3=Ryan, 4=Tiffany, 5=Yoshio
# Assign positions for years 1921..1924 (indices 0..3)
assign = [Int(f'assign_{i}') for i in range(4)]

# Domain: each position must be one of the six students
for i in range(4):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# Exactly 4 distinct students assigned
solver.add(Distinct(assign))

# Condition 1: Only Louis (0) or Tiffany (4) can be assigned to 1923 (index 2)
solver.add(Or(assign[2] == 0, assign[2] == 4))

# Condition 2: If Mollie (1) is assigned, then she must be at index 0 or 1
solver.add(Implies(Or([assign[i] == 1 for i in range(4)]), Or(assign[0] == 1, assign[1] == 1)))

# Condition 3: If Tiffany (4) is assigned, then Ryan (3) must be assigned
solver.add(Implies(Or([assign[i] == 4 for i in range(4)]), Or([assign[i] == 3 for i in range(4)])))

# Condition 4: If Ryan (3) is assigned, then Onyx (2) must be assigned to the year immediately prior to Ryan's
solver.add(Implies(Or([assign[i] == 3 for i in range(4)]), 
                   Or([And(assign[i] == 3, assign[i-1] == 2) for i in range(1, 4)])))

# Now test each option
options = [
    ("A", [0, 2, 3, 5]),  # Louis, Onyx, Ryan, Yoshio
    ("B", [1, 5, 4, 2]),  # Mollie, Yoshio, Tiffany, Onyx
    ("C", [2, 3, 0, 4]),  # Onyx, Ryan, Louis, Tiffany
    ("D", [4, 2, 0, 3]),  # Tiffany, Onyx, Louis, Ryan
    ("E", [5, 2, 0, 1])   # Yoshio, Onyx, Louis, Mollie
]

found_options = []
for letter, vals in options:
    solver.push()
    # Add constraints that the assignment matches this option exactly
    for i in range(4):
        solver.add(assign[i] == vals[i])
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