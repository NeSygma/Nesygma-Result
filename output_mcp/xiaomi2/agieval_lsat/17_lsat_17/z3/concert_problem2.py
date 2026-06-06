from z3 import *

solver = Solver()

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

for c in comps:
    solver.add(c >= 1, c <= 8)

solver.add(Distinct(comps))

# Given: P is third, S is sixth
solver.add(P == 3)
solver.add(S == 6)

# Constraint 1: T is performed either immediately before F or immediately after R
solver.add(Or(T + 1 == F, R + 1 == T))

# Constraint 2: At least two compositions between F and R (|F-R| >= 3)
solver.add(Or(F - R >= 3, R - F >= 3))

# Constraint 3: O is performed either first or fifth
solver.add(Or(O == 1, O == 5))

# Constraint 4: The eighth composition is either L or H
solver.add(Or(L == 8, H == 8))

# Constraint 5: P < S (already satisfied)
solver.add(P < S)

# Constraint 6: At least one composition between O and S (|O-S| >= 2)
solver.add(Or(O - S >= 2, S - O >= 2))

# Enumerate all solutions
solutions = []
decision_vars = [F, H, L, O, R, T]  # P=3, S=6 are fixed

while solver.check() == sat:
    m = solver.model()
    sol = {}
    for v in decision_vars:
        sol[str(v)] = m.eval(v, model_completion=True).as_long()
    sol['P'] = 3
    sol['S'] = 6
    solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v, model_completion=True) for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")
print()

# Check what's at position 5 in each solution
pos5_values = set()
for sol in solutions:
    for name, pos in sol.items():
        if pos == 5:
            pos5_values.add(name)
    print(sol)

print(f"\nValues at position 5 across all solutions: {pos5_values}")

# Now check each answer choice: which one MUST be true?
# (A) F or H at position 5
# (B) F or O at position 5
# (C) F or T at position 5
# (D) H or L at position 5
# (E) O or R at position 5

options = {
    'A': {'F', 'H'},
    'B': {'F', 'O'},
    'C': {'F', 'T'},
    'D': {'H', 'L'},
    'E': {'O', 'R'},
}

for letter, vals in options.items():
    # Check if pos5_values is a subset of vals (i.e., MUST be one of these)
    if pos5_values.issubset(vals):
        print(f"Option {letter} ({vals}) MUST be true - covers all pos5 values")
    else:
        print(f"Option {letter} ({vals}) does NOT cover all pos5 values")