from z3 import *

solver = Solver()

# Variables
pianist = [Int(f'p{i}') for i in range(5)]
piece = [Int(f'piece{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(And(pianist[i] >= 0, pianist[i] <= 1))
    solver.add(And(piece[i] >= 0, piece[i] <= 1))

# Third solo is traditional
solver.add(piece[2] == 1)

# Fifth solo is traditional (given in question)
solver.add(piece[4] == 1)

# Exactly one consecutive pair of traditional pieces
consec = [If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]
solver.add(Sum(consec) == 1)

# Fourth solo condition
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Pianist of second solo != pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# No traditional until Wayne performs at least one modern piece
for i in range(5):
    j_conditions = [And(pianist[j] == 0, piece[j] == 0) for j in range(i+1)]
    solver.add(Implies(piece[i] == 1, Or(j_conditions)))

# Solve base constraints
if solver.check() != sat:
    print("STATUS: unsat")
    exit()

model = solver.model()

# Compute forced solos
forced_count = 0
for i in range(5):
    solver.push()
    solver.add(pianist[i] != model[pianist[i]])
    if solver.check() == unsat:
        forced_count += 1
    solver.pop()

# Now test options
found_options = []
for letter, number in [("A",1), ("B",2), ("C",3), ("D",4), ("E",5)]:
    solver.push()
    if forced_count == number:
        solver.add(True)
    else:
        solver.add(False)
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