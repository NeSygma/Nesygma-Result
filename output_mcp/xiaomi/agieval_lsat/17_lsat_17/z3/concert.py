from z3 import *

solver = Solver()

# Variables: position of each composition (1-8)
F = Int('F')
H = Int('H')
L = Int('L')
O = Int('O')
P = Int('P')
R = Int('R')
S = Int('S')
T = Int('T')

comps = [F, H, L, O, P, R, S, T]
names = ['F', 'H', 'L', 'O', 'P', 'R', 'S', 'T']

# All positions are between 1 and 8
for c in comps:
    solver.add(c >= 1, c <= 8)

# All distinct
solver.add(Distinct(comps))

# Given: P is performed third and S is performed sixth
solver.add(P == 3)
solver.add(S == 6)

# Condition 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Condition 2: At least two compositions are performed either after F and before R, or after R and before F
# This means |pos(F) - pos(R)| >= 3 (at least 2 compositions between them)
solver.add(Or(F - R >= 3, R - F >= 3))

# Condition 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Condition 4: The eighth composition performed is either L or H
solver.add(Or(L == 8, H == 8))

# Condition 5: P is performed at some time before S
solver.add(P < S)  # Already satisfied: P=3 < S=6

# Condition 6: At least one composition is performed either after O and before S, or after S and before O
# This means |pos(O) - pos(S)| >= 2
solver.add(Or(O - S >= 2, S - O >= 2))

# Now test each answer choice for what must be in position 5
# The question: "the composition performed fifth must be either"
# We need to find which option is necessarily true (i.e., for ALL valid solutions)

# First, let's find all valid solutions and see what's in position 5
# We'll enumerate solutions and track what appears in position 5

# Create a variable for position 5
pos5 = Int('pos5')

# For each composition, check if it can be in position 5
# We need to find which compositions MUST be in position 5 across all solutions

# Let's check each option by seeing if the negation is unsatisfiable
# i.e., if we can prove that NOT(option) leads to unsat, then option is necessary

options = {
    "A": Or(pos5 == F, pos5 == H),  # F or H
    "B": Or(pos5 == F, pos5 == O),  # F or O
    "C": Or(pos5 == F, pos5 == T),  # F or T
    "D": Or(pos5 == H, pos5 == L),  # H or L
    "E": Or(pos5 == O, pos5 == R),  # O or R
}

# We need to find which composition is at position 5
# pos5 is the composition whose position is 5
# So pos5 == X means X is at position 5
# We need: for each composition X, X == 5 iff pos5 == X
# Actually, let's just directly check: what value is at position 5?
# We can use: Or([And(pos5 == c, c == 5) for c in comps])
# But simpler: pos5 is the composition at position 5
# So we need: for each composition c, (c == 5) iff (pos5 == c)
# Let's just enumerate and check

# Actually, let's just find all solutions and see what's at position 5
solutions = []
decision_vars = comps  # All composition positions

while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m.eval(v, model_completion=True) for v in decision_vars}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions found: {len(solutions)}")

# Find what's at position 5 in each solution
pos5_values = []
for sol in solutions:
    for name in names:
        if sol[name].as_long() == 5:
            pos5_values.append(name)
            break

print(f"Compositions at position 5: {pos5_values}")

# Now check which options are always true
# An option is "must be" if in ALL solutions, position 5 is one of the two compositions
option_valid = {}
for letter, (c1, c2) in [("A", ("F", "H")), ("B", ("F", "O")), ("C", ("F", "T")), ("D", ("H", "L")), ("E", ("O", "R"))]:
    all_valid = all(p in [c1, c2] for p in pos5_values)
    option_valid[letter] = all_valid
    print(f"Option {letter} ({c1} or {c2}): {'Always valid' if all_valid else 'Not always valid'}")

# Find which options are always valid
valid_options = [letter for letter, valid in option_valid.items() if valid]
print(f"Valid options: {valid_options}")

if len(valid_options) == 1:
    print("STATUS: sat")
    print(f"answer:{valid_options[0]}")
elif len(valid_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {valid_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")