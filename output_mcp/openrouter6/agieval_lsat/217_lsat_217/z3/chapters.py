from z3 import *

solver = Solver()

# Variables for each clue
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Domain constraints: each clue in 1..7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All clues distinct
solver.add(Distinct(clues))

# T cannot be in chapter 1
solver.add(T != 1)

# T before W and exactly two chapters between them: W = T + 3
solver.add(W == T + 3)

# S and Z not adjacent
solver.add(Or(S - Z != 1, Z - S != 1))  # equivalent to |S-Z| != 1
# Actually simpler: Not(Or(S == Z+1, S == Z-1))
solver.add(Not(Or(S == Z+1, S == Z-1)))

# W and X not adjacent
solver.add(Not(Or(W == X+1, W == X-1)))

# U and X adjacent
solver.add(Or(U == X+1, U == X-1))

# Base constraints added

# Now test each option
found_options = []

# Option A: R is mentioned in chapter 7
solver.push()
solver.add(R == 7)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: T is mentioned in chapter 5
solver.push()
solver.add(T == 5)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: U is mentioned in chapter 7
solver.push()
solver.add(U == 7)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: W is mentioned in chapter 3
solver.push()
solver.add(W == 3)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: X is mentioned in chapter 6
solver.push()
solver.add(X == 6)
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