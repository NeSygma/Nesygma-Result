from z3 import *

opt = Optimize()

# Variables: 5 solos (0-indexed: 0..4 for solos 1..5)
p = [Bool(f'p_{i}') for i in range(5)]  # True = Wayne, False = Zara
t = [Bool(f't_{i}') for i in range(5)]  # True = Traditional, False = Modern

# Constraint 1: Solo 3 (index 2) is a traditional piece
opt.add(t[2] == True)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively
# This means exactly one pair of adjacent solos are both traditional
consecutive_pairs = [If(And(t[i], t[i+1]), 1, 0) for i in range(4)]
opt.add(Sum(consecutive_pairs) == 1)

# Constraint 3: Solo 4 (index 3): Wayne performs traditional OR Zara performs modern
opt.add(Or(And(p[3], t[3]), And(Not(p[3]), Not(t[3]))))

# Constraint 4: Pianist of solo 2 (index 1) != pianist of solo 5 (index 4)
opt.add(p[1] != p[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# Solo 1 (index 0) cannot be traditional (no prior solo for Wayne to play modern)
opt.add(Not(t[0]))
# For each subsequent solo, if it's traditional, Wayne must have played modern before it
for i in range(1, 5):
    wayne_modern_before = Or([And(p[j], Not(t[j])) for j in range(i)])
    opt.add(Implies(t[i], wayne_modern_before))

# Objective: Minimize the number of solos where Wayne performs a traditional piece
wayne_trad_count = Sum([If(And(p[i], t[i]), 1, 0) for i in range(5)])
opt.minimize(wayne_trad_count)

result = opt.check()
if result == sat:
    m = opt.model()
    min_count = m.evaluate(wayne_trad_count)
    count_val = int(str(min_count))
    print("STATUS: sat")
    print(f"Minimum Wayne traditional count: {count_val}")
    
    # Print solution details
    for i in range(5):
        pianist = "Wayne" if is_true(m.evaluate(p[i])) else "Zara"
        piece_type = "Traditional" if is_true(m.evaluate(t[i])) else "Modern"
        print(f"  Solo {i+1}: {pianist}, {piece_type}")
    
    # Map to answer choice
    answer_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    if count_val in answer_map:
        print(f"answer:{answer_map[count_val]}")
    else:
        print(f"answer:UNKNOWN (count={count_val})")
else:
    print("STATUS: unsat")
    print("No valid assignment found")