from z3 import *

# Create solver
solver = Solver()

# Define variables
# For each position 1-5, we have pianist (0=Wayne, 1=Zara) and type (0=modern, 1=traditional)
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]  # 1-5
piece_type = [Int(f'piece_type_{i}') for i in range(1, 6)]  # 1-5

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))  # Wayne or Zara
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))  # modern or traditional

# Constraint 1: Third solo is traditional
solver.add(piece_type[2] == 1)  # position 3 (index 2)

# Constraint 2: Exactly two traditional pieces are performed consecutively
# We need to count consecutive traditional pairs
# For positions 1-2, 2-3, 3-4, 4-5
consecutive_traditional = []
for i in range(4):
    # Check if positions i and i+1 are both traditional
    is_consecutive = If(And(piece_type[i] == 1, piece_type[i+1] == 1), 1, 0)
    consecutive_traditional.append(is_consecutive)

# Exactly one consecutive pair (since exactly two traditional pieces are consecutive)
solver.add(Sum(consecutive_traditional) == 1)

# Constraint 3: Fourth solo: either Wayne performs traditional OR Zara performs modern
# Position 4: index 3
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, piece_type[3] == 0)   # Zara performs modern
))

# Constraint 4: Pianist who performs second solo does not perform fifth solo
solver.add(pianist[1] != pianist[4])  # position 2 vs position 5

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece
# This means: before any traditional piece appears, Wayne must have performed at least one modern piece
# We need to ensure that if a traditional piece appears at position i, then there exists some position j < i
# where pianist[j] == 0 (Wayne) and piece_type[j] == 0 (modern)
for i in range(5):
    if piece_type[i] == 1:  # if this position is traditional
        # Check if there's a Wayne modern piece before this position
        has_earlier_wayne_modern = False
        for j in range(i):
            has_earlier_wayne_modern = Or(has_earlier_wayne_modern, 
                                         And(pianist[j] == 0, piece_type[j] == 0))
        # If this is the first traditional piece, we need Wayne modern before it
        # But we need to be careful: the constraint says "until Wayne performs at least one modern piece"
        # So if there's any traditional piece before Wayne's modern, that's invalid
        # Actually, let's rephrase: For all positions i, if piece_type[i] == 1 (traditional),
        # then there must exist some j < i with pianist[j] == 0 and piece_type[j] == 0
        if i > 0:  # can't have traditional at position 1 unless Wayne performed modern before (impossible)
            # So position 1 cannot be traditional
            solver.add(Implies(piece_type[i] == 1, 
                             Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])))

# Actually, let's implement constraint 5 more carefully:
# "No traditional piece is performed until Wayne performs at least one modern piece"
# This means: The first traditional piece must occur AFTER Wayne has performed at least one modern piece
# So we need to find the first position where piece_type == 1 (traditional)
# And ensure that before that position, there's at least one position where pianist == 0 and piece_type == 0

# Let's define: first_traditional_pos = minimum i where piece_type[i] == 1
# And Wayne_modern_before = exists j < first_traditional_pos where pianist[j] == 0 and piece_type[j] == 0

# We can model this by ensuring that for each position i, if it's traditional,
# then either it's not the first traditional, or there's a Wayne modern before it

# Alternative approach: For each position i, if it's traditional, then either:
# 1. There's a traditional piece before it (so it's not the first), OR
# 2. There's a Wayne modern piece before it

for i in range(5):
    if i == 0:  # position 1
        # Cannot be traditional because no positions before it
        solver.add(piece_type[i] == 0)  # position 1 must be modern
    else:
        # If position i is traditional, then either:
        # a) There's a traditional piece before it, OR
        # b) There's a Wayne modern piece before it
        has_traditional_before = Or([piece_type[j] == 1 for j in range(i)])
        has_wayne_modern_before = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
        solver.add(Implies(piece_type[i] == 1, Or(has_traditional_before, has_wayne_modern_before)))

# Now we need to count how many solos Wayne performs a traditional piece
# That is: count positions where pianist[i] == 0 and piece_type[i] == 1
wayne_traditional_count = Sum([If(And(pianist[i] == 0, piece_type[i] == 1), 1, 0) for i in range(5)])

# Now test each answer choice
found_options = []

# Option A: zero (minimum is 0)
solver.push()
solver.add(wayne_traditional_count == 0)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: one (minimum is 1)
solver.push()
solver.add(wayne_traditional_count == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: two (minimum is 2)
solver.push()
solver.add(wayne_traditional_count == 2)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: three (minimum is 3)
solver.push()
solver.add(wayne_traditional_count == 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: four (minimum is 4)
solver.push()
solver.add(wayne_traditional_count == 4)
if solver.check() == sat:
    found_options.append("E")
solver.pop()

# Print results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")