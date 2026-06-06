from z3 import *

# Create solver
solver = Solver()

# Define variables
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]  # 1-5
piece_type = [Int(f'piece_type_{i}') for i in range(1, 6)]  # 1-5

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))  # Wayne or Zara
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))  # modern or traditional

# Constraint 1: Third solo is traditional
solver.add(piece_type[2] == 1)  # position 3 (index 2)

# Constraint 2: Exactly two traditional pieces are performed consecutively
# We need exactly one consecutive pair (since exactly two traditional pieces are consecutive)
consecutive_traditional = []
for i in range(4):
    is_consecutive = If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0)
    consecutive_traditional.append(is_consecutive)
solver.add(Sum(consecutive_traditional) == 1)

# Constraint 3: Fourth solo: either Wayne performs traditional OR Zara performs modern
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, piece_type[3] == 0)   # Zara performs modern
))

# Constraint 4: Pianist who performs second solo does not perform fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# Position 1 cannot be traditional (no positions before it)
solver.add(piece_type[0] == 0)  # position 1 must be modern

# For positions 2-5: if traditional, then either there's a traditional before OR Wayne modern before
for i in range(1, 5):
    has_traditional_before = Or([piece_type[j] == 1 for j in range(i)])
    has_wayne_modern_before = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
    solver.add(Implies(piece_type[i] == 1, Or(has_traditional_before, has_wayne_modern_before)))

# Count Wayne traditional pieces
wayne_traditional_count = Sum([If(And(pianist[i] == 0, piece_type[i] == 1), 1, 0) for i in range(5)])

# Now find the minimum possible value of wayne_traditional_count
# We'll test from 0 upward until we find a satisfiable constraint
min_found = None
for test_count in range(6):  # 0 to 5
    solver.push()
    solver.add(wayne_traditional_count == test_count)
    if solver.check() == sat:
        min_found = test_count
        solver.pop()
        break
    solver.pop()

if min_found is not None:
    print("STATUS: sat")
    print(f"Minimum Wayne traditional pieces: {min_found}")
    # Now test which option matches
    if min_found == 0:
        print("answer:A")
    elif min_found == 1:
        print("answer:B")
    elif min_found == 2:
        print("answer:C")
    elif min_found == 3:
        print("answer:D")
    elif min_found == 4:
        print("answer:E")
else:
    print("STATUS: unsat")
    print("Refine: No solution found")