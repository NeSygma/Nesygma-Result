from z3 import *

# The problem asks: "What is the minimum number of solos in which Wayne performs a traditional piece?"
# So we need to find the minimum possible value. Let's use optimization.

opt = Optimize()

pianist = [Int(f'p_{i}') for i in range(5)]
piece   = [Int(f'g_{i}') for i in range(5)]

for i in range(5):
    opt.add(Or(pianist[i] == 0, pianist[i] == 1))
    opt.add(Or(piece[i] == 0, piece[i] == 1))

# 0 = Wayne, 1 = Zara
# 0 = modern, 1 = traditional

# Condition 1: The third solo is a traditional piece.
opt.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means exactly one pair of consecutive traditional pieces.
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
opt.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
opt.add(Or(And(pianist[3] == 0, piece[3] == 1),
           And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo does not perform the fifth solo.
opt.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for any traditional piece at position i, there must be some earlier position j < i
# where Wayne performs a modern piece.
for i in range(5):
    earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
    opt.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Count Wayne's traditional solos
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

# Minimize
opt.minimize(wayne_trad_count)

result = opt.check()

if result == sat:
    m = opt.model()
    min_val = m.eval(wayne_trad_count)
    print(f"Minimum Wayne traditional solos: {min_val}")
    print("Solution:")
    for i in range(5):
        p = "Wayne" if m[pianist[i]] == 0 else "Zara"
        g = "modern" if m[piece[i]] == 0 else "traditional"
        print(f"  Solo {i+1}: {p} plays {g}")
    
    # Map to answer choice
    val = min_val.as_long()
    mapping = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
    print("STATUS: sat")
    print(f"answer:{mapping[val]}")
else:
    print(f"Result: {result}")