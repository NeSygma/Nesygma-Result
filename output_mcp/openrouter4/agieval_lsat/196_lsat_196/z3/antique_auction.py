from z3 import *

# Define positions (days) 1 through 6
# We'll use integer variables for each item's position
H, L, M, S, T, V = Ints('H L M S T V')
items = [H, L, M, S, T, V]

solver = Solver()

# All items distinct and in range 1-6
solver.add(Distinct(items))
for item in items:
    solver.add(item >= 1, item <= 6)

# Constraint 1: Sundial not on June 1
solver.add(S != 1)

# Constraint 2: If H < L then M < L
solver.add(Implies(H < L, M < L))

# Constraint 3: S < M and S < V
solver.add(S < M)
solver.add(S < V)

# Constraint 4: Table is earlier than harmonica or earlier than vase, but not both
# Exactly one of (T < H) or (T < V) is true
solver.add(Xor(T < H, T < V))

# Now test each option
# Each option gives a specific ordering (list of items from day 1 to day 6)

options = {
    "A": [H, T, S, L, V, M],
    "B": [L, H, S, M, V, T],
    "C": [H, S, T, M, L, V],
    "D": [S, M, H, T, V, L],
    "E": [V, S, L, H, T, M]
}

found_options = []

for letter, order in options.items():
    solver.push()
    # Each position i (0-indexed) should have the item with value i+1
    for i, item in enumerate(order):
        solver.add(item == i + 1)
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