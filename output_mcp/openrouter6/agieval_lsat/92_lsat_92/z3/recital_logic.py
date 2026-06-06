from z3 import *

solver = Solver()

# Variables for 5 solos (indices 0-4 correspond to solos 1-5)
isWayne = [Bool(f'wayne_{i}') for i in range(5)]
isTraditional = [Bool(f'traditional_{i}') for i in range(5)]

# Base constraints

# 1. Third solo is traditional
solver.add(isTraditional[2] == True)

# 2. Exactly two traditional pieces are consecutive
# Define consecutive pairs
pairs = [And(isTraditional[i], isTraditional[i+1]) for i in range(4)]
# Count how many pairs are true
pair_count = Sum([If(p, 1, 0) for p in pairs])
solver.add(pair_count == 1)

# 3. Fourth solo: either Wayne performs a traditional piece or Zara performs a modern piece
# This translates to: isWayne[3] == isTraditional[3]
solver.add(isWayne[3] == isTraditional[3])

# 4. Pianist of second solo != pianist of fifth solo
solver.add(isWayne[1] != isWayne[4])

# 5. No traditional piece until Wayne performs at least one modern piece
# For each solo i, if it's traditional, there must be an earlier solo j where Wayne performed a modern piece.
for i in range(5):
    if i == 0:
        # First solo cannot be traditional because no earlier solo
        solver.add(Not(isTraditional[0]))
    else:
        # For solo i, if traditional, then there exists j < i with Wayne modern
        earlier_modern = Or([And(isWayne[j], Not(isTraditional[j])) for j in range(i)])
        solver.add(Implies(isTraditional[i], earlier_modern))

# Additional premise: fifth solo Wayne performs a traditional piece
solver.add(isWayne[4] == True)
solver.add(isTraditional[4] == True)

# Now evaluate each answer choice
options = [
    ("A", isWayne[0] == False),  # Zara performs the first solo
    ("B", isWayne[1] == True),   # Wayne performs the second solo
    ("C", isWayne[2] == False),  # Zara performs the third solo
    ("D", isTraditional[1] == False),  # The second solo is a modern piece
    ("E", isTraditional[3] == True)    # The fourth solo is a traditional piece
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