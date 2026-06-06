from z3 import *

# Employees
employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
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

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The question asks "which one of the following MUST be true?"
# This means we need to find the option that is true in ALL valid models.
# Let's re-verify the "MUST be true" logic.
# If an option is true in all models, then Not(option) is unsat.

must_be_true = []
for letter, constr in options.items():
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Found {len(must_be_true)} options that must be true: {must_be_true}")