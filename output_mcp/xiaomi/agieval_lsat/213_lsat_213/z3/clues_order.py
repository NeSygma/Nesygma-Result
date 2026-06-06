from z3 import *

# Create solver
solver = Solver()

# Define variables: position of each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue is assigned to a chapter 1-7
for c in clues:
    solver.add(And(c >= 1, c <= 7))

# All clues are in different chapters
solver.add(Distinct(clues))

# Constraint 1: T cannot be in chapter 1
solver.add(T != 1)

# Constraint 2: T must be before W, with exactly two chapters between them
# This means W = T + 3 (e.g., T=1, W=4; T=2, W=5; T=3, W=6; T=4, W=7)
solver.add(W == T + 3)

# Constraint 3: S and Z cannot be adjacent
solver.add(Abs(S - Z) != 1)

# Constraint 4: W and X cannot be adjacent
solver.add(Abs(W - X) != 1)

# Constraint 5: U and X must be adjacent
solver.add(Abs(U - X) == 1)

# Define the answer choices as constraints
# Each option specifies the order: chapter 1 through chapter 7
opt_a = And(S == 1, T == 2, Z == 3, X == 4, U == 5, W == 6, R == 7)
opt_b = And(T == 1, X == 2, U == 3, W == 4, S == 5, R == 6, Z == 7)
opt_c = And(U == 1, S == 2, X == 3, T == 4, Z == 5, R == 6, W == 7)
opt_d = And(X == 1, U == 2, T == 3, Z == 4, R == 5, W == 6, S == 7)
opt_e = And(Z == 1, R == 2, T == 3, U == 4, X == 5, W == 6, S == 7)

# Test each option
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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