from z3 import *

solver = Solver()

# There are 5 solos, indexed 0..4
pianist = [Int(f'p_{i}') for i in range(5)]
piece   = [Int(f'g_{i}') for i in range(5)]

# Domains
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Condition 1: The third solo (index 2) is a traditional piece.
solver.add(piece[2] == 1)

# Condition 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive traditional solos.
consec_pairs = [And(piece[i] == 1, piece[i+1] == 1) for i in range(4)]
solver.add(Sum([If(consec_pairs[i], 1, 0) for i in range(4)]) == 1)

# Condition 3: In the fourth solo (index 3), either Wayne performs a traditional piece
# or Zara performs a modern piece.
solver.add(Or(And(pianist[3] == 0, piece[3] == 1),
              And(pianist[3] == 1, piece[3] == 0)))

# Condition 4: The pianist who performs the second solo (index 1) does not perform the fifth solo (index 4).
solver.add(pianist[1] != pianist[4])

# Condition 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each i, if piece[i]==1 then there exists j < i with pianist[j]==0 and piece[j]==0.
for i in range(5):
    if i == 0:
        solver.add(piece[0] == 0)
    else:
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Let's first check if the base constraints are satisfiable at all.
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("SAT - base model found")
    for i in range(5):
        print(f"Solo {i+1}: pianist={'Wayne' if m[pianist[i]]==0 else 'Zara'}, piece={'modern' if m[piece[i]]==0 else 'traditional'}")
else:
    print("UNSAT - base constraints unsatisfiable")
    exit()

# Now let's find the minimum number of Wayne traditional solos.
# We'll use optimization to find the minimum.
solver2 = Solver()
for i in range(5):
    solver2.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver2.add(Or(piece[i] == 0, piece[i] == 1))

solver2.add(piece[2] == 1)
solver2.add(Sum([If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]) == 1)
solver2.add(Or(And(pianist[3] == 0, piece[3] == 1),
               And(pianist[3] == 1, piece[3] == 0)))
solver2.add(pianist[1] != pianist[4])
for i in range(5):
    if i == 0:
        solver2.add(piece[0] == 0)
    else:
        earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
        solver2.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))

# Count Wayne's traditional solos
wayne_trad_count = Sum([If(And(pianist[i] == 0, piece[i] == 1), 1, 0) for i in range(5)])

# Try each possible count to find the minimum feasible
for k in range(6):
    s = Solver()
    # Add all base constraints
    for i in range(5):
        s.add(Or(pianist[i] == 0, pianist[i] == 1))
        s.add(Or(piece[i] == 0, piece[i] == 1))
    s.add(piece[2] == 1)
    s.add(Sum([If(And(piece[i] == 1, piece[i+1] == 1), 1, 0) for i in range(4)]) == 1)
    s.add(Or(And(pianist[3] == 0, piece[3] == 1),
               And(pianist[3] == 1, piece[3] == 0)))
    s.add(pianist[1] != pianist[4])
    for i in range(5):
        if i == 0:
            s.add(piece[0] == 0)
        else:
            earlier_wayne_modern = [And(pianist[j] == 0, piece[j] == 0) for j in range(i)]
            s.add(Implies(piece[i] == 1, Or(earlier_wayne_modern)))
    
    s.add(wayne_trad_count == k)
    if s.check() == sat:
        print(f"Count = {k} is feasible")
        m = s.model()
        for i in range(5):
            print(f"  Solo {i+1}: pianist={'Wayne' if m[pianist[i]]==0 else 'Zara'}, piece={'modern' if m[piece[i]]==0 else 'traditional'}")
    else:
        print(f"Count = {k} is NOT feasible")