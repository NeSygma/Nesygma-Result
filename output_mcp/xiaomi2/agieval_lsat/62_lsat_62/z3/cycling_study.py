from z3 import *

solver = Solver()

# Riders: R=0, S=1, T=2, Y=3
# Bicycles: F=0, G=1, H=2, J=3
R, S, T, Y = 0, 1, 2, 3
F, G, H, J = 0, 1, 2, 3

# day1[r] = bicycle tested by rider r on day 1
# day2[r] = bicycle tested by rider r on day 2
day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Each bicycle is in range 0-3
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# Each day is a permutation (all different)
solver.add(Distinct(day1))
solver.add(Distinct(day2))

# Each rider tests a different bicycle on day 2 than day 1
for r in range(4):
    solver.add(day1[r] != day2[r])

# Constraint 1: Reynaldo cannot test F (on either day)
solver.add(day1[R] != F)
solver.add(day2[R] != F)

# Constraint 2: Yuki cannot test J (on either day)
solver.add(day1[Y] != J)
solver.add(day2[Y] != J)

# Constraint 3: Theresa must test H on at least one day
solver.add(Or(day1[T] == H, day2[T] == H))

# Constraint 4: Yuki's day 1 bicycle = Seamus's day 2 bicycle
solver.add(day2[S] == day1[Y])

# Now test each option to see which CANNOT be true
# "Any of the following could be true EXCEPT" = the one that is UNSAT

options = [
    ("A", day1[R] == J),   # Reynaldo tests J on day 1
    ("B", day2[R] == J),   # Reynaldo tests J on day 2
    ("C", day1[S] == H),   # Seamus tests H on day 1
    ("D", day1[Y] == H),   # Yuki tests H on day 1
    ("E", day2[Y] == H),   # Yuki tests H on day 2
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# The EXCEPT answer is the one NOT in found_options
# "could be true EXCEPT" means the one that CANNOT be true
all_options = ["A", "B", "C", "D", "E"]
impossible = [o for o in all_options if o not in found_options]

print(f"Possible options: {found_options}")
print(f"Impossible options: {impossible}")

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: All options are possible")