from z3 import *

solver = Solver()

# Number of solos
N = 5

# Pianists: True = Wayne, False = Zara
pianist = [Bool(f'pianist_{i}') for i in range(N)]

# Piece types: True = traditional, False = modern
piece_type = [Bool(f'piece_type_{i}') for i in range(N)]

# Constraint 1: The third solo (index 2) is a traditional piece
solver.add(piece_type[2] == True)

# Constraint 2: Exactly two traditional pieces in total, and they are performed consecutively
# So, there are exactly two True values in piece_type, and they are consecutive
solver.add(Sum(piece_type) == 2)

# Ensure the two traditional pieces are consecutive
consecutive_pairs = []
for i in range(N - 1):
    consecutive_pairs.append(And(piece_type[i], piece_type[i+1]))
solver.add(Sum(consecutive_pairs) >= 1)

# Constraint 3: In the fourth solo (index 3), either Wayne performs a traditional piece or Zara performs a modern piece
solver.add(Or(And(pianist[3], piece_type[3]), And(Not(pianist[3]), Not(piece_type[3]))))

# Constraint 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4)
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# For each solo i, if it is traditional, then there must be a prior solo j < i where Wayne performs a modern piece
for i in range(N):
    if i > 0:
        prior_modern_wayne = Sum([If(And(pianist[j], Not(piece_type[j])), 1, 0) for j in range(i)])
        solver.add(Implies(piece_type[i], prior_modern_wayne > 0))
    else:
        solver.add(Implies(piece_type[0], False))

# Count the number of solos in which Wayne performs a traditional piece
wayne_traditional_count = Sum([If(And(pianist[i], piece_type[i]), 1, 0) for i in range(N)])

# Define the options
options = [
    ("A", wayne_traditional_count == 0),
    ("B", wayne_traditional_count == 1),
    ("C", wayne_traditional_count == 2),
    ("D", wayne_traditional_count == 3),
    ("E", wayne_traditional_count == 4),
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