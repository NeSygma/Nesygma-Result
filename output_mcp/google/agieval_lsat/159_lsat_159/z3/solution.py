from z3 import *

# Photographers
photographers = ['F', 'G', 'H', 'K', 'L', 'M']
# Assignments: 0=None, 1=Silva, 2=Thorne
val = {p: Int(p) for p in photographers}

solver = Solver()

# Domain constraints
for p in photographers:
    solver.add(val[p] >= 0, val[p] <= 2)

# Constraint 1: At least two at S, at least two at T
solver.add(Sum([If(val[p] == 1, 1, 0) for p in photographers]) >= 2)
solver.add(Sum([If(val[p] == 2, 1, 0) for p in photographers]) >= 2)

# Constraint 3: Frost and Heideck together AND assigned
solver.add(val['F'] == val['H'])
solver.add(val['F'] != 0)

# Constraint 4: If L and M are both assigned, they must be at different ceremonies
solver.add(Implies(And(val['L'] != 0, val['M'] != 0), val['L'] != val['M']))

# Constraint 5: If G is at S, then L must be at T
solver.add(Implies(val['G'] == 1, val['L'] == 2))

# Constraint 6: If K is not at T, then H and M must be at T
solver.add(Implies(val['K'] != 2, And(val['H'] == 2, val['M'] == 2)))

# Question constraint: Exactly four assigned
solver.add(Sum([If(val[p] != 0, 1, 0) for p in photographers]) == 4)

options = {
    "A": 'F',
    "B": 'G',
    "C": 'K',
    "D": 'L',
    "E": 'M'
}

found_options = []
for letter, p in options.items():
    # Check if it's possible for p NOT to be at S
    solver.push()
    solver.add(val[p] != 1)
    if solver.check() == unsat:
        # If it's impossible for p not to be at S, then p MUST be at S
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