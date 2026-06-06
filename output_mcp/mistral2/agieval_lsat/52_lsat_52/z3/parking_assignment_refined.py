from z3 import *

solver = Solver()

# Declare employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
parking_spaces = [1, 2, 3, 4, 5, 6]

# Assign a parking space to each employee
assign = {e: Int(f"assign_{e}") for e in employees}

# Each employee gets a unique parking space
solver.add(Distinct(list(assign.values())))

# Constraints from the problem statement
# Young must be assigned a higher-numbered parking space than Togowa
solver.add(assign["Young"] > assign["Togowa"])

# Xu must be assigned a higher-numbered parking space than Souza
solver.add(assign["Xu"] > assign["Souza"])

# Robertson must be assigned a higher-numbered parking space than Young
solver.add(assign["Robertson"] > assign["Young"])

# Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or([assign["Robertson"] == i for i in [1, 2, 3, 4]]))

# Additional constraint: Young is assigned a higher-numbered parking space than Souza
solver.add(assign["Young"] > assign["Souza"])

# Ensure that all assignments are within the valid range
for e in employees:
    solver.add(Or([assign[e] == i for i in parking_spaces]))

# Base constraints are set. Now evaluate the multiple-choice options.

# Define the options as constraints
opt_a_constr = (assign["Togowa"] == 1)
opt_b_constr = (assign["Young"] == 2)
opt_c_constr = (assign["Robertson"] == 3)
opt_d_constr = (assign["Souza"] == 3)
opt_e_constr = (assign["Vaughn"] == 4)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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