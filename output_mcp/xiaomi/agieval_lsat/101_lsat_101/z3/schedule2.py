from z3 import *

solver = Solver()

# Variables: day assignment for each witness (0=Monday, 1=Tuesday, 2=Wednesday)
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

witnesses = [Franco, Garcia, Hong, Iturbe, Jackson]
names = ['Franco', 'Garcia', 'Hong', 'Iturbe', 'Jackson']

# Each witness testifies on exactly one day (0, 1, or 2)
for w in witnesses:
    solver.add(Or(w == 0, w == 1, w == 2))

# Franco does not testify on the same day as Garcia
solver.add(Franco != Garcia)

# Iturbe testifies on Wednesday
solver.add(Iturbe == 2)

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Hong does not testify on Monday
solver.add(Hong != 0)

# At least one witness testifies on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Jackson is the only witness scheduled to testify on Monday
solver.add(Jackson == 0)
solver.add(Franco != 0)
solver.add(Garcia != 0)
solver.add(Hong != 0)
solver.add(Iturbe != 0)

# Let's first see what the base constraints imply
# With Jackson on Monday (alone), Iturbe on Wednesday,
# exactly 2 on Tuesday, and Hong not on Monday,
# the remaining 3 (Franco, Garcia, Hong) must fill:
# - Tuesday: exactly 2 witnesses
# - Wednesday: remaining witnesses (besides Iturbe)
# Hong can only be Tuesday or Wednesday
# Franco and Garcia must be different days

# Let's enumerate all valid models
solutions = []
decision_vars = [Franco, Garcia, Hong]
while solver.check() == sat:
    m = solver.model()
    sol = {str(v): m[v] for v in decision_vars}
    solutions.append(sol)
    solver.add(Or([v != m[v] for v in decision_vars]))

print(f"Total solutions: {len(solutions)}")
for i, s in enumerate(solutions):
    print(f"Solution {i+1}: {s}")

# Now check which options MUST be true (true in ALL solutions)
options = {
    "A": lambda s: s['Franco'] == 2,  # Franco on Wednesday
    "B": lambda s: s['Hong'] == 1,    # Hong on Tuesday
    "C": lambda s: s['Garcia'] == 1,  # Garcia on Tuesday
    "D": lambda s: s['Franco'] == s['Hong'],  # Franco same day as Hong
    "E": lambda s: s['Garcia'] == s['Hong'],  # Garcia same day as Hong
}

must_be_true = []
for letter, check in options.items():
    if all(check(s) for s in solutions):
        must_be_true.append(letter)

print(f"\nMust be true in all solutions: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple must-be-true options {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No must-be-true options found")