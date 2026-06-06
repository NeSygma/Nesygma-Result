from z3 import *

# Let's verify count=0 more carefully. The model for count=0 had:
# Solo 1: Wayne modern
# Solo 2: Zara traditional
# Solo 3: Zara traditional
# Solo 4: Zara modern
# Solo 5: Wayne modern

# Check condition 2: Exactly two traditional pieces are performed consecutively.
# Traditional pieces are at indices 1 and 2 (solos 2 and 3). That's one consecutive pair.
# Are there any other consecutive traditional pairs? No. So exactly 1 pair. Good.

# Check condition 3: Fourth solo (index 3): Zara modern. That satisfies "Zara performs a modern piece". Good.

# Check condition 4: Second solo (index 1) is Zara, fifth solo (index 4) is Wayne. Different. Good.

# Check condition 5: No traditional piece until Wayne performs at least one modern piece.
# Wayne performs modern at solo 1 (index 0). So traditional pieces at indices 1,2 are after that. Good.

# But wait - condition 5 says "No traditional piece is performed until Wayne performs at least one modern piece."
# This means the FIRST traditional piece must come AFTER Wayne's first modern piece.
# In the count=0 model, Wayne's first modern is at solo 1, and the first traditional is at solo 2. That's fine.

# So count=0 seems valid. Let me double-check by running the multiple choice evaluation.

solver = Solver()

pianist = [Int(f'p_{i}') for i in range(5)]
piece   = [Int(f'g_{i}') for i in range(5)]

for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1
solver.add(piece[2] == 1)

# Condition 2: Exactly one pair of consecutive traditional pieces
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3
solver.add(Or(And(pianist[3] == 0, piece[3] == 1),
              And(pianist[3] == 1, piece[3] == 0)))

# Condition 4
solver.add(pianist[1] != pianist[4])

# Condition 5
for i in range(5):
    if i == 0:
        solver.add(piece[0] == 0)
    else:
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Count Wayne's traditional solos
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

# Evaluate each option
found_options = []

# Option A: zero
solver.push()
solver.add(wayne_trad_count == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: one
solver.push()
solver.add(wayne_trad_count == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: two
solver.push()
solver.add(wayne_trad_count == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: three
solver.push()
solver.add(wayne_trad_count == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: four
solver.push()
solver.add(wayne_trad_count == 4)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

print(f"Found options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")