from z3 import *

# Define indices for riders and bicycles
R, S, T, Y = 0, 1, 2, 3
F, G, H, J = 0, 1, 2, 3

# Create solver
solver = Solver()

# Day assignments: each rider has a bicycle each day
day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Base constraints
# Each day: permutation (all distinct and within 0..3)
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle each day
for r in range(4):
    solver.add(day1[r] != day2[r])

# Reynaldo cannot test F
solver.add(day1[R] != F)
solver.add(day2[R] != F)

# Yuki cannot test J
solver.add(day1[Y] != J)
solver.add(day2[Y] != J)

# Theresa must test H at least once
solver.add(Or(day1[T] == H, day2[T] == H))

# Yuki's first day bicycle is tested by Seamus on second day
solver.add(day2[S] == day1[Y])

# Define options
opt_a = (day1[R] == J)
opt_b = (day2[R] == J)
opt_c = (day1[S] == H)
opt_d = (day1[Y] == H)
opt_e = (day2[Y] == H)

# Use the exact skeleton for multiple choice evaluation
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Now found_options contains letters of options that are possible.
# We want the one that is NOT possible (the exception).
all_options = ["A", "B", "C", "D", "E"]
impossible_options = [opt for opt in all_options if opt not in found_options]

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
else:
    print("STATUS: unsat")
    print(f"Refine: Found {len(impossible_options)} impossible options: {impossible_options}")