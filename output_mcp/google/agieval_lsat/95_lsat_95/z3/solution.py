from z3 import *

# Houses
houses = ['J', 'K', 'L', 'M', 'N', 'O', 'P']
pos = {h: Int(f'pos_{h}') for h in houses}

solver = Solver()

# 1. Positions are 1-7 and distinct
for h in houses:
    solver.add(pos[h] >= 1, pos[h] <= 7)
solver.add(Distinct([pos[h] for h in houses]))

# 2. J must be shown in the evening (6, 7)
solver.add(Or(pos['J'] == 6, pos['J'] == 7))

# 3. K cannot be shown in the morning (not 1, 2)
solver.add(pos['K'] >= 3)

# 4. K < L < M
solver.add(pos['K'] < pos['L'])
solver.add(pos['L'] < pos['M'])

# Define time slots
def is_morning(p): return Or(p == 1, p == 2)
def is_afternoon(p): return Or(p == 3, p == 4, p == 5)
def is_evening(p): return Or(p == 6, p == 7)

# Options
options = [
    ("A", is_evening(pos['K'])),
    ("B", is_afternoon(pos['L'])),
    ("C", is_evening(pos['L'])),
    ("D", is_morning(pos['M'])),
    ("E", is_afternoon(pos['M']))
]

# Check which one MUST be true
# An option must be true if Not(option) is unsatisfiable given the constraints
must_be_true = []
for letter, constr in options:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_be_true.append(letter)
    solver.pop()

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")