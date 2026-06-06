from z3 import *

solver = Solver()

# Variables for each position (1-5)
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]  # 0 = Wayne, 1 = Zara
piece_type = [Int(f'type_{i}') for i in range(1, 6)]   # 0 = Modern, 1 = Traditional

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Constraint 1: Third solo is traditional
solver.add(piece_type[2] == 1)  # index 2 corresponds to position 3

# Constraint 2: Exactly two traditional pieces are performed consecutively
# We need exactly one pair of consecutive T's
consecutive_pairs = []
for i in range(4):  # positions 1-4 can start a consecutive pair
    consecutive_pairs.append(And(piece_type[i] == 1, piece_type[i+1] == 1))

# Count how many consecutive T pairs exist
solver.add(Sum([If(cp, 1, 0) for cp in consecutive_pairs]) == 1)

# Constraint 3: Fourth solo condition
# (Wayne performs traditional) OR (Zara performs modern)
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),
    And(pianist[3] == 1, piece_type[3] == 0)
))

# Constraint 4: Pianist of second solo ≠ pianist of fifth solo
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece until Wayne performs at least one modern piece
# For each position i where type[i] = T, there must be some j < i with pianist[j] = W and type[j] = M
for i in range(5):
    if piece_type[i] == 1:  # traditional
        # There exists j < i such that pianist[j] = W and type[j] = M
        exists_modern_wayne_before = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
        solver.add(Implies(piece_type[i] == 1, exists_modern_wayne_before))

# Additional condition: Fifth solo is Wayne performing traditional
solver.add(pianist[4] == 0)  # Wayne
solver.add(piece_type[4] == 1)  # Traditional

# Now evaluate each answer choice
found_options = []

# Option A: Zara performs the first solo
opt_a = pianist[0] == 1  # Zara
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wayne performs the second solo
opt_b = pianist[1] == 0  # Wayne
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Zara performs the third solo
opt_c = pianist[2] == 1  # Zara
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The second solo is a modern piece
opt_d = piece_type[1] == 0  # Modern
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The fourth solo is a traditional piece
opt_e = piece_type[3] == 1  # Traditional
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")