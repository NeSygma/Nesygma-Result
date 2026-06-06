from z3 import *
solver = Solver()

# Declare variables
pos_F = Int('pos_F')
pos_G = Int('pos_G')
pos_H = Int('pos_H')
pos_J = Int('pos_J')
pos_litho = Int('pos_litho')
pos_oil = Int('pos_oil')
pos_sculpt = Int('pos_sculpt')
pos_water = Int('pos_water')

# Base constraints
solver.add(pos_F >= 1, pos_F <= 4)
solver.add(pos_G >= 1, pos_G <= 4)
solver.add(pos_H >= 1, pos_H <= 4)
solver.add(pos_J >= 1, pos_J <= 4)
solver.add(pos_litho >= 1, pos_litho <= 4)
solver.add(pos_oil >= 1, pos_oil <= 4)
solver.add(pos_sculpt >= 1, pos_sculpt <= 4)
solver.add(pos_water >= 1, pos_water <= 4)

solver.add(Distinct([pos_F, pos_G, pos_H, pos_J]))
solver.add(Distinct([pos_litho, pos_oil, pos_sculpt, pos_water]))

solver.add(pos_oil < pos_litho)
solver.add(pos_water < pos_litho)
solver.add(pos_F < pos_oil)
solver.add(pos_H < pos_G)
solver.add(pos_H < pos_J)

# Now define options
options = [
    ("A", [pos_F == 1, pos_H == 2, pos_G == 3, pos_J == 4,
           pos_sculpt == 1, pos_litho == 2, pos_oil == 3, pos_water == 4]),
    ("B", [pos_F == 1, pos_J == 2, pos_H == 3, pos_G == 4,
           pos_water == 1, pos_oil == 2, pos_sculpt == 3, pos_litho == 4]),
    ("C", [pos_G == 1, pos_F == 2, pos_H == 3, pos_J == 4,
           pos_sculpt == 1, pos_water == 2, pos_oil == 3, pos_litho == 4]),
    ("D", [pos_H == 1, pos_J == 2, pos_F == 3, pos_G == 4,
           pos_oil == 1, pos_water == 2, pos_litho == 3, pos_sculpt == 4]),
    ("E", [pos_H == 1, pos_F == 2, pos_J == 3, pos_G == 4,
           pos_sculpt == 1, pos_water == 2, pos_oil == 3, pos_litho == 4])
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