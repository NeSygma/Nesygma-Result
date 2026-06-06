from z3 import *

solver = Solver()

# 5 solos, indices 0..4
pianist = [Int(f'p_{i}') for i in range(5)]
piece = [Int(f'pc_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive pairs of traditional pieces.
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each solo i, if piece[i]==1, then there exists j < i with pianist[j]==0 and piece[j]==0.
for i in range(5):
    if i == 0:
        solver.add(piece[0] != 1)
    else:
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Additional condition: The pianist who performs the first solo also performs the second solo.
solver.add(pianist[0] == pianist[1])

# Now evaluate each option as "must be true" — i.e., check if the negation is possible.
# An option "must be true" if adding its negation makes the problem unsat.
# So we check: base + NOT(option) -> if unsat, then option must be true.

found_options = []
for letter, constr in [("A", pianist[0] == 1), ("B", pianist[2] == 0), ("C", pianist[4] == 1), ("D", piece[1] == 1), ("E", piece[3] == 0)]:
    solver.push()
    solver.add(Not(constr))
    res = solver.check()
    if res == unsat:
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