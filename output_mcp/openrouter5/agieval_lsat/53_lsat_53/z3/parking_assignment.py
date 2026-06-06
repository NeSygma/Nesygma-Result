from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: #1 through #6
# We'll use integer variables for each employee's assigned space (1-6)

R, S, T, V, X, Y = Ints('R S T V X Y')

# Domain: each assigned to 1 through 6
employees = [R, S, T, V, X, Y]
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Constraints:
# Young > Togowa
solver.add(Y > T)

# Xu > Souza
solver.add(X > S)

# Robertson > Young
solver.add(R > Y)

# Robertson must be #1, #2, #3, or #4
solver.add(Or(R == 1, R == 2, R == 3, R == 4))

# Additional condition: Robertson is assigned parking space #3
solver.add(R == 3)

# Now evaluate each option
# Option A: Souza is assigned parking space #4
opt_a = (S == 4)

# Option B: Togowa is assigned parking space #2
opt_b = (T == 2)

# Option C: Vaughn is assigned parking space #5
opt_c = (V == 5)

# Option D: Xu is assigned parking space #6
opt_d = (X == 6)

# Option E: Young is assigned parking space #2
opt_e = (Y == 2)

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