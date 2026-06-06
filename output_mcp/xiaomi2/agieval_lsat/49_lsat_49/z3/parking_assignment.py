from z3 import *

solver = Solver()

# Variables: each employee gets a parking space 1-6
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

employees = [R, S, T, V, X, Y]

# Each assigned a space 1-6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Base constraints from problem
solver.add(Y > T)       # Young higher than Togowa
solver.add(X > S)       # Xu higher than Souza
solver.add(R > Y)       # Robertson higher than Young
solver.add(R <= 4)      # Robertson in {1,2,3,4}

# Additional condition: Togowa > Souza
solver.add(T > S)

# Define option constraints
opt_a = (Y == 2)   # Young assigned #2
opt_b = (V == 5)   # Vaughn assigned #5
opt_c = (T == 3)   # Togowa assigned #3
opt_d = (S == 2)   # Souza assigned #2
opt_e = (R == 3)   # Robertson assigned #3

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT: R={m[R]}, S={m[S]}, T={m[T]}, V={m[V]}, X={m[X]}, Y={m[Y]}")
    else:
        print(f"Option {letter} is UNSAT")
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