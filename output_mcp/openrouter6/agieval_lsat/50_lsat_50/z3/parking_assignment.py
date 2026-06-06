from z3 import *

# Define variables for employees
R, S, T, V, X, Y = Ints('R S T V X Y')

# Base constraints
solver = Solver()
solver.add(Distinct([R, S, T, V, X, Y]))
solver.add(Y > T)          # Young > Togowa
solver.add(X > S)          # Xu > Souza
solver.add(R > Y)          # Robertson > Young
solver.add(R <= 4)         # Robertson in {1,2,3,4}
solver.add(R >= 1, S >= 1, T >= 1, V >= 1, X >= 1, Y >= 1)
solver.add(R <= 6, S <= 6, T <= 6, V <= 6, X <= 6, Y <= 6)

# Option constraints
opt_a = (S == 1)
opt_b = (Y == 2)
opt_c = (V == 3)
opt_d = (R == 4)
opt_e = (X == 5)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Get first model
        m1 = solver.model()
        # Add blocking clause to check for second solution
        solver.push()
        blocking = Or([R != m1[R], S != m1[S], T != m1[T], V != m1[V], X != m1[X], Y != m1[Y]])
        solver.add(blocking)
        if solver.check() == unsat:
            # Exactly one solution
            found_options.append(letter)
        solver.pop()  # pop blocking clause
    solver.pop()  # pop option constraint

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")