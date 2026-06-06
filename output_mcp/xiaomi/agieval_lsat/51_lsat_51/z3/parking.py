from z3 import *

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Parking spaces: 1-6

Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
names = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']

solver = Solver()

# Each employee gets a unique parking space 1-6
for e in employees:
    solver.add(e >= 1, e <= 6)
solver.add(Distinct(employees))

# Constraints
solver.add(Young > Togowa)       # Young higher than Togowa
solver.add(Xu > Souza)           # Xu higher than Souza
solver.add(Robertson > Young)    # Robertson higher than Young
solver.add(Robertson <= 4)       # Robertson in {1,2,3,4}

# Now we need to find for how many employees the assignment is limited to exactly two possible spaces.
# We enumerate all valid assignments and track which values each employee can take.

solutions = []
decision_vars = employees
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(e).as_long() for e in employees)
    solutions.append(sol)
    solver.add(Or([e != m.eval(e) for e in employees]))

print(f"Total valid assignments: {len(solutions)}")

# For each employee, collect the set of possible values
possible_values = {name: set() for name in names}
for sol in solutions:
    for i, name in enumerate(names):
        possible_values[name].add(sol[i])

print("\nPossible values for each employee:")
for name in names:
    pv = sorted(possible_values[name])
    print(f"  {name}: {pv} (count={len(pv)})")

# Count how many employees have exactly 2 possible spaces
count_two = sum(1 for name in names if len(possible_values[name]) == 2)
print(f"\nEmployees with exactly 2 possible spaces: {count_two}")

# Now evaluate the multiple choice options
# (A) none = 0, (B) two = 2, (C) three = 3, (D) four = 4, (E) five = 5

found_options = []
for letter, target in [("A", 0), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    if count_two == target:
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