from z3 import *

# Sections: 0: Lifestyle, 1: Metro, 2: Sports
# Photographers: 0: Fuentes, 1: Gagnon, 2: Hue
# count[s][p]

# We need to find which option MUST be true.
# This means we check if NOT(option) is UNSAT.

solver = Solver()
count = [[Int(f'count_{s}_{p}') for p in range(3)] for s in range(3)]

# Constraints
for s in range(3):
    solver.add(Sum([count[s][p] for p in range(3)]) == 2)
    for p in range(3):
        solver.add(count[s][p] >= 0)

for p in range(3):
    total_p = Sum([count[s][p] for s in range(3)])
    solver.add(total_p >= 1, total_p <= 3)

solver.add(Or([And(count[0][p] > 0, count[1][p] > 0) for p in range(3)]))
solver.add(count[0][2] == count[2][0])
solver.add(count[2][1] == 0)
solver.add(count[0][2] == 2)

# The question asks "which one of the following MUST be true".
# This means we need to find an option that is true in ALL valid models.
# Let's find all valid models first.

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = [[m.evaluate(count[s][p]).as_long() for p in range(3)] for s in range(3)]
    solutions.append(sol)
    # Block this solution
    solver.add(Or([count[s][p] != m.evaluate(count[s][p]) for s in range(3) for p in range(3)]))

print(f"Total solutions: {len(solutions)}")
for i, sol in enumerate(solutions):
    print(f"Solution {i+1}: {sol}")

# Now check which option is true for ALL solutions
options = [
    ("A", lambda sol: sum(sol[s][0] for s in range(3)) == 1),
    ("B", lambda sol: sum(sol[s][0] for s in range(3)) == 3),
    ("C", lambda sol: sum(sol[s][1] for s in range(3)) == 1),
    ("D", lambda sol: sum(sol[s][1] for s in range(3)) == 2),
    ("E", lambda sol: sum(sol[s][2] for s in range(3)) == 2)
]

must_be_true = []
for letter, check_func in options:
    if all(check_func(sol) for sol in solutions):
        must_be_true.append(letter)

print(f"Must be true: {must_be_true}")