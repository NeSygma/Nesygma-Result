from z3 import *

# Riders: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Bikes: 0:F, 1:G, 2:H, 3:J
# Days: 0:Day 1, 1:Day 2

solver = Solver()

# Variables: test[rider, day]
test = {}
for r in range(4):
    for d in range(2):
        test[(r, d)] = Int(f'test_r{r}_d{d}')
        solver.add(test[(r, d)] >= 0, test[(r, d)] <= 3)

# Each day, all 4 bikes are tested (Distinct)
for d in range(2):
    solver.add(Distinct([test[(r, d)] for r in range(4)]))

# Each rider tests a different bike on day 2 than on day 1
for r in range(4):
    solver.add(test[(r, 0)] != test[(r, 1)])

# Reynaldo (0) cannot test F (0)
solver.add(test[(0, 0)] != 0)
solver.add(test[(0, 1)] != 0)

# Yuki (3) cannot test J (3)
solver.add(test[(3, 0)] != 3)
solver.add(test[(3, 1)] != 3)

# Theresa (2) must test H (2) on one of the days
solver.add(Or(test[(2, 0)] == 2, test[(2, 1)] == 2))

# The bicycle that Yuki (3) tests on the first day (0) must be tested by Seamus (1) on the second day (1)
solver.add(test[(3, 0)] == test[(1, 1)])

# Options:
# (A) Reynaldo (0) tests J (3) on the first day (0)
# (B) Reynaldo (0) tests J (3) on the second day (1)
# (C) Seamus (1) tests H (2) on the first day (0)
# (D) Yuki (3) tests H (2) on the first day (0)
# (E) Yuki (3) tests H (2) on the second day (1)

options = [
    ("A", test[(0, 0)] == 3),
    ("B", test[(0, 1)] == 3),
    ("C", test[(1, 0)] == 2),
    ("D", test[(3, 0)] == 2),
    ("E", test[(3, 1)] == 2)
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# We are looking for the one that is NOT possible (UNSAT)
all_letters = ["A", "B", "C", "D", "E"]
impossible_options = [l for l in all_letters if l not in found_options]

print(f"Possible options: {found_options}")
print(f"Impossible options: {impossible_options}")

if len(impossible_options) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible_options[0]}")
else:
    print("STATUS: unsat")