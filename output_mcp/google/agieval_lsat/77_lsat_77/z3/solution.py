from z3 import *

# Businesses
# P: Pharmacy
# R1, R2: Restaurants
# O: Optometrist
# V: Veterinarian
# S: Shoe store
# T: Toy store

businesses = ['P', 'R1', 'R2', 'O', 'V', 'S', 'T']
pos = {b: Int(b) for b in businesses}

solver = Solver()

# Each business in a unique space 1-7
for b in businesses:
    solver.add(pos[b] >= 1, pos[b] <= 7)
solver.add(Distinct([pos[b] for b in businesses]))

# Constraint 1: Pharmacy at one end, one restaurant at the other
# (P=1 and (R1=7 or R2=7)) or (P=7 and (R1=1 or R2=1))
solver.add(Or(
    And(pos['P'] == 1, Or(pos['R1'] == 7, pos['R2'] == 7)),
    And(pos['P'] == 7, Or(pos['R1'] == 1, pos['R2'] == 1))
))

# Constraint 2: Two restaurants separated by at least two other businesses
# abs(pos[R1] - pos[R2]) >= 3
solver.add(If(pos['R1'] > pos['R2'], pos['R1'] - pos['R2'] >= 3, pos['R2'] - pos['R1'] >= 3))

# Constraint 3: Pharmacy next to O or V
# abs(pos[P] - pos[O]) == 1 or abs(pos[P] - pos[V]) == 1
solver.add(Or(
    If(pos['P'] > pos['O'], pos['P'] - pos['O'] == 1, pos['O'] - pos['P'] == 1),
    If(pos['P'] > pos['V'], pos['P'] - pos['V'] == 1, pos['V'] - pos['P'] == 1)
))

# Constraint 4: Toy store cannot be next to veterinarian
# abs(pos[T] - pos[V]) != 1
solver.add(If(pos['T'] > pos['V'], pos['T'] - pos['V'] != 1, pos['V'] - pos['T'] != 1))

# Condition: Shoe store is in space 2
solver.add(pos['S'] == 2)

# Options
options = [
    ("A", pos['O'] == 5),
    ("B", pos['P'] == 1),
    ("C", Or(pos['R1'] == 3, pos['R2'] == 3)),
    ("D", pos['T'] == 6),
    ("E", pos['V'] == 4)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
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