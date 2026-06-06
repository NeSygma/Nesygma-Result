from z3 import *

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Spaces: #1, #2, #3, #4, #5, #6
# Each employee gets a distinct space number 1-6.

R, S, T, V, X, Y = Ints('R S T V X Y')
employees = [R, S, T, V, X, Y]

solver = Solver()

# Domain: each space is 1..6
for e in employees:
    solver.add(e >= 1, e <= 6)

# All distinct
solver.add(Distinct(employees))

# Constraints:
# Young > Togowa
solver.add(Y > T)

# Xu > Souza
solver.add(X > S)

# Robertson > Young
solver.add(R > Y)

# Robertson must be #1, #2, #3, or #4
solver.add(Or([R == i for i in [1, 2, 3, 4]]))

# Now we need to find: For how many employees is the assignment limited to only two possible spaces?
# We'll enumerate all solutions and count, for each employee, how many distinct values they take across all solutions.

solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = {e: m.eval(e, model_completion=True).as_long() for e in employees}
    solutions.append(sol)
    # Block this solution
    solver.add(Or([e != sol[e] for e in employees]))

print(f"Total solutions: {len(solutions)}")

# For each employee, collect all possible space numbers across solutions
possible = {e: set() for e in employees}
for sol in solutions:
    for e in employees:
        possible[e].add(sol[e])

print("Possible spaces per employee:")
for e, name in zip(employees, ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]):
    print(f"  {name}: {sorted(possible[e])} (count={len(possible[e])})")

# Count employees limited to exactly 2 possible spaces
limited_to_two = sum(1 for e in employees if len(possible[e]) == 2)
print(f"Employees limited to exactly 2 possible spaces: {limited_to_two}")

# Now evaluate the multiple choice options
# A: none (0), B: two (2), C: three (3), D: four (4), E: five (5)
opt_a = (limited_to_two == 0)
opt_b = (limited_to_two == 2)
opt_c = (limited_to_two == 3)
opt_d = (limited_to_two == 4)
opt_e = (limited_to_two == 5)

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