from z3 import *

solver = Solver()

# 7 accomplices, each assigned a position 1-7
P = Int('Peters')
Q = Int('Quinn')
R = Int('Rovero')
S = Int('Stanton')
T = Int('Tao')
V = Int('Villas')
W = Int('White')

people = [P, Q, R, S, T, V, W]
names = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']

# All positions 1-7, all distinct
for p in people:
    solver.add(p >= 1, p <= 7)
solver.add(Distinct(people))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Abs(S - T) != 1)

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White
solver.add(W == V + 1)

# Constraint 4: Peters was recruited fourth
solver.add(P == 4)

# Additional condition from the question: Quinn was recruited immediately before Rovero
solver.add(R == Q + 1)

# Now test each answer choice
# The question: Stanton CANNOT have been recruited at which position?
# For each option, check if Stanton CAN be at that position.
# The answer is the one where Stanton CANNOT be there (unsat).

options = [
    ("A", 1),  # first
    ("B", 2),  # second
    ("C", 3),  # third
    ("D", 5),  # fifth
    ("E", 7),  # seventh
]

found_options = []
for letter, pos in options:
    solver.push()
    solver.add(S == pos)
    result = solver.check()
    if result == unsat:
        # Stanton CANNOT be at this position - this is the answer
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