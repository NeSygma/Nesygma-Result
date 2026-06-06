from z3 import *

# Define student indices
Louis = 0
Mollie = 1
Onyx = 2
Ryan = 3
Tiffany = 4
Yoshio = 5

# Define year indices (0:1921, 1:1922, 2:1923, 3:1924)
years = [1921, 1922, 1923, 1924]

# Variables: assign[i] = student assigned to year i
assign = [Int(f'assign_{i}') for i in range(4)]

# Base constraints
base_constraints = []

# Each assign[i] must be between 0 and 5
for i in range(4):
    base_constraints.append(assign[i] >= 0)
    base_constraints.append(assign[i] <= 5)

# All four assigned students must be distinct
base_constraints.append(Distinct(assign))

# Condition 1: Only Louis or Tiffany can be assigned to 1923 (year index 2)
base_constraints.append(Or(assign[2] == Louis, assign[2] == Tiffany))

# Condition 2: If Mollie is assigned, she must be assigned to 1921 or 1922
for i in range(4):
    base_constraints.append(Implies(assign[i] == Mollie, Or(i == 0, i == 1)))

# Condition 3: If Tiffany is assigned, then Ryan must be assigned
tiffany_assigned = Or([assign[i] == Tiffany for i in range(4)])
ryan_assigned = Or([assign[i] == Ryan for i in range(4)])
base_constraints.append(Implies(tiffany_assigned, ryan_assigned))

# Condition 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
# Ryan cannot be assigned to 1921 (index 0) because there is no prior year
base_constraints.append(assign[0] != Ryan)
for i in range(1, 4):
    base_constraints.append(Implies(assign[i] == Ryan, assign[i-1] == Onyx))

# Create solver and add base constraints
solver = Solver()
solver.add(base_constraints)

# Define answer choices as constraints
options = [
    ("A", assign[3] == Louis),          # Louis assigned to 1924
    ("B", assign[0] == Onyx),           # Onyx assigned to 1921
    ("C", assign[3] == Onyx),           # Onyx assigned to 1924
    ("D", assign[2] == Tiffany),        # Tiffany assigned to 1923
    ("E", assign[0] == Yoshio)          # Yoshio assigned to 1921
]

found_options = []

for letter, constr in options:
    # Check if base + option is consistent
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Now check if adding "Mollie not assigned to 1922" makes it unsat
        solver.push()
        solver.add(assign[1] != Mollie)  # Mollie not assigned to 1922
        if solver.check() == unsat:
            found_options.append(letter)
        solver.pop()
    solver.pop()

# Determine result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")