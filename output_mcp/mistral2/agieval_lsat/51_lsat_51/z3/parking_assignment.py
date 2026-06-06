from z3 import *

# Base constraints for the parking assignment problem
solver = Solver()

# Employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
spaces = [1, 2, 3, 4, 5, 6]

# Assign a parking space to each employee
assign = {e: Int(f"assign_{e}") for e in employees}

# Each employee gets a unique space
solver.add(Distinct(list(assign.values())))

# Each space is assigned to exactly one employee (implicit in Distinct)
for e in employees:
    solver.add(Or([assign[e] == s for s in spaces]))

# Constraints from the problem statement
# Young must be assigned a higher-numbered parking space than Togowa
solver.add(assign["Young"] > assign["Togowa"])

# Xu must be assigned a higher-numbered parking space than Souza
solver.add(assign["Xu"] > assign["Souza"])

# Robertson must be assigned a higher-numbered parking space than Young
solver.add(assign["Robertson"] > assign["Young"])

# Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or([assign["Robertson"] == s for s in [1, 2, 3, 4]]))

# Now, we need to determine for how many employees the assignment is limited to only two possible spaces.
# We will check each employee to see if their assignment is constrained to exactly two possible spaces.

# Helper function to check if an employee's assignment is limited to exactly two possible spaces
def is_limited_to_two_spaces(emp):
    solver.push()
    # Collect all possible spaces for the employee
    possible_spaces = []
    for s in spaces:
        solver.push()
        solver.add(assign[emp] == s)
        if solver.check() == sat:
            possible_spaces.append(s)
        solver.pop()
    solver.pop()
    return len(possible_spaces) == 2

# Check each employee
limited_employees = []
for emp in employees:
    if is_limited_to_two_spaces(emp):
        limited_employees.append(emp)

# Now, evaluate the multiple choice options
found_options = []
for letter, count in [("A", 0), ("B", 2), ("C", 3), ("D", 4), ("E", 5)]:
    solver.push()
    if len(limited_employees) == count:
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