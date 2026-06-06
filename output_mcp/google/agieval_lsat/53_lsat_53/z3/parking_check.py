from z3 import *

# Employees
employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']

# Variables: space assigned to each employee
assign = {e: Int(e) for e in employees}

solver = Solver()

# Each employee gets a unique space
for e in employees:
    solver.add(assign[e] >= 1, assign[e] <= 6)
solver.add(Distinct([assign[e] for e in employees]))

# Rules
solver.add(assign['Young'] > assign['Togowa'])
solver.add(assign['Xu'] > assign['Souza'])
solver.add(assign['Robertson'] > assign['Young'])
solver.add(Or([assign['Robertson'] == i for i in [1, 2, 3, 4]]))

# Condition: Robertson is assigned parking space #3
solver.add(assign['Robertson'] == 3)

# Test options
options = {
    "A": assign['Souza'] == 4,
    "B": assign['Togowa'] == 2,
    "C": assign['Vaughn'] == 5,
    "D": assign['Xu'] == 6,
    "E": assign['Young'] == 2
}

# Check which options are valid (can be true)
# The question asks "which one of the following MUST be true"
# This means we are looking for an option that is true in ALL valid models.
# We can check this by verifying if Not(option) is unsatisfiable.

for label, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        print(f"Option {label} MUST be true.")
    else:
        print(f"Option {label} is NOT necessarily true.")
    solver.pop()