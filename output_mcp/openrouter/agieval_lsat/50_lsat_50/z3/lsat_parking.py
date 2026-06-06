from z3 import *

# Define variables for each employee
R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

employees = [R, S, T, V, X, Y]

solver = Solver()

# Domain constraints: each parking space 1..6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All different
solver.add(Distinct(employees))

# Given rules
solver.add(Y > T)          # Young higher than Togowa
solver.add(X > S)          # Xu higher than Souza
solver.add(R > Y)          # Robertson higher than Young
solver.add(R <= 4)        # Robertson in {1,2,3,4}

# Helper to test uniqueness under an extra condition
def is_unique(extra_constraint):
    # Push extra condition
    solver.push()
    solver.add(extra_constraint)
    if solver.check() != sat:
        solver.pop()
        return False
    m = solver.model()
    # Build blocking clause for this model
    block = Or([e != m[e] for e in employees])
    # Check if another solution exists
    solver.push()
    solver.add(block)
    unique = (solver.check() == unsat)
    solver.pop()
    solver.pop()
    return unique

found_options = []
# Define extra constraints for each option
opt_a = (S == 1)          # Souza is #1
opt_b = (Y == 2)          # Young is #2
opt_c = (V == 3)          # Vaughn is #3
opt_d = (R == 4)          # Robertson is #4
opt_e = (X == 5)          # Xu is #5

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

for letter, constr in options:
    if is_unique(constr):
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")