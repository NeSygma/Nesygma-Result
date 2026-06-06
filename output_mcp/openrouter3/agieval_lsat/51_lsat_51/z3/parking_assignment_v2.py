from z3 import *

# Define employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
spaces = [1, 2, 3, 4, 5, 6]

# Create assignment variables: assign[employee] = parking space number
assign = {emp: Int(f"assign_{emp}") for emp in employees}

# Phase 1: Find all valid assignments
solver1 = Solver()

# Each employee gets a unique space from 1 to 6
for emp in employees:
    solver1.add(assign[emp] >= 1)
    solver1.add(assign[emp] <= 6)

# All different constraint
solver1.add(Distinct([assign[emp] for emp in employees]))

# Rule 1: Young > Togowa
solver1.add(assign["Young"] > assign["Togowa"])

# Rule 2: Xu > Souza
solver1.add(assign["Xu"] > assign["Souza"])

# Rule 3: Robertson > Young
solver1.add(assign["Robertson"] > assign["Young"])

# Rule 4: Robertson in {1,2,3,4}
solver1.add(Or([assign["Robertson"] == s for s in [1,2,3,4]]))

# Find all solutions
all_solutions = []
while solver1.check() == sat:
    m = solver1.model()
    sol = {emp: m[assign[emp]] for emp in employees}
    all_solutions.append(sol)
    
    # Block this solution to find next one
    blocking_clause = Or([assign[emp] != sol[emp] for emp in employees])
    solver1.add(blocking_clause)

print(f"Total valid assignments found: {len(all_solutions)}")

# For each employee, collect all possible spaces across all solutions
possible_spaces = {emp: set() for emp in employees}
for sol in all_solutions:
    for emp in employees:
        # Convert Z3 IntVal to Python int
        space_val = sol[emp].as_long() if hasattr(sol[emp], 'as_long') else int(sol[emp])
        possible_spaces[emp].add(space_val)

# Count employees with exactly 2 possible spaces
employees_with_two_options = 0
for emp in employees:
    num_options = len(possible_spaces[emp])
    sorted_spaces = sorted(possible_spaces[emp])
    print(f"{emp}: {sorted_spaces} ({num_options} options)")
    if num_options == 2:
        employees_with_two_options += 1

print(f"\nEmployees with exactly 2 possible spaces: {employees_with_two_options}")

# Phase 2: Evaluate answer choices using a fresh solver
# The question asks: "For how many of the six new employees is the assignment of a parking space limited to one of only two possible spaces?"
# This means: count employees who have exactly 2 possible spaces across all valid assignments

# Define options based on the count
opt_a_constr = (employees_with_two_options == 0)  # none
opt_b_constr = (employees_with_two_options == 2)  # two
opt_c_constr = (employees_with_two_options == 3)  # three
opt_d_constr = (employees_with_two_options == 4)  # four
opt_e_constr = (employees_with_two_options == 5)  # five

# Use the required skeleton with a fresh solver
solver2 = Solver()
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), 
                       ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver2.push()
    solver2.add(constr)
    if solver2.check() == sat:
        found_options.append(letter)
    solver2.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")