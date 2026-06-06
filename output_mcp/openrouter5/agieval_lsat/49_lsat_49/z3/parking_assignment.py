from z3 import *

solver = Solver()

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: #1, #2, #3, #4, #5, #6
# We'll use integer variables for each employee's assigned space.

R, S, T, V, X, Y = Ints('R S T V X Y')

# Domain: each must be assigned 1 through 6
employees = [R, S, T, V, X, Y]
for e in employees:
    solver.add(e >= 1, e <= 6)

# No two employees can be assigned the same parking space
solver.add(Distinct(employees))

# Rules:
# Young must be assigned a higher-numbered space than Togowa.
solver.add(Y > T)

# Xu must be assigned a higher-numbered space than Souza.
solver.add(X > S)

# Robertson must be assigned a higher-numbered space than Young.
solver.add(R > Y)

# Robertson must be assigned #1, #2, #3, or #4.
solver.add(R >= 1, R <= 4)

# Additional condition: Togowa is assigned a higher-numbered space than Souza.
solver.add(T > S)

# Now evaluate each option
options = {
    "A": Y == 2,  # Young is assigned parking space #2
    "B": V == 5,  # Vaughn is assigned parking space #5
    "C": T == 3,  # Togowa is assigned parking space #3
    "D": S == 2,  # Souza is assigned parking space #2
    "E": R == 3   # Robertson is assigned parking space #3
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