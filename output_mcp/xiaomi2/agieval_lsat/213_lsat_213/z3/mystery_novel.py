from z3 import *

solver = Solver()

# Variables: chapter position for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Each clue assigned to a chapter 1-7
for c in clues:
    solver.add(c >= 1, c <= 7)

# All different chapters
solver.add(Distinct(clues))

# Constraint 1: T cannot be in chapter 1
solver.add(T != 1)

# Constraint 2: T before W with exactly two chapters between them => W = T + 3
solver.add(W == T + 3)

# Constraint 3: S and Z not adjacent
solver.add(Abs(S - Z) != 1)

# Constraint 4: W and X not adjacent
solver.add(Abs(W - X) != 1)

# Constraint 5: U and X must be adjacent
solver.add(Abs(U - X) == 1)

# Define each option as exact position assignments
options = {
    "A": [S==1, T==2, Z==3, X==4, U==5, W==6, R==7],
    "B": [T==1, X==2, U==3, W==4, S==5, R==6, Z==7],
    "C": [U==1, S==2, X==3, T==4, Z==5, R==6, W==7],
    "D": [X==1, U==2, T==3, Z==4, R==5, W==6, S==7],
    "E": [Z==1, R==2, T==3, U==4, X==5, W==6, S==7],
}

found_options = []
for letter, constr in options.items():
    solver.push()
    solver.add(And(constr))
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