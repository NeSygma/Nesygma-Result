from z3 import *

solver = Solver()

# Variables: for each solo (1-5), which pianist and which type
# pianist[i] = 0 for Wayne, 1 for Zara
# piece[i] = 0 for modern, 1 for traditional
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece = [Int(f'piece_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Constraint 1: The third solo is a traditional piece.
solver.add(piece[2] == 1)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive solos that are both traditional,
# and no other consecutive pair is both traditional.
consec_trad = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(ct, 1, 0) for ct in consec_trad]) == 1)

# Constraint 3: In the fourth solo, either Wayne performs a traditional piece
# or Zara performs a modern piece.
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),  # Wayne traditional
    And(pianist[3] == 1, piece[3] == 0)   # Zara modern
))

# Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
for i in range(5):
    if i == 0:
        solver.add(piece[0] == 0)
    else:
        earlier_wayne_modern = Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)])
        solver.add(Implies(piece[i] == 1, earlier_wayne_modern))

# Wayne traditional count
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

# Use Optimize to find the MINIMUM
opt = Optimize()
opt.add(solver.assertions())
opt.minimize(wayne_trad_count)

result = opt.check()
if result == sat:
    m = opt.model()
    print("STATUS: sat")
    min_count = m.evaluate(wayne_trad_count)
    print(f"Minimum Wayne traditional count: {min_count}")
    for i in range(5):
        p_val = m.evaluate(pianist[i])
        pc_val = m.evaluate(piece[i])
        pname = "Wayne" if str(p_val) == "0" else "Zara"
        pcname = "modern" if str(pc_val) == "0" else "traditional"
        print(f"Solo {i+1}: {pname} - {pcname}")
    
    # Map to answer
    count = int(str(min_count))
    if count == 0:
        print("answer:A")
    elif count == 1:
        print("answer:B")
    elif count == 2:
        print("answer:C")
    elif count == 3:
        print("answer:D")
    elif count == 4:
        print("answer:E")
else:
    print("STATUS: unsat")