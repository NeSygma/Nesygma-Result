from z3 import *

solver = Solver()

# Variables: 5 solos (0-indexed: 0=solo1, 1=solo2, ..., 4=solo5)
# pianist[i]: True = Wayne, False = Zara
# piece[i]: True = Traditional, False = Modern
pianist = [Bool(f'pianist_{i+1}') for i in range(5)]
piece = [Bool(f'piece_{i+1}') for i in range(5)]

# Constraint 1: The third solo is a traditional piece
solver.add(piece[2] == True)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively
# Count adjacent pairs (i, i+1) where both are traditional; must equal 1
consec_trad = Sum([If(And(piece[i], piece[i+1]), 1, 0) for i in range(4)])
solver.add(consec_trad == 1)

# Constraint 3: Fourth solo: Wayne+Traditional OR Zara+Modern
solver.add(Or(
    And(pianist[3], piece[3]),       # Wayne performs traditional
    And(Not(pianist[3]), Not(piece[3]))  # Zara performs modern
))

# Constraint 4: Pianist of solo 2 ≠ pianist of solo 5
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece until Wayne performs at least one modern piece
# For each solo i that is traditional, some earlier solo j must be Wayne+Modern
solver.add(Not(piece[0]))  # Solo 1 can't be traditional (no earlier solo)
for i in range(1, 5):
    earlier_wayne_modern = Or([And(pianist[j], Not(piece[j])) for j in range(i)])
    solver.add(Implies(piece[i], earlier_wayne_modern))

# Additional condition from question: Wayne performs the fifth solo as a traditional piece
solver.add(pianist[4] == True)   # Wayne
solver.add(piece[4] == True)     # Traditional

# Define answer options
options = [
    ("A", Not(pianist[0])),          # Zara performs the first solo
    ("B", pianist[1]),               # Wayne performs the second solo
    ("C", Not(pianist[2])),          # Zara performs the third solo
    ("D", Not(piece[1])),            # Second solo is a modern piece
    ("E", piece[3]),                 # Fourth solo is a traditional piece
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
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