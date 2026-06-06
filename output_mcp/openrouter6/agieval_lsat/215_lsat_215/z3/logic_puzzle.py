from z3 import *

solver = Solver()

# Declare variables for each clue
R, S, T, U, W, X, Z = Ints('R S T U W X Z')

# All clues are distinct and between 1 and 7
solver.add(Distinct(R, S, T, U, W, X, Z))
solver.add([And(1 <= v, v <= 7) for v in [R, S, T, U, W, X, Z]])

# Base constraints
# T cannot be in chapter 1
solver.add(T != 1)

# T before W and exactly two chapters separating => W = T + 3
solver.add(W == T + 3)

# S and Z not adjacent
solver.add(Not(Or(S - Z == 1, S - Z == -1)))

# W and X not adjacent
solver.add(Not(Or(W - X == 1, W - X == -1)))

# U and X adjacent
solver.add(Or(U - X == 1, U - X == -1))

# U is in chapter 3
solver.add(U == 3)

# Now evaluate each option
found_options = []

# Option A: R = 1
solver.push()
solver.add(R == 1)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: R = 5
solver.push()
solver.add(R == 5)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: S = 7
solver.push()
solver.add(S == 7)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: W = 6
solver.push()
solver.add(W == 6)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: X = 4
solver.push()
solver.add(X == 4)
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