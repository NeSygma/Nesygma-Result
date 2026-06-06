from z3 import *

solver = Solver()

# Variables
traditional = [Bool(f't_{i}') for i in range(5)]
pianist = [Int(f'p_{i}') for i in range(5)]

# Domain for pianist: 0 = Wayne, 1 = Zara
for i in range(5):
    solver.add(pianist[i] >= 0, pianist[i] <= 1)

# Base constraints
# 1. third solo is traditional
solver.add(traditional[2] == True)

# 2. exactly two consecutive traditional pieces
consecutive = [And(traditional[i], traditional[i+1]) for i in range(4)]
solver.add(Sum([If(c, 1, 0) for c in consecutive]) == 1)

# 3. fourth solo condition
solver.add(Or(And(pianist[3]==0, traditional[3]), And(pianist[3]==1, Not(traditional[3]))))

# 4. pianist of second solo != pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# 5. no traditional until Wayne modern
# position 1 (index 0) cannot be traditional
solver.add(Not(traditional[0]))
# position 2 (index 1)
solver.add(Implies(traditional[1], And(pianist[0]==0, Not(traditional[0]))))
# position 3 (index 2)
solver.add(Implies(traditional[2], Or(
    And(pianist[0]==0, Not(traditional[0])),
    And(pianist[1]==0, Not(traditional[1]))
)))
# position 4 (index 3)
solver.add(Implies(traditional[3], Or(
    And(pianist[0]==0, Not(traditional[0])),
    And(pianist[1]==0, Not(traditional[1])),
    And(pianist[2]==0, Not(traditional[2]))
)))
# position 5 (index 4)
solver.add(Implies(traditional[4], Or(
    And(pianist[0]==0, Not(traditional[0])),
    And(pianist[1]==0, Not(traditional[1])),
    And(pianist[2]==0, Not(traditional[2])),
    And(pianist[3]==0, Not(traditional[3]))
)))

# Options
options = [
    ("A", [0, 2, 3]),   # positions 1,3,4
    ("B", [1, 2, 3]),   # positions 2,3,4
    ("C", [2, 3]),      # positions 3,4
    ("D", [2, 4]),      # positions 3,5
    ("E", [3, 4])       # positions 4,5
]

found_options = []
for letter, indices in options:
    solver.push()
    # Set traditional according to the option
    for i in range(5):
        if i in indices:
            solver.add(traditional[i])
        else:
            solver.add(Not(traditional[i]))
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