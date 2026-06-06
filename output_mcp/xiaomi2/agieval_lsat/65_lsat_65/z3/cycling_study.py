from z3 import *

solver = Solver()

# Riders: R=0, S=1, T=2, Y=3
# Bicycles: F=0, G=1, H=2, J=3
F, G, H, J = 0, 1, 2, 3
R, S, T, Y = 0, 1, 2, 3

# day1[r] = bicycle tested by rider r on day 1
# day2[r] = bicycle tested by rider r on day 2
day1 = [Int(f'day1_{r}') for r in range(4)]
day2 = [Int(f'day2_{r}') for r in range(4)]

# Domain: each assignment is 0-3 (F, G, H, J)
for r in range(4):
    solver.add(day1[r] >= 0, day1[r] <= 3)
    solver.add(day2[r] >= 0, day2[r] <= 3)

# All different on each day (each bicycle tested exactly once per day)
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

# Constraint 4: Bicycle Yuki tests on day 1 must be tested by Seamus on day 2
solver.add(day1[Y] == day2[S])

# Now check each option - which CANNOT be true?
# (A) Both Reynaldo and Seamus test J (each tests J on at least one day)
opt_a = And(
    Or(day1[R] == J, day2[R] == J),
    Or(day1[S] == J, day2[S] == J)
)

# (B) Both Reynaldo and Theresa test J
opt_b = And(
    Or(day1[R] == J, day2[R] == J),
    Or(day1[T] == J, day2[T] == J)
)

# (C) Both Reynaldo and Yuki test G
opt_c = And(
    Or(day1[R] == G, day2[R] == G),
    Or(day1[Y] == G, day2[Y] == G)
)

# (D) Both Seamus and Theresa test G
opt_d = And(
    Or(day1[S] == G, day2[S] == G),
    Or(day1[T] == G, day2[T] == G)
)

# (E) Both Theresa and Yuki test F
opt_e = And(
    Or(day1[T] == F, day2[T] == F),
    Or(day1[Y] == F, day2[Y] == F)
)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        d1 = [m[day1[r]].as_long() for r in range(4)]
        d2 = [m[day2[r]].as_long() for r in range(4)]
        bike_name = ['F', 'G', 'H', 'J']
        rider_name = ['R', 'S', 'T', 'Y']
        print(f"Option {letter} is POSSIBLE:")
        for r in range(4):
            print(f"  {rider_name[r]}: Day1={bike_name[d1[r]]}, Day2={bike_name[d2[r]]}")
    else:
        print(f"Option {letter} is IMPOSSIBLE (unsat)")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")