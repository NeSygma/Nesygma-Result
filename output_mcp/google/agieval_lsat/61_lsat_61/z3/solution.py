from z3 import *

# Riders: 0:Reynaldo, 1:Seamus, 2:Theresa, 3:Yuki
# Bikes: 0:F, 1:G, 2:H, 3:J
# Days: 0:Day1, 1:Day2

R, S, T, Y = 0, 1, 2, 3
F, G, H, J = 0, 1, 2, 3

solver = Solver()

# test[rider, day]
test = {}
for r in [R, S, T, Y]:
    for d in [0, 1]:
        test[(r, d)] = Int(f"test_{r}_{d}")
        solver.add(test[(r, d)] >= 0, test[(r, d)] <= 3)

# Each day, each bike is tested by exactly one rider
for d in [0, 1]:
    solver.add(Distinct([test[(r, d)] for r in [R, S, T, Y]]))

# Each rider tests a different bike on Day 2 than on Day 1
for r in [R, S, T, Y]:
    solver.add(test[(r, 0)] != test[(r, 1)])

# Reynaldo cannot test F
solver.add(test[(R, 0)] != F, test[(R, 1)] != F)

# Yuki cannot test J
solver.add(test[(Y, 0)] != J, test[(Y, 1)] != J)

# Theresa must be one of the testers for H
solver.add(Or(test[(T, 0)] == H, test[(T, 1)] == H))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(test[(Y, 0)] == test[(S, 1)])

# Condition: Theresa tests G on the second day
solver.add(test[(T, 1)] == G)

# Answer Choices
# (A) Reynaldo tests H on the first day.
# (B) Reynaldo tests J on the first day.
# (C) Theresa tests H on the second day.
# (D) Theresa tests J on the first day.
# (E) Yuki tests H on the second day.

options = [
    ("A", test[(R, 0)] == H),
    ("B", test[(R, 0)] == J),
    ("C", test[(T, 1)] == H),
    ("D", test[(T, 0)] == J),
    ("E", test[(Y, 1)] == H)
]

found_options = []
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