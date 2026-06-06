from z3 import *

solver = Solver()

# Variables
# pianist[i] = 0 for Wayne, 1 for Zara
pianist = [Int(f'p_{i}') for i in range(5)]
# piece[i] = 0 for modern, 1 for traditional
piece = [Int(f'pc_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive traditional pieces, and no longer run.
# We need to count consecutive pairs of traditional pieces.
consecutive_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(cp, 1, 0) for cp in consecutive_pairs]) == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for all i, if piece[i] == 1 (traditional), then there exists j < i such that pianist[j] == 0 and piece[j] == 0.
# Equivalently: the first traditional piece must be preceded by at least one modern piece by Wayne.
# We can encode: for each i, if piece[i]==1, then Or over j<i: (pianist[j]==0 and piece[j]==0)
for i in range(5):
    solver.add(Implies(piece[i] == 1, Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])))

# Additional given: In the fifth solo Wayne performs a traditional piece.
solver.add(pianist[4] == 0)
solver.add(piece[4] == 1)

# Now evaluate each option
# (A) Zara performs the first solo.
opt_a = (pianist[0] == 1)
# (B) Wayne performs the second solo.
opt_b = (pianist[1] == 0)
# (C) Zara performs the third solo.
opt_c = (pianist[2] == 1)
# (D) The second solo is a modern piece.
opt_d = (piece[1] == 0)
# (E) The fourth solo is a traditional piece.
opt_e = (piece[3] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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