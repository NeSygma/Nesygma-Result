from z3 import *

solver = Solver()

# Variables: for each solo (1-5), who plays (W=Wayne, Z=Zara) and what type (T=Traditional, M=Modern)
# pianist: 0=Wayne, 1=Zara; piece_type: 0=Modern, 1=Traditional
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece_type = [Int(f'piece_type_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Condition 1: The third solo is a traditional piece.
solver.add(piece_type[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means: there exists exactly one pair of consecutive solos that are both traditional,
# and no other traditional pieces exist outside this pair.
# Let's enumerate all possible consecutive pairs and ensure exactly one such pair exists.
trad_count = Sum([If(piece_type[i] == 1, 1, 0) for i in range(5)])
# At least 2 traditional pieces (the consecutive pair)
solver.add(trad_count >= 2)

# Exactly one consecutive pair of traditional pieces
pair_count = Sum([If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0) for i in range(4)])
solver.add(pair_count == 1)

# No other traditional pieces outside the consecutive pair
# This means: if piece_type[i] == 1, then either piece_type[i-1] == 1 or piece_type[i+1] == 1
for i in range(5):
    if i == 0:
        solver.add(Implies(piece_type[0] == 1, piece_type[1] == 1))
    elif i == 4:
        solver.add(Implies(piece_type[4] == 1, piece_type[3] == 1))
    else:
        solver.add(Implies(piece_type[i] == 1, Or(piece_type[i-1] == 1, piece_type[i+1] == 1)))

# Condition 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece_type[3] == 1),
              And(pianist[3] == 1, piece_type[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for every solo i that is traditional, there must exist some solo j < i where
# Wayne plays a modern piece.
for i in range(5):
    if i == 0:
        # If solo 1 is traditional, there's no preceding solo, so this is impossible
        solver.add(piece_type[0] == 0)  # solo 1 cannot be traditional
    else:
        preceding_wayne_modern = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
        solver.add(Implies(piece_type[i] == 1, preceding_wayne_modern))

# Additional condition from question: The pianist who performs the first solo also performs the second solo.
solver.add(pianist[0] == pianist[1])

# Now evaluate each answer choice
# (A) Zara performs the first solo.
opt_a = (pianist[0] == 1)
# (B) Wayne performs the third solo.
opt_b = (pianist[2] == 0)
# (C) Zara performs the fifth solo.
opt_c = (pianist[4] == 1)
# (D) The second solo is a traditional piece.
opt_d = (piece_type[1] == 1)
# (E) The fourth solo is a modern piece.
opt_e = (piece_type[3] == 0)

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