from z3 import *

solver = Solver()

# Solo positions 0..4 (1st to 5th)
N = 5

# pianist[i] = 0 for Wayne, 1 for Zara
pianist = [Int(f'pianist_{i}') for i in range(N)]
# piece_type[i] = 0 for modern, 1 for traditional
piece = [Int(f'piece_{i}') for i in range(N)]

# Domain constraints
for i in range(N):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Constraint 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# Count consecutive traditional pairs (i,i+1)
consec_pairs = [If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(N-1)]
solver.add(Sum(consec_pairs) == 1)

# Constraint 3: In the fourth solo (index 3), either Wayne performs a traditional piece or Zara performs a modern piece.
# (pianist[3]==0 AND piece[3]==1) OR (pianist[3]==1 AND piece[3]==0)
solver.add(Or(And(pianist[3] == 0, piece[3] == 1), And(pianist[3] == 1, piece[3] == 0)))

# Constraint 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each solo i, if piece[i]==1, then there exists some j < i with piece[j]==0 and pianist[j]==0.
for i in range(N):
    if i == 0:
        # No earlier solo, so cannot be traditional
        solver.add(piece[i] == 0)  # first solo must be modern
    else:
        # The first traditional piece must be preceded by a Wayne modern piece
        # This means: if piece[i]==1 then there exists j < i such that piece[j]==0 and pianist[j]==0.
        solver.add(Implies(piece[i] == 1,
                           Or([And(piece[j] == 0, pianist[j] == 0) for j in range(i)])))

# Additional condition: In the fifth solo (index 4) Wayne performs a traditional piece.
solver.add(pianist[4] == 0)
solver.add(piece[4] == 1)

# Now test each option

# Option A: Zara performs the first solo. => pianist[0] == 1
opt_a = (pianist[0] == 1)

# Option B: Wayne performs the second solo. => pianist[1] == 0
opt_b = (pianist[1] == 0)

# Option C: Zara performs the third solo. => pianist[2] == 1
opt_c = (pianist[2] == 1)

# Option D: The second solo is a modern piece. => piece[1] == 0
opt_d = (piece[1] == 0)

# Option E: The fourth solo is a traditional piece. => piece[3] == 1
opt_e = (piece[3] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        # print(f"Option {letter} is possible")
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