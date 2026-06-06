from z3 import *

# Create solver
solver = Solver()

# Define variables for each employee's parking space
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

# All employees must be assigned spaces 1-6
employees = [R, S, T, V, X, Y]
for emp in employees:
    solver.add(emp >= 1, emp <= 6)

# All different parking spaces
solver.add(Distinct(employees))

# Base constraints from problem
solver.add(Y > T)  # Young higher than Togowa
solver.add(X > S)  # Xu higher than Souza
solver.add(R > Y)  # Robertson higher than Young
solver.add(Or(R == 1, R == 2, R == 3, R == 4))  # Robertson in 1-4

# Define options
opt_a = (S == 1)  # Souza is assigned parking space #1
opt_b = (Y == 2)  # Young is assigned parking space #2
opt_c = (V == 3)  # Vaughn is assigned parking space #3
opt_d = (R == 4)  # Robertson is assigned parking space #4
opt_e = (X == 5)  # Xu is assigned parking space #5

# Test each option to see if it uniquely determines the assignment
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        # Check if this option uniquely determines the assignment
        # We need to see if there's only one possible model
        m = solver.model()
        # Try to find another solution with the same option
        solver.push()
        # Add constraints to make at least one variable different
        diff_constraints = []
        for emp in employees:
            diff_constraints.append(emp != m[emp])
        solver.add(Or(diff_constraints))
        if solver.check() == unsat:
            # This option uniquely determines the assignment
            found_options.append(letter)
        solver.pop()
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