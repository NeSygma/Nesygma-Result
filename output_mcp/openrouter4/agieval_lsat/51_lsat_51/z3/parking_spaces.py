from z3 import *

# Employees: Robertson, Souza, Togowa, Vaughn, Xu, Young
# Spaces: 1, 2, 3, 4, 5, 6

R, S, T, V, X, Y = Ints('R S T V X Y')

solver = Solver()

# Each gets a space 1-6
solver.add(R >= 1, R <= 6)
solver.add(S >= 1, S <= 6)
solver.add(T >= 1, T <= 6)
solver.add(V >= 1, V <= 6)
solver.add(X >= 1, X <= 6)
solver.add(Y >= 1, Y <= 6)

# All distinct
solver.add(Distinct(R, S, T, V, X, Y))

# Rules
solver.add(Y > T)  # Young > Togowa
solver.add(X > S)  # Xu > Souza
solver.add(R > Y)  # Robertson > Young
solver.add(R >= 1, R <= 4)  # Robertson in {1,2,3,4}

# Find ALL solutions
z3_vars = [R, S, T, V, X, Y]
var_names = ['R', 'S', 'T', 'V', 'X', 'Y']
employee_full = {'R': 'Robertson', 'S': 'Souza', 'T': 'Togowa', 'V': 'Vaughn', 'X': 'Xu', 'Y': 'Young'}

all_solutions = []

while solver.check() == sat:
    m = solver.model()
    sol = {}
    for name, var in zip(var_names, z3_vars):
        sol[name] = m.eval(var).as_long()
    all_solutions.append(sol)
    # Block this solution
    solver.add(Or([v != m.eval(v) for v in z3_vars]))

print(f"Total solutions: {len(all_solutions)}")

# For each employee, find which spaces are possible
possible_spaces = {name: set() for name in var_names}
for sol in all_solutions:
    for name in var_names:
        possible_spaces[name].add(sol[name])

print("\nPossible spaces for each employee:")
for name in var_names:
    spaces = sorted(possible_spaces[name])
    print(f"{employee_full[name]}: {spaces} (count={len(spaces)})")

# Count employees with exactly 2 possible spaces
count_limited_to_two = sum(1 for name in var_names if len(possible_spaces[name]) == 2)
print(f"\nNumber of employees with exactly 2 possible spaces: {count_limited_to_two}")

# Now we know the answer directly from count_limited_to_two
# The answer choices are:
# A: none (0)
# B: two (2)
# C: three (3)
# D: four (4)
# E: five (5)

answer_map = {0: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
if count_limited_to_two in answer_map:
    print("STATUS: sat")
    print(f"answer:{answer_map[count_limited_to_two]}")
else:
    print("STATUS: unsat")
    print("Refine: Count doesn't match any answer choice")