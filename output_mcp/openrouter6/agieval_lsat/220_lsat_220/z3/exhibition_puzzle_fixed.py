from z3 import *

# Painting indices
F_oil = 0
F_water = 1
G_oil = 2
G_water = 3
H_oil = 4
H_water = 5
I_oil = 6
I_water = 7

# Slots: 8 slots, each for a painting index
# Order: wall1 upper, wall1 lower, wall2 upper, wall2 lower, wall3 upper, wall3 lower, wall4 upper, wall4 lower
slots = [Int(f'slot_{i}') for i in range(8)]

solver = Solver()

# Each slot must be between 0 and 7
for s in slots:
    solver.add(s >= 0, s <= 7)

# All slots distinct (each painting used exactly once)
solver.add(Distinct(slots))

# Constraint: each wall has exactly one oil and one watercolor
for w in range(4):
    upper = slots[2*w]
    lower = slots[2*w+1]
    # One even (oil) and one odd (watercolor)
    solver.add(Or(And(Mod(upper, 2) == 0, Mod(lower, 2) == 1),
                  And(Mod(upper, 2) == 1, Mod(lower, 2) == 0)))

# Constraint: each wall has paintings from two different students
for w in range(4):
    upper = slots[2*w]
    lower = slots[2*w+1]
    solver.add(Div(upper, 2) != Div(lower, 2))

# Constraint: no wall has both Franz and Isaacs
for w in range(4):
    upper = slots[2*w]
    lower = slots[2*w+1]
    # Franz indices: 0,1; Isaacs indices: 6,7
    solver.add(Not(Or(
        And(Or(upper == 0, upper == 1), Or(lower == 6, lower == 7)),
        And(Or(upper == 6, upper == 7), Or(lower == 0, lower == 1))
    )))

# Constraint: Greene's watercolor (3) is upper on the wall where Franz's oil (0) is displayed.
# Since they cannot share a slot, Franz's oil must be lower, Greene's watercolor upper.
solver.add(Or([And(slots[2*w] == 3, slots[2*w+1] == 0) for w in range(4)]))

# Constraint: Isaacs's oil (6) is lower on wall 4 (w=3)
solver.add(slots[7] == 6)

# Given scenario: Isaacs's watercolor (7) on wall 2 (w=1)
solver.add(Or(slots[2] == 7, slots[3] == 7))

# Given scenario: Franz's oil (0) on wall 3 (w=2)
# From constraint 4, Franz's oil must be lower, so slot[5] == 0 and Greene's watercolor upper slot[4] == 3
solver.add(slots[5] == 0)
solver.add(slots[4] == 3)

# Now evaluate multiple choice options
options = [
    ("A", F_water),   # Franz's watercolor
    ("B", G_oil),     # Greene's oil
    ("C", G_water),   # Greene's watercolor
    ("D", H_oil),     # Hidalgo's oil
    ("E", H_water)    # Hidalgo's watercolor
]

found_options = []
for letter, painting_idx in options:
    solver.push()
    # Constraint: painting is on wall 1 (either upper or lower slot)
    solver.add(Or(slots[0] == painting_idx, slots[1] == painting_idx))
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