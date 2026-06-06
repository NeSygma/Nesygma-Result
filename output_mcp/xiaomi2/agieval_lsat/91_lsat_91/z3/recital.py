from z3 import *

solver = Solver()

# Variables: pianist[i] = 0 (Wayne) or 1 (Zara), piece[i] = 0 (Modern) or 1 (Traditional)
N = 5
pianist = [Int(f'pianist_{i}') for i in range(N)]
piece = [Int(f'piece_{i}') for i in range(N)]

# Domain constraints
for i in range(N):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece[i] == 0, piece[i] == 1))

# Constraint 1: Solo 3 is traditional
solver.add(piece[2] == 1)

# Constraint 2: Exactly two traditional pieces are performed consecutively
# Count adjacent pairs where both are traditional; this count must be exactly 1
# (which means exactly 2 traditional pieces form a consecutive block)
adj_trad = [And(piece[i] == 1, piece[i+1] == 1) for i in range(N-1)]
solver.add(Sum([If(at, 1, 0) for at in adj_trad]) == 1)

# Constraint 3: Solo 4 - Wayne performs traditional OR Zara performs modern
solver.add(Or(
    And(pianist[3] == 0, piece[3] == 1),  # Wayne + Traditional
    And(pianist[3] == 1, piece[3] == 0)   # Zara + Modern
))

# Constraint 4: Pianist of solo 2 != pianist of solo 5
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece until Wayne performs at least one modern piece
# For each solo i that is traditional, there must exist j < i where Wayne plays modern
for i in range(N):
    # If piece[i] is traditional, then some earlier solo j has Wayne + Modern
    earlier_wayne_modern = Or([And(pianist[j] == 0, piece[j] == 0) for j in range(i)]) if i > 0 else BoolVal(False)
    solver.add(Implies(piece[i] == 1, earlier_wayne_modern))

# Additional condition: Solo 5 is traditional
solver.add(piece[4] == 1)

# First, find all valid assignments
result = solver.check()
if result != sat:
    print("STATUS: unsat")
    print("No solution found with given constraints")
else:
    m = solver.model()
    print("STATUS: sat")
    print("A valid assignment:")
    names = ["Wayne", "Zara"]
    types = ["Modern", "Traditional"]
    for i in range(N):
        p = m[pianist[i]].as_long()
        t = m[piece[i]].as_long()
        print(f"  Solo {i+1}: {names[p]}, {types[t]}")
    
    # Now determine which solos have completely determined pianists
    # For each solo, check if the pianist value is the same in ALL valid models
    determined = []
    for i in range(N):
        # Check if pianist[i] must be 0 (Wayne)
        solver.push()
        solver.add(pianist[i] == 1)  # Try Zara
        res_z = solver.check()
        solver.pop()
        
        # Check if pianist[i] must be 1 (Zara)
        solver.push()
        solver.add(pianist[i] == 0)  # Try Wayne
        res_w = solver.check()
        solver.pop()
        
        if res_z == unsat and res_w == sat:
            determined.append((i+1, "Wayne"))
        elif res_w == unsat and res_z == sat:
            determined.append((i+1, "Zara"))
        # else: not determined
    
    print(f"\nDetermined pianists: {len(determined)}")
    for solo, name in determined:
        print(f"  Solo {solo}: must be {name}")
    
    # Now evaluate the multiple choice options
    count = len(determined)
    found_options = []
    for letter, val in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
        if count == val:
            found_options.append(letter)
    
    if len(found_options) == 1:
        print(f"\nSTATUS: sat")
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print(f"\nSTATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print(f"\nSTATUS: unsat")
        print(f"Refine: No options found (count={count})")