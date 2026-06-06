from z3 import *

# Businesses
businesses = ['O', 'P', 'R1', 'R2', 'S', 'T', 'V']
pos = {b: Int(f'pos_{b}') for b in businesses}

solver = Solver()

# Domain constraints
for b in businesses:
    solver.add(pos[b] >= 1, pos[b] <= 7)

# All businesses in distinct spaces
solver.add(Distinct([pos[b] for b in businesses]))

# Constraint 1: Pharmacy at one end, one restaurant at the other
solver.add(Or(
    And(pos['P'] == 1, Or(pos['R1'] == 7, pos['R2'] == 7)),
    And(pos['P'] == 7, Or(pos['R1'] == 1, pos['R2'] == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
solver.add(Abs(pos['R1'] - pos['R2']) >= 3)

# Constraint 3: Pharmacy next to Optometrist or Veterinarian
solver.add(Or(
    Abs(pos['P'] - pos['O']) == 1,
    Abs(pos['P'] - pos['V']) == 1
))

# Constraint 4: Toy store not next to Veterinarian
solver.add(Abs(pos['T'] - pos['V']) != 1)

# Question condition: Veterinarian in space 5
solver.add(pos['V'] == 5)

# Answer choices
# (A) The optometrist is in space 2.
# (B) The pharmacy is in space 7.
# (C) A restaurant is in space 4.
# (D) The shoe store is in space 6.
# (E) The toy store is in space 3.

options = [
    ("A", pos['O'] == 2),
    ("B", pos['P'] == 7),
    ("C", Or(pos['R1'] == 4, pos['R2'] == 4)),
    ("D", pos['S'] == 6),
    ("E", pos['T'] == 3)
]

# To find what MUST be true, we check if the negation is UNSAT
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
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")