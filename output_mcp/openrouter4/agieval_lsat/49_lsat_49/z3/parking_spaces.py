from z3 import *

solver = Solver()

# Variables for each employee's parking space
R, So, T, V, X, Y = Ints('R So T V X Y')

# Domain: each parking space is 1 through 6
employees = [R, So, T, V, X, Y]
for e in employees:
    solver.add(e >= 1, e <= 6)

# All distinct (bijection: 6 people, 6 spaces)
solver.add(Distinct(employees))

# Rule 1: Young > Togowa
solver.add(Y > T)

# Rule 2: Xu > Souza
solver.add(X > So)

# Rule 3: Robertson > Young
solver.add(R > Y)

# Rule 4: Robertson must be #1, #2, #3, or #4
solver.add(R >= 1, R <= 4)

# Conditional premise: Togowa > Souza
solver.add(T > So)

# Now test each option
# Option A: Young is assigned parking space #2
opt_a = (Y == 2)

# Option B: Vaughn is assigned parking space #5
opt_b = (V == 5)

# Option C: Togowa is assigned parking space #3
opt_c = (T == 3)

# Option D: Souza is assigned parking space #2
opt_d = (So == 2)

# Option E: Robertson is assigned parking space #3
opt_e = (R == 3)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    result = solver.check()
    print(f"Option {letter}: {result}")
    if result == sat:
        m = solver.model()
        print(f"  R={m[R]}, So={m[So]}, T={m[T]}, V={m[V]}, X={m[X]}, Y={m[Y]}")
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