from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

employees = [R, S, T, V, X, Y]

# Each assigned a space from 1 to 6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All distinct
solver.add(Distinct(employees))

# Base constraints from problem
solver.add(Y > T)       # Young higher than Togowa
solver.add(X > S)       # Xu higher than Souza
solver.add(R > Y)       # Robertson higher than Young
solver.add(And(R >= 1, R <= 4))  # Robertson in {1,2,3,4}

# Additional condition: Young > Souza
solver.add(Y > S)

# Define option constraints
opt_a = (T == 1)   # Togowa assigned parking space #1
opt_b = (Y == 2)   # Young assigned parking space #2
opt_c = (R == 3)   # Robertson assigned parking space #3
opt_d = (S == 3)   # Souza assigned parking space #3
opt_e = (V == 4)   # Vaughn assigned parking space #4

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