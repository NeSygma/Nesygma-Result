from z3 import *

solver = Solver()

# Variables: for each solo (1-5), define pianist (0=Wayne, 1=Zara) and type (0=modern, 1=traditional)
pianist = [Int(f'pianist_{i}') for i in range(1, 6)]
piece_type = [Int(f'piece_type_{i}') for i in range(1, 6)]

# Domain constraints
for i in range(5):
    solver.add(Or(pianist[i] == 0, pianist[i] == 1))
    solver.add(Or(piece_type[i] == 0, piece_type[i] == 1))

# Constraint 1: The third solo is a traditional piece.
solver.add(piece_type[2] == 1)

# Constraint 2: Exactly two of the traditional pieces are performed consecutively.
# This means there is exactly one pair of consecutive solos that are both traditional,
# and no other consecutive pair is both traditional.
# Also, the total number of traditional pieces could be 2, 3, 4, or 5, but exactly
# one consecutive pair exists.

# Count consecutive traditional pairs
consecutive_pairs = []
for i in range(4):
    consecutive_pairs.append(And(piece_type[i] == 1, piece_type[i+1] == 1))

# Exactly one consecutive pair of traditional pieces
solver.add(Sum([If(cp, 1, 0) for cp in consecutive_pairs]) == 1)

# Constraint 3: In the fourth solo, either Wayne performs a traditional piece or Zara performs a modern piece.
solver.add(Or(
    And(pianist[3] == 0, piece_type[3] == 1),  # Wayne performs traditional
    And(pianist[3] == 1, piece_type[3] == 0)   # Zara performs modern
))

# Constraint 4: The pianist who performs the second solo does not perform the fifth solo.
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece is performed until Wayne performs at least one modern piece.
# This means: for any solo i that is traditional, there must exist some solo j < i where Wayne performs a modern piece.
# Equivalently: the first traditional piece must come after at least one Wayne modern piece.
# Let's find the first traditional piece position and ensure a Wayne modern exists before it.

# For each position i, if piece_type[i] is traditional, then there exists j < i with pianist[j]==Wayne and piece_type[j]==modern
for i in range(5):
    # If this is a traditional piece, then some earlier solo must be Wayne+modern
    earlier_wayne_modern = Or([And(pianist[j] == 0, piece_type[j] == 0) for j in range(i)])
    if i == 0:
        # First solo cannot be traditional (no earlier solo for Wayne modern)
        solver.add(piece_type[0] == 0)
    else:
        solver.add(Implies(piece_type[i] == 1, earlier_wayne_modern))

# Additional constraint: fifth solo is a traditional piece (given in the question)
solver.add(piece_type[4] == 1)

# Now we need to find how many solos have a completely determined pianist.
# A pianist is "completely determined" if in ALL valid solutions, that solo has the same pianist.

# First, find all valid solutions
solutions = []
decision_vars = pianist + piece_type

while solver.check() == sat:
    m = solver.model()
    sol = {}
    for v in decision_vars:
        sol[str(v)] = m.eval(v, model_completion=True).as_long()
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total valid solutions: {len(solutions)}")
for idx, sol in enumerate(solutions):
    print(f"Solution {idx+1}: {sol}")

# Now check each solo to see if the pianist is determined
determined_count = 0
determined_solos = []
for solo_idx in range(5):
    pianist_values = set(sol[f'pianist_{solo_idx+1}'] for sol in solutions)
    if len(pianist_values) == 1:
        determined_count += 1
        determined_solos.append(solo_idx + 1)
        print(f"Solo {solo_idx+1}: pianist is determined = {'Wayne' if pianist_values.pop() == 0 else 'Zara'}")
    else:
        print(f"Solo {solo_idx+1}: pianist is NOT determined (values: {pianist_values})")

print(f"\nNumber of solos with determined pianist: {determined_count}")
print(f"Determined solos: {determined_solos}")

# Now evaluate the answer choices
# (A) one, (B) two, (C) three, (D) four, (E) five
found_options = []
for letter, count in [("A", 1), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    if determined_count == count:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")