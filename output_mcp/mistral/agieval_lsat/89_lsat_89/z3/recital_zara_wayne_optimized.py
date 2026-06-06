from z3 import *

# Number of solos
N = 5

# Pianists: True = Wayne, False = Zara
pianist = [Bool(f'pianist_{i}') for i in range(N)]

# Piece types: True = traditional, False = modern
piece_type = [Bool(f'piece_type_{i}') for i in range(N)]

# Use Optimize to find the minimum number of solos where Wayne performs a traditional piece
opt = Optimize()

# Constraint 1: The third solo (index 2) is a traditional piece
opt.add(piece_type[2] == True)

# Constraint 2: Exactly two traditional pieces in total, and they are performed consecutively
opt.add(Sum(piece_type) == 2)

# Ensure the two traditional pieces are consecutive
consecutive_pairs = []
for i in range(N - 1):
    consecutive_pairs.append(And(piece_type[i], piece_type[i+1]))
opt.add(Sum(consecutive_pairs) >= 1)

# Constraint 3: In the fourth solo (index 3), either Wayne performs a traditional piece or Zara performs a modern piece
opt.add(Or(And(pianist[3], piece_type[3]), And(Not(pianist[3]), Not(piece_type[3]))))

# Constraint 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4)
opt.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# For each solo i, if it is traditional, then there must be a prior solo j < i where Wayne performs a modern piece
for i in range(N):
    if i > 0:
        prior_modern_wayne = Sum([If(And(pianist[j], Not(piece_type[j])), 1, 0) for j in range(i)])
        opt.add(Implies(piece_type[i], prior_modern_wayne > 0))
    else:
        opt.add(Implies(piece_type[0], False))

# Count the number of solos in which Wayne performs a traditional piece
wayne_traditional_count = Sum([If(And(pianist[i], piece_type[i]), 1, 0) for i in range(N)])

# Minimize the number of solos where Wayne performs a traditional piece
opt.minimize(wayne_traditional_count)

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    min_wayne_traditional = model.eval(wayne_traditional_count)
    print("STATUS: sat")
    print(f"Minimum number of solos where Wayne performs a traditional piece: {min_wayne_traditional}")
    
    # Map the minimum count to the answer choice
    min_count = int(str(min_wayne_traditional))
    if min_count == 0:
        print("answer:A")
    elif min_count == 1:
        print("answer:B")
    elif min_count == 2:
        print("answer:C")
    elif min_count == 3:
        print("answer:D")
    elif min_count == 4:
        print("answer:E")
    else:
        print("STATUS: unsat")
        print("Refine: Unexpected minimum count")
elif result == unsat:
    print("STATUS: unsat")
    print("Refine: No solution exists")
else:
    print("STATUS: unknown")