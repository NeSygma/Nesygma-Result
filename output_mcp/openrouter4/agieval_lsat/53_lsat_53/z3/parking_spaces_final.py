from z3 import *

# Encode the problem
R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

solver = Solver()

# Domain: each employee gets one space (1-6)
for e in employees:
    solver.add(e >= 1, e <= 6)

# No two share a space
solver.add(Distinct(employees))

# Order constraints
solver.add(Y > T)   # Young > Togowa
solver.add(X > S)   # Xu > Souza
solver.add(R > Y)   # Robertson > Young

# Robertson must be in 1-4
solver.add(R >= 1, R <= 4)

# Additional condition: Robertson = #3
solver.add(R == 3)

# Option constraints
opt_A = (S == 4)  # Souza is #4
opt_B = (T == 2)  # Togowa is #2
opt_C = (V == 5)  # Vaughn is #5
opt_D = (X == 6)  # Xu is #6
opt_E = (Y == 2)  # Young is #2

# Check each option: if NOT(option) is UNSAT, option MUST be true
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
    solver.push()
    solver.add(Not(constr))
    if solver.check() == unsat:
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