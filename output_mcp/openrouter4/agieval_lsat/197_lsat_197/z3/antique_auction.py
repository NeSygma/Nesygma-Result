from z3 import *

solver = Solver()

# Days 1 to 6
days = list(range(1, 7))

# Variables for each antique
h, l, m, s, t, v = Ints('h l m s t v')

# Each antique assigned a distinct day 1-6
antiques = [h, l, m, s, t, v]
solver.add(Distinct(antiques))
for a in antiques:
    solver.add(a >= 1, a <= 6)

# Constraint 1: sundial not on June 1
solver.add(s != 1)

# Constraint 2: If harmonica earlier than lamp, then mirror earlier than lamp
solver.add(Implies(h < l, m < l))

# Constraint 3: sundial earlier than mirror and earlier than vase
solver.add(s < m)
solver.add(s < v)

# Constraint 4: table earlier than harmonica XOR table earlier than vase
solver.add((t < h) != (t < v))  # XOR using !=

# Now evaluate each option
options = [
    ("A", And(t == 2, l == 3)),
    ("B", And(s == 2, v == 3)),
    ("C", And(m == 3, s == 4)),
    ("D", And(v == 4, s == 5)),
    ("E", And(s == 4, t == 5))
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