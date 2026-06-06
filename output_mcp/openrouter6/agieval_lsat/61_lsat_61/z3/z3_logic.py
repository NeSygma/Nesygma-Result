from z3 import *

# Map bikes to integers
F, G, H, J = 0, 1, 2, 3

# Riders
R, S, T, Y = 0, 1, 2, 3  # just indices for readability, but we'll use separate variables

# Variables for day1 and day2 assignments for each rider
R1 = Int('R1')  # Reynaldo day1
R2 = Int('R2')  # Reynaldo day2
S1 = Int('S1')
S2 = Int('S2')
T1 = Int('T1')
T2 = Int('T2')
Y1 = Int('Y1')
Y2 = Int('Y2')

solver = Solver()

# Domain constraints: each assignment is a bike (0..3)
for var in [R1, R2, S1, S2, T1, T2, Y1, Y2]:
    solver.add(var >= 0, var <= 3)

# Each rider tests two different bikes
solver.add(R1 != R2)
solver.add(S1 != S2)
solver.add(T1 != T2)
solver.add(Y1 != Y2)

# Each day, all bikes are tested (permutation)
solver.add(Distinct([R1, S1, T1, Y1]))
solver.add(Distinct([R2, S2, T2, Y2]))

# Reynaldo cannot test F (0)
solver.add(R1 != F)
solver.add(R2 != F)

# Yuki cannot test J (3)
solver.add(Y1 != J)
solver.add(Y2 != J)

# Theresa must test H (2) on at least one day
solver.add(Or(T1 == H, T2 == H))

# The bicycle that Yuki tests on the first day must be tested by Seamus on the second day
solver.add(Y1 == S2)

# Additional premise: Theresa tests G on the second day
solver.add(T2 == G)

# Now test each option
options = [
    ("A", R1 == H),   # Reynaldo tests H on the first day
    ("B", R1 == J),   # Reynaldo tests J on the first day
    ("C", T2 == H),   # Theresa tests H on the second day
    ("D", T1 == J),   # Theresa tests J on the first day
    ("E", Y2 == H),   # Yuki tests H on the second day
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