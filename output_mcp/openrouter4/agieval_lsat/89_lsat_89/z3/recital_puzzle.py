from z3 import *

# Five solos, indexed 0..4
# pianist[i] = True if Wayne, False if Zara
# piece[i] = True if Traditional, False if Modern

pianist = [Bool(f'pianist_{i}') for i in range(5)]
piece = [Bool(f'piece_{i}') for i in range(5)]

solver = Solver()

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == True)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive traditional pieces.
consec_pairs = [i for i in range(4)]
solver.add(Sum([If(And(piece[i], piece[i+1]), 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
# Wayne performs traditional: pianist[3] == True and piece[3] == True
# Zara performs modern: pianist[3] == False and piece[3] == False
solver.add(Or(And(pianist[3], piece[3]), And(Not(pianist[3]), Not(piece[3]))))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each index i where piece[i] is True, there must exist some j < i such that
# pianist[j] is True and piece[j] is False.
for i in range(5):
    solver.add(Implies(piece[i], Or([And(pianist[j], Not(piece[j])) for j in range(i)])))

# Count of Wayne's traditional solos
count_wayne_trad = Sum([If(And(pianist[i], piece[i]), 1, 0) for i in range(5)])

# Use optimization to find the minimum number of Wayne traditional solos
opt = Optimize()
# Add all constraints from solver to opt
for c in solver.assertions():
    opt.add(c)

opt.minimize(count_wayne_trad)

result = opt.check()

if result == sat:
    m = opt.model()
    min_val = m.eval(count_wayne_trad)
    min_val_int = min_val.as_long()
    
    # Map to answer letter
    if min_val_int == 0:
        answer_letter = 'A'
    elif min_val_int == 1:
        answer_letter = 'B'
    elif min_val_int == 2:
        answer_letter = 'C'
    elif min_val_int == 3:
        answer_letter = 'D'
    elif min_val_int == 4:
        answer_letter = 'E'
    else:
        answer_letter = '?'
    
    print("STATUS: sat")
    print(f"Minimum number of Wayne traditional solos: {min_val_int}")
    print(f"answer:{answer_letter}")
    
    # Also print the model for verification
    print("\nModel (pianist: True=Wayne, False=Zara; piece: True=Traditional, False=Modern):")
    for i in range(5):
        pn = "Wayne" if m.eval(pianist[i]) else "Zara"
        pt = "Traditional" if m.eval(piece[i]) else "Modern"
        print(f"  Solo {i+1}: {pn} performs {pt}")
else:
    print("STATUS: unsat")
    print("No solution found")