from z3 import *

# Employees: Robertson=0, Souza=1, Togowa=2, Vaughn=3, Xu=4, Young=5
# Spaces: 1-6

employees = ['Robertson', 'Souza', 'Togowa', 'Vaughn', 'Xu', 'Young']
R, S, T, V, X, Y = [Int(e) for e in employees]

# Base constraints
base_constraints = [
    # Each assigned a space 1-6
    And(R >= 1, R <= 6),
    And(S >= 1, S <= 6),
    And(T >= 1, T <= 6),
    And(V >= 1, V <= 6),
    And(X >= 1, X <= 6),
    And(Y >= 1, Y <= 6),
    # All different
    Distinct(R, S, T, V, X, Y),
    # Young > Togowa
    Y > T,
    # Xu > Souza
    X > S,
    # Robertson > Young
    R > Y,
    # Robertson in {1,2,3,4}
    And(R >= 1, R <= 4),
]

# For each employee, check which spaces are possible
vars_list = [R, S, T, V, X, Y]
possible_spaces = {}

for i, emp in enumerate(employees):
    possible = []
    for space in range(1, 7):
        s = Solver()
        s.add(base_constraints)
        s.add(vars_list[i] == space)
        if s.check() == sat:
            possible.append(space)
    possible_spaces[emp] = possible
    print(f"{emp}: possible spaces = {possible} (count: {len(possible)})")

# Count employees with exactly 2 possible spaces
count_two = sum(1 for emp in employees if len(possible_spaces[emp]) == 2)
print(f"\nNumber of employees with exactly 2 possible spaces: {count_two}")

# Now evaluate the answer choices
# (A) none -> count_two == 0
# (B) two -> count_two == 2
# (C) three -> count_two == 3
# (D) four -> count_two == 4
# (E) five -> count_two == 5

options = {
    "A": count_two == 0,
    "B": count_two == 2,
    "C": count_two == 3,
    "D": count_two == 4,
    "E": count_two == 5,
}

found_options = [letter for letter, valid in options.items() if valid]

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")