from z3 import *

solver = Solver()

# Variables for chapter numbers (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

# Domain constraints
for c in clues:
    solver.add(c >= 1, c <= 7)

# All distinct
solver.add(Distinct(clues))

# Constraints
solver.add(T != 1)  # T cannot be chapter 1
solver.add(T < W)   # T before W
solver.add(W - T == 3)  # exactly two chapters between T and W

# Adjacency constraints
solver.add(Abs(S - Z) != 1)  # S and Z not adjacent
solver.add(Abs(W - X) != 1)  # W and X not adjacent
solver.add(Abs(U - X) == 1)  # U and X must be adjacent

# Premise: X is mentioned in chapter 1
solver.add(X == 1)

# Base check
print("Base constraints + X=1 check...")
base_result = solver.check()
if base_result == sat:
    print("Base is SAT")
    m = solver.model()
    for c in clues:
        print(f"  {c} = {m[c]}")
else:
    print("Base is UNSAT")

# Now evaluate each option
options = {
    "A": R == 3,
    "B": R == 7,
    "C": S == 2,
    "D": W == 5,
    "E": Z == 3
}

found_options = []
for letter, constr in options.items():
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