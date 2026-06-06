from z3 import *

# Create solver
solver = Solver()

# Define riders and bicycles
riders = ["Reynaldo", "Seamus", "Theresa", "Yuki"]
bicycles = ["F", "G", "H", "J"]

# Create mapping from names to indices
r_idx = {r: i for i, r in enumerate(riders)}
b_idx = {b: i for i, b in enumerate(bicycles)}

# Create assignment variables: assign[day][rider] = bicycle
# Day 0 = Day 1, Day 1 = Day 2
assign = [[Int(f"assign_{day}_{rider}") for rider in riders] for day in range(2)]

# Domain constraints: each assignment must be 0-3 (F=0, G=1, H=2, J=3)
for day in range(2):
    for rider in riders:
        solver.add(assign[day][r_idx[rider]] >= 0)
        solver.add(assign[day][r_idx[rider]] <= 3)

# Constraint 1: Each rider tests exactly one bicycle per day
# (Already enforced by single variable per rider per day)

# Constraint 2: Each bicycle is tested by exactly one rider per day
for day in range(2):
    for b in range(4):
        # Exactly one rider has this bicycle on this day
        solver.add(Sum([If(assign[day][r] == b, 1, 0) for r in range(4)]) == 1)

# Constraint 3: Reynaldo cannot test F (bicycle 0)
for day in range(2):
    solver.add(assign[day][r_idx["Reynaldo"]] != 0)

# Constraint 4: Yuki cannot test J (bicycle 3)
for day in range(2):
    solver.add(assign[day][r_idx["Yuki"]] != 3)

# Constraint 5: Theresa must be one of the testers for H (bicycle 2)
# This means Theresa tests H on either Day 1 or Day 2 (or both)
solver.add(Or(assign[0][r_idx["Theresa"]] == 2, assign[1][r_idx["Theresa"]] == 2))

# Constraint 6: The bicycle that Yuki tests on Day 1 must be tested by Seamus on Day 2
# Let Y = assign[0][Yuki], then assign[1][Seamus] must equal Y
solver.add(assign[1][r_idx["Seamus"]] == assign[0][r_idx["Yuki"]])

# Additional constraint for this question: Theresa tests J on Day 1
# J is bicycle 3
solver.add(assign[0][r_idx["Theresa"]] == 3)

# Now test each option
found_options = []

# Option A: Reynaldo tests G on the second day
# G is bicycle 1
opt_a = assign[1][r_idx["Reynaldo"]] == 1

# Option B: Seamus tests H on the first day
# H is bicycle 2
opt_b = assign[0][r_idx["Seamus"]] == 2

# Option C: Yuki tests H on the second day
# H is bicycle 2
opt_c = assign[1][r_idx["Yuki"]] == 2

# Option D: Seamus is one of the testers for J
# J is bicycle 3, so Seamus tests J on either day
opt_d = Or(assign[0][r_idx["Seamus"]] == 3, assign[1][r_idx["Seamus"]] == 3)

# Option E: Theresa is one of the testers for G
# G is bicycle 1, so Theresa tests G on either day
opt_e = Or(assign[0][r_idx["Theresa"]] == 1, assign[1][r_idx["Theresa"]] == 1)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
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