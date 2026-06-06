from z3 import *

# Variables: chapter position for each clue (1-7)
R, S, T, U, W, X, Z = Ints('R S T U W X Z')
clues = [R, S, T, U, W, X, Z]

solver = Solver()

# Each clue assigned to a chapter 1-7, all different
for c in clues:
    solver.add(c >= 1, c <= 7)
solver.add(Distinct(clues))

# Base constraints (excluding "T cannot be in chapter 1" since we're testing replacements)
# T must be mentioned before W, exactly two chapters separating
solver.add(T + 3 == W)  # T before W with exactly 2 chapters between (e.g., T=1,W=4)

# S and Z cannot be adjacent
solver.add(Abs(S - Z) != 1)

# W and X cannot be adjacent
solver.add(Abs(W - X) != 1)

# U and X must be adjacent
solver.add(Abs(U - X) == 1)

# Now test each option as a replacement for "T != 1"
# The question: which constraint, when substituted for "T != 1", 
# would have the SAME effect in determining the order?
# This means: the set of valid orderings under the base constraints + "T != 1"
# should be EXACTLY the same as under base constraints + the new constraint.

# First, find all solutions with base + "T != 1"
def find_solutions(extra_constraint):
    s = Solver()
    for c in clues:
        s.add(c >= 1, c <= 7)
    s.add(Distinct(clues))
    s.add(T + 3 == W)
    s.add(Abs(S - Z) != 1)
    s.add(Abs(W - X) != 1)
    s.add(Abs(U - X) == 1)
    s.add(extra_constraint)
    
    solutions = []
    while s.check() == sat:
        m = s.model()
        sol = tuple(m[c].as_long() for c in clues)
        solutions.append(sol)
        s.add(Or([c != m[c] for c in clues]))
    return set(solutions)

# Solutions with T != 1
base_solutions = find_solutions(T != 1)

# Test each option
options = {
    "A": U != 2,
    "B": W != 4,
    "C": X != 6,
    "D": U < T,
    "E": X < W,
}

found_options = []
for letter, constr in options.items():
    opt_solutions = find_solutions(constr)
    if opt_solutions == base_solutions:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Debug output
print(f"\nBase solutions count: {len(base_solutions)}")
for letter, constr in options.items():
    opt_solutions = find_solutions(constr)
    print(f"Option {letter}: {len(opt_solutions)} solutions, match={opt_solutions == base_solutions}")