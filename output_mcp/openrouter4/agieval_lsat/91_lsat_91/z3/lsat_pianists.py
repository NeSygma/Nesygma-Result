from z3 import *

solver = Solver()

# Variables: solo 1 through 5
pianist = [Bool(f'p_{i}') for i in range(1, 6)]  # True = Wayne, False = Zara
type_ = [Bool(f't_{i}') for i in range(1, 6)]    # True = Traditional, False = Modern

# Constraint 1: The third solo is a traditional piece.
solver.add(type_[2] == True)  # index 2 = third solo (0-indexed: 0,1,2,3,4)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# Count adjacent pairs of T's
adj_pairs = []
for i in range(4):
    adj_pairs.append(If(And(type_[i] == True, type_[i+1] == True), 1, 0))
solver.add(Sum(adj_pairs) == 1)

# Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
# solo 4 = index 3
solver.add(Or(
    And(pianist[3] == True, type_[3] == True),
    And(pianist[3] == False, type_[3] == False)
))

# Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
# solo 2 = index 1, solo 5 = index 4
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# For each solo i, if it's T, then there exists some earlier solo j where pianist=W and type=M.
for i in range(5):
    # Build list of earlier solos j < i where pianist_j == True and type_j == False (Modern)
    earlier_wayne_modern = []
    for j in range(i):
        earlier_wayne_modern.append(And(pianist[j] == True, type_[j] == False))
    # If no earlier solos exist, this constraint is trivially unsatisfiable if type_i is T
    # Actually for i=0 (first solo), there are no earlier solos, so if type_0 == T, it's impossible.
    # We'll add: if type_i is T, then there must be at least one earlier Wayne-modern.
    if earlier_wayne_modern:
        solver.add(Implies(type_[i] == True, Or(earlier_wayne_modern)))
    else:
        # i=0: first solo cannot be traditional (since no earlier Wayne-modern possible)
        solver.add(type_[0] == False)

# Additional condition: the fifth solo is a traditional piece.
solver.add(type_[4] == True)

# Now let's first check satisfiability of the base model
print("Checking base model (with type_5=T)...")
result = solver.check()
if result == sat:
    print("Base model is SAT")
    m = solver.model()
    for i in range(5):
        p = "Wayne" if m[pianist[i]] else "Zara"
        t = "Traditional" if m[type_[i]] else "Modern"
        print(f"  Solo {i+1}: {p}, {t}")
else:
    print("Base model is UNSAT")
    # Let's debug by checking without the additional condition
    solver.pop()  # remove type_5 == True? Actually we need to pop the last constraint
    # But we didn't push, so let's just rebuild
    exit()

# Now determine for each solo whether pianist is forced
determined_count = 0
determined_solos = []
for i in range(5):
    # Can pianist be Wayne?
    solver.push()
    solver.add(pianist[i] == True)
    wayne_possible = solver.check() == sat
    solver.pop()
    
    # Can pianist be Zara?
    solver.push()
    solver.add(pianist[i] == False)
    zara_possible = solver.check() == sat
    solver.pop()
    
    if wayne_possible and not zara_possible:
        determined_count += 1
        determined_solos.append((i+1, "Wayne"))
        print(f"Solo {i+1}: pianist forced to Wayne")
    elif zara_possible and not wayne_possible:
        determined_count += 1
        determined_solos.append((i+1, "Zara"))
        print(f"Solo {i+1}: pianist forced to Zara")
    else:
        print(f"Solo {i+1}: pianist not determined (Wayne: {wayne_possible}, Zara: {zara_possible})")

print(f"\nDetermined count: {determined_count}")
print(f"Determined solos: {determined_solos}")

# Now evaluate options
found_options = []
for letter, constr_val in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    solver.add(determined_count == constr_val)
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