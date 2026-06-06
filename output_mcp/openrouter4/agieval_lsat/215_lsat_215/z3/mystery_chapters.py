from z3 import *

solver = Solver()

# Variables: chapter numbers (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Domain: each clue in 1..7
for v in clues:
    solver.add(v >= 1, v <= 7)

# All different
solver.add(Distinct(clues))

# Constraint 1: T != 1
solver.add(T != 1)

# Constraint 2: T before W, exactly two chapters separating
# So W = T + 3
solver.add(W == T + 3)

# Constraint 3: S and Z not adjacent
solver.add(Or(S - Z != 1, Z - S != 1))
solver.add(Abs(S - Z) != 1)  # use Abs

# Constraint 4: W and X not adjacent
solver.add(Abs(W - X) != 1)

# Constraint 5: U and X adjacent
solver.add(Abs(U - X) == 1)

# Given: U is in chapter 3
solver.add(U == 3)

# Options
options = [
    ("A", R == 1),
    ("B", R == 5),
    ("C", S == 7),
    ("D", W == 6),
    ("E", X == 4)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
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