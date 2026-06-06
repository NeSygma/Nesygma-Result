from z3 import *

# Base constraints solver
solver = Solver()

# Variables: chapter position for each clue (1-7)
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')

# Each clue appears exactly once in chapters 1-7
solver.add(Distinct([R, S, T, U, W, X, Z]))
solver.add(R >= 1, R <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(U >= 1, U <= 7)
solver.add(W >= 1, W <= 7)
solver.add(X >= 1, X <= 7)
solver.add(Z >= 1, Z <= 7)

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(T != 1)

# Constraint 2: T must be mentioned before W
solver.add(T < W)

# Constraint 3: Exactly two chapters separating T and W (W = T + 3)
solver.add(W == T + 3)

# Constraint 4: S and Z cannot be mentioned in adjacent chapters
solver.add(Not(Or(S == Z + 1, Z == S + 1)))

# Constraint 5: W and X cannot be mentioned in adjacent chapters
solver.add(Not(Or(W == X + 1, X == W + 1)))

# Constraint 6: U and X must be mentioned in adjacent chapters
solver.add(Or(U == X + 1, X == U + 1))

# Now evaluate each option
found_options = []

# Option A: S, T, Z, X, U, W, R
solver.push()
solver.add(S == 1)
solver.add(T == 2)
solver.add(Z == 3)
solver.add(X == 4)
solver.add(U == 5)
solver.add(W == 6)
solver.add(R == 7)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: T, X, U, W, S, R, Z
solver.push()
solver.add(T == 1)
solver.add(X == 2)
solver.add(U == 3)
solver.add(W == 4)
solver.add(S == 5)
solver.add(R == 6)
solver.add(Z == 7)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: U, S, X, T, Z, R, W
solver.push()
solver.add(U == 1)
solver.add(S == 2)
solver.add(X == 3)
solver.add(T == 4)
solver.add(Z == 5)
solver.add(R == 6)
solver.add(W == 7)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: X, U, T, Z, R, W, S
solver.push()
solver.add(X == 1)
solver.add(U == 2)
solver.add(T == 3)
solver.add(Z == 4)
solver.add(R == 5)
solver.add(W == 6)
solver.add(S == 7)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Z, R, T, U, X, W, S
solver.push()
solver.add(Z == 1)
solver.add(R == 2)
solver.add(T == 3)
solver.add(U == 4)
solver.add(X == 5)
solver.add(W == 6)
solver.add(S == 7)
if solver.check() == sat:
    found_options.append("E")
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