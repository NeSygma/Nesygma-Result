from z3 import *

solver = Solver()

# Employees: Robertson=0, Souza=1, Togowa=2, Vaughn=3, Xu=4, Young=5
# Parking spaces: 1-6
R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Each assigned a space 1-6, all different
for e in employees:
    solver.add(e >= 1, e <= 6)
solver.add(Distinct(employees))

# Base constraints
solver.add(Y > T)   # Young higher than Togowa
solver.add(X > S)   # Xu higher than Souza
solver.add(R > Y)   # Robertson higher than Young
solver.add(And(R >= 1, R <= 4))  # Robertson in {1,2,3,4}

# Define each option as a complete assignment
opt_a = And(R == 4, S == 2, T == 5, V == 3, X == 6, Y == 1)
opt_b = And(R == 5, S == 4, T == 2, V == 1, X == 6, Y == 3)
opt_c = And(R == 4, S == 5, T == 1, V == 6, X == 3, Y == 2)
opt_d = And(R == 2, S == 4, T == 1, V == 5, X == 6, Y == 3)
opt_e = And(R == 4, S == 1, T == 2, V == 6, X == 5, Y == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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