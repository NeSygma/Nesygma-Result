from z3 import *

solver = Solver()

# Decision variables
# pianist[i] where 0=Wayne, 1=Zara
pianist = [Int(f'pianist_{i}') for i in range(5)]
# piece[i] where 0=modern, 1=traditional
piece = [Int(f'piece_{i}') for i in range(5)]

# Constraints
constraints = []

# 1. Third solo is traditional (solo 2 if 0-indexed)
constraints.append(piece[2] == 1)

# 2. Exactly two traditional pieces are performed consecutively
# This means: there is exactly one pair of consecutive solos where both are traditional
consec_pairs = []
for i in range(4):
    consec_pairs.append(And(piece[i] == 1, piece[i+1] == 1))

# The number of true consec_pairs must be exactly 1
constraints.append(Sum([If(p, 1, 0) for p in consec_pairs]) == 1)

# 3. Fourth solo: either Wayne performs traditional OR Zara performs modern
constraints.append(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# 4. Pianist of second solo (index 1) is not pianist of fifth solo (index 4)
constraints.append(pianist[1] != pianist[4])

# 5. No traditional piece is performed until Wayne performs at least one modern piece
# For each traditional piece, there must be a Wayne modern piece before it
for i in range(5):
    if piece[i] == 1:
        before_constraints = []
        for j in range(i):
            before_constraints.append(And(pianist[j] == 0, piece[j] == 0))
        constraints.append(Or(before_constraints))

# 6. Additional condition: Wayne performs traditional in fifth solo
constraints.append(And(pianist[4] == 0, piece[4] == 1))

# Add domain constraints
for i in range(5):
    constraints.append(Or(pianist[i] == 0, pianist[i] == 1))
    constraints.append(Or(piece[i] == 0, piece[i] == 1))

# Add all constraints to solver
solver.add(constraints)

# Now check each option
found_options = []

# Option A: Zara performs the first solo
# pianist[0] == 1
solver.push()
solver.add(pianist[0] == 1)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Wayne performs the second solo
# pianist[1] == 0
solver.push()
solver.add(pianist[1] == 0)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Zara performs the third solo
# pianist[2] == 1
solver.push()
solver.add(pianist[2] == 1)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The second solo is a modern piece
# piece[1] == 0
solver.push()
solver.add(piece[1] == 0)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The fourth solo is a traditional piece
# piece[3] == 1
solver.push()
solver.add(piece[3] == 1)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")