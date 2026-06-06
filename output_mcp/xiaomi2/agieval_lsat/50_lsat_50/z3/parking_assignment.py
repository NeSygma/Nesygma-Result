from z3 import *

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: 1-6, all distinct

R = Int('R')  # Robertson
S = Int('S')  # Souza
T = Int('T')  # Togowa
V = Int('V')  # Vaughn
X = Int('X')  # Xu
Y = Int('Y')  # Young

employees = [R, S, T, V, X, Y]

def add_base_constraints(solver):
    # Each assigned a space 1-6
    for e in employees:
        solver.add(And(e >= 1, e <= 6))
    # All distinct
    solver.add(Distinct(employees))
    # Young > Togowa
    solver.add(Y > T)
    # Xu > Souza
    solver.add(X > S)
    # Robertson > Young
    solver.add(R > Y)
    # Robertson in {1,2,3,4}
    solver.add(And(R >= 1, R <= 4))

# Define option constraints
options = {
    "A": (S == 1),       # Souza is assigned parking space #1
    "B": (Y == 2),       # Young is assigned parking space #2
    "C": (V == 3),       # Vaughn is assigned parking space #3
    "D": (R == 4),       # Robertson is assigned parking space #4
    "E": (X == 5),       # Xu is assigned parking space #5
}

def count_solutions(base_constraints_fn, extra_constraint, max_count=100):
    """Count distinct solutions under given constraints."""
    s = Solver()
    base_constraints_fn(s)
    s.add(extra_constraint)
    
    solutions = 0
    while s.check() == sat:
        m = s.model()
        solutions += 1
        if solutions > max_count:
            break
        # Block current solution
        block = []
        for e in employees:
            block.append(e != m[e])
        s.add(Or(block))
    return solutions

found_options = []
for letter, constr in options.items():
    count = count_solutions(add_base_constraints, constr)
    print(f"Option {letter}: {count} solution(s)")
    if count == 1:
        found_options.append(letter)

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")