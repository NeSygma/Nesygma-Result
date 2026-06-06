from z3 import *

solver = Solver()

# 0 = Wayne, 1 = Zara
pianist = [Int(f'pianist_{i}') for i in range(5)]
# 0 = modern, 1 = traditional
piece = [Int(f'piece_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count adjacent pairs which are both traditional
consec_pairs = [If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]
solver.add(Sum(consec_pairs) == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece
# or Zara performs a modern piece.
# Fourth solo is index 3.
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
# Second solo is index 1, fifth solo is index 4.
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each position i, if piece[i] is traditional, then there must exist some j < i
# where pianist[j] is Wayne (0) and piece[j] is modern (0).
for i in range(5):
    # For i=0, there is no j < i, so piece[0] cannot be traditional unless... 
    # Actually the condition says "No traditional piece is performed until Wayne performs 
    # at least one modern piece." So the first traditional piece must come AFTER 
    # Wayne's first modern piece. So at position 0, it cannot be traditional 
    # (since there's no earlier position).
    if i == 0:
        solver.add(piece[0] != 1)  # First solo cannot be traditional
    else:
        # There exists some j < i where Wayne plays modern
        solver.add(Implies(piece[i] == 1, 
                          Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])))

# Additional condition from the question: The pianist who performs the first solo
# also performs the second solo.
solver.add(pianist[0] == pianist[1])

# Now evaluate each option under the additional condition
# Option A: Zara performs the first solo. => pianist[0] == 1
# Option B: Wayne performs the third solo. => pianist[2] == 0
# Option C: Zara performs the fifth solo. => pianist[4] == 1
# Option D: The second solo is a traditional piece. => piece[1] == 1
# Option E: The fourth solo is a modern piece. => piece[3] == 0

found_options = []
for letter, constr in [
    ("A", pianist[0] == 1),
    ("B", pianist[2] == 0),
    ("C", pianist[4] == 1),
    ("D", piece[1] == 1),
    ("E", piece[3] == 0)
]:
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