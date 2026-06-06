from z3 import *

solver = Solver()

# Declare variables for each clue's chapter
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# All clues must be in distinct chapters 1..7
solver.add(Distinct(R, S, T, U, W, X, Z))
# Each variable must be between 1 and 7 inclusive
for v in [R, S, T, U, W, X, Z]:
    solver.add(v >= 1)
    solver.add(v <= 7)

# Base constraints
solver.add(T != 1)                     # T cannot be in chapter 1
solver.add(W == T + 3)                 # Exactly two chapters between T and W
solver.add(Abs(S - Z) != 1)            # S and Z not adjacent
solver.add(Abs(W - X) != 1)            # W and X not adjacent
solver.add(Abs(U - X) == 1)            # U and X adjacent
solver.add(X == 1)                     # X is in chapter 1

# Pre-deduced constraints (optional but helpful)
# U must be 2 because X=1 and adjacent
solver.add(U == 2)

# Now evaluate each answer choice
found_options = []

# Option A: R is mentioned in chapter 3
solver.push()
solver.add(R == 3)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: R is mentioned in chapter 7
solver.push()
solver.add(R == 7)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: S is mentioned in chapter 2
solver.push()
solver.add(S == 2)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: W is mentioned in chapter 5
solver.push()
solver.add(W == 5)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Z is mentioned in chapter 3
solver.push()
solver.add(Z == 3)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")