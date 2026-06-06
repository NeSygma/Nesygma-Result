from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: #1, #2, #3, #4, #5, #6
# We'll use integer variables for each employee's assigned space.

R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

# Domain: each assigned to 1..6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Rules:
# Young > Togowa
solver.add(Y > T)
# Xu > Souza
solver.add(X > S)
# Robertson > Young
solver.add(R > Y)
# Robertson must be #1, #2, #3, or #4
solver.add(Or(R == 1, R == 2, R == 3, R == 4))

# Additional condition: Young is assigned a higher-numbered space than Souza
solver.add(Y > S)

# Now evaluate each option
options = {
    "A": T == 1,
    "B": Y == 2,
    "C": R == 3,
    "D": S == 3,
    "E": V == 4
}

found_options = []
for letter, constr in options.items():
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