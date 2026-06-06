from z3 import *

solver = Solver()

# Variables: for each solo i (1-5), who performs it and what type
# w[i] = True if Wayne performs solo i, False if Zara
# t[i] = True if solo i is Traditional, False if Modern
w = [None] + [Bool(f'w_{i}') for i in range(1, 6)]
t = [None] + [Bool(f't_{i}') for i in range(1, 6)]

# Constraint 1: The third solo is a traditional piece
solver.add(t[3] == True)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# This means exactly one pair of consecutive solos (i, i+1) are both traditional.
consecutive_pairs = [And(t[i], t[i+1]) for i in range(1, 5)]
solver.add(Sum([If(cp, 1, 0) for cp in consecutive_pairs]) == 1)

# Constraint 3: In the fourth solo, either Wayne performs a traditional piece 
# or Zara performs a modern piece
solver.add(Or(And(w[4], t[4]), And(Not(w[4]), Not(t[4]))))

# Constraint 4: The pianist who performs the second solo does not perform the fifth solo
solver.add(w[2] != w[5])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for each solo i that is traditional, there must exist some j < i where Wayne performs modern.
# Equivalently: the first traditional piece must come after at least one Wayne modern piece.
for i in range(1, 6):
    # If solo i is traditional, then there exists j < i with w[j] and not t[j]
    solver.add(Implies(t[i], Or([And(w[j], Not(t[j])) for j in range(1, i)])))

# Now check each option
# Option A: Traditional at 1, 3, 4
# Option B: Traditional at 2, 3, 4
# Option C: Traditional at 3, 4
# Option D: Traditional at 3, 5
# Option E: Traditional at 4, 5

options = {
    "A": [1, 3, 4],
    "B": [2, 3, 4],
    "C": [3, 4],
    "D": [3, 5],
    "E": [4, 5],
}

found_options = []

for letter, trad_positions in options.items():
    solver.push()
    # Set which solos are traditional and which are modern
    for i in range(1, 6):
        if i in trad_positions:
            solver.add(t[i] == True)
        else:
            solver.add(t[i] == False)
    
    if solver.check() == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter} is SAT:")
        for i in range(1, 6):
            pianist = "Wayne" if is_true(m.evaluate(w[i])) else "Zara"
            piece_type = "Traditional" if is_true(m.evaluate(t[i])) else "Modern"
            print(f"  Solo {i}: {pianist} - {piece_type}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")