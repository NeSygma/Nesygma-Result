from z3 import *

# Create solver
solver = Solver()

# Define chapters 1-7
chapters = [1, 2, 3, 4, 5, 6, 7]

# Create variables for each clue's chapter
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')

# All clues must be in chapters 1-7
clues = [R, S, T, U, W, X, Z]
for clue in clues:
    solver.add(clue >= 1)
    solver.add(clue <= 7)

# All clues must be in different chapters (each chapter has exactly one clue)
solver.add(Distinct(clues))

# Constraint 1: T cannot be in chapter 1
solver.add(T != 1)

# Constraint 2: T must be before W, with exactly two chapters separating them
# So if T is in chapter i, W must be in chapter i+3
# This means T can be in chapters 1-4 (since W must be ≤7)
# We'll use an OR constraint for all possible positions
solver.add(Or(
    And(T == 1, W == 4),
    And(T == 2, W == 5),
    And(T == 3, W == 6),
    And(T == 4, W == 7)
))

# Constraint 3: S and Z cannot be adjacent
# Adjacent means |S - Z| = 1
solver.add(Not(Or(S == Z + 1, S == Z - 1)))

# Constraint 4: W and X cannot be adjacent
solver.add(Not(Or(W == X + 1, W == X - 1)))

# Constraint 5: U and X must be adjacent
solver.add(Or(U == X + 1, U == X - 1))

# Now test each answer choice
found_options = []

# Answer A: S, T, Z, X, U, W, R
# This means: S=1, T=2, Z=3, X=4, U=5, W=6, R=7
opt_a = And(S == 1, T == 2, Z == 3, X == 4, U == 5, W == 6, R == 7)

# Answer B: T, X, U, W, S, R, Z
# This means: T=1, X=2, U=3, W=4, S=5, R=6, Z=7
opt_b = And(T == 1, X == 2, U == 3, W == 4, S == 5, R == 6, Z == 7)

# Answer C: U, S, X, T, Z, R, W
# This means: U=1, S=2, X=3, T=4, Z=5, R=6, W=7
opt_c = And(U == 1, S == 2, X == 3, T == 4, Z == 5, R == 6, W == 7)

# Answer D: X, U, T, Z, R, W, S
# This means: X=1, U=2, T=3, Z=4, R=5, W=6, S=7
opt_d = And(X == 1, U == 2, T == 3, Z == 4, R == 5, W == 6, S == 7)

# Answer E: Z, R, T, U, X, W, S
# This means: Z=1, R=2, T=3, U=4, X=5, W=6, S=7
opt_e = And(Z == 1, R == 2, T == 3, U == 4, X == 5, W == 6, S == 7)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

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