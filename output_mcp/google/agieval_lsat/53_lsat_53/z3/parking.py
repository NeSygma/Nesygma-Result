from z3 import *

# Employees
employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
# Spaces 1-6
spaces = [1, 2, 3, 4, 5, 6]

# Variables: space assigned to each employee
assign = {e: Int(e) for e in employees}

solver = Solver()

# Each employee gets a unique space
for e in employees:
    solver.add(assign[e] >= 1, assign[e] <= 6)
solver.add(Distinct([assign[e] for e in employees]))

# Rules
# Young > Togowa
solver.add(assign['Young'] > assign['Togowa'])
# Xu > Souza
solver.add(assign['Xu'] > assign['Souza'])
# Robertson > Young
solver.add(assign['Robertson'] > assign['Young'])
# Robertson in {1, 2, 3, 4}
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

found_options = []
for label, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    # If Not(constr) is unsat, then constr must be true
    if solver.check() == unsat:
        found_options.append(label)
    solver.pop()

print(f"Options that must be true: {found_options}")