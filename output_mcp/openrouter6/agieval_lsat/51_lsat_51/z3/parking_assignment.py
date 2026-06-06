from z3 import *

# Define employees and variables
employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
vars = {e: Int(e) for e in employees}
R, S, T, V, X, Y = vars['Robertson'], vars['Souza'], vars['Togowa'], vars['Vaughn'], vars['Xu'], vars['Young']

solver = Solver()

# Base constraints
solver.add(R >= 1, R <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)

solver.add(Distinct([R, S, T, V, X, Y]))

# Rule 1: Young must be assigned a higher-numbered parking space than Togowa.
solver.add(Y > T)

# Rule 2: Xu must be assigned a higher-numbered parking space than Souza.
solver.add(X > S)

# Rule 3: Robertson must be assigned a higher-numbered parking space than Young.
solver.add(R > Y)

# Rule 4: Robertson must be assigned parking space #1, #2, #3, or #4.
solver.add(Or([R == 1, R == 2, R == 3, R == 4]))

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = (m[R], m[S], m[T], m[V], m[X], m[Y])
    solutions.append(sol)
    # Blocking clause: at least one variable must differ from this model
    solver.add(Or([v != m[v] for v in [R, S, T, V, X, Y]]))

print(f"Total solutions found: {len(solutions)}")

# Compute possible spaces per employee
possible_spaces = {e: set() for e in employees}
for sol in solutions:
    # sol is a tuple of (R, S, T, V, X, Y) in the order of employees list
    for i, e in enumerate(employees):
        possible_spaces[e].add(sol[i])

# Count employees with exactly two possible spaces
count = 0
for e in employees:
    if len(possible_spaces[e]) == 2:
        count += 1
        print(f"{e} has exactly two possible spaces: {sorted(possible_spaces[e])}")
    else:
        print(f"{e} has {len(possible_spaces[e])} possible spaces: {sorted(possible_spaces[e])}")

print(f"Number of employees with exactly two possible spaces: {count}")

# Now use the skeleton to evaluate multiple choice options
found_options = []
options = [("A", 0), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]
for letter, num in options:
    solver.push()
    # We add a constraint that is always true, because we already computed count.
    # Instead, we check if count equals num.
    if count == num:
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