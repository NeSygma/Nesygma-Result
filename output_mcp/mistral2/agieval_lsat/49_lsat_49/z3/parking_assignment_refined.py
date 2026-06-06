from z3 import *

solver = Solver()

# Declare employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
spaces = [1, 2, 3, 4, 5, 6]

# Assign a parking space to each employee
assign = {e: Int(f"assign_{e}") for e in employees}

# Each employee gets a unique space
solver.add(Distinct(list(assign.values())))

# Constraints from the problem statement
# 1. Young must be assigned a higher-numbered parking space than Togowa
solver.add(assign["Young"] > assign["Togowa"])

# 2. Xu must be assigned a higher-numbered parking space than Souza
solver.add(assign["Xu"] > assign["Souza"])

# 3. Robertson must be assigned a higher-numbered parking space than Young
solver.add(assign["Robertson"] > assign["Young"])

# 4. Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or([assign["Robertson"] == s for s in [1, 2, 3, 4]]))

# Additional constraint: Togowa is assigned a higher-numbered parking space than Souza
solver.add(assign["Togowa"] > assign["Souza"])

# Now, evaluate each option while ensuring only one is valid at a time.
# We will add constraints to ensure the other options are not valid when testing each one.

# Define the options as constraints
opt_A = (assign["Young"] == 2)
opt_B = (assign["Vaughn"] == 5)
opt_C = (assign["Togowa"] == 3)
opt_D = (assign["Souza"] == 2)
opt_E = (assign["Robertson"] == 3)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
    solver.push()
    # Block the other options to ensure only one is valid
    if letter == "A":
        solver.add(Not(opt_B), Not(opt_C), Not(opt_D), Not(opt_E))
    elif letter == "B":
        solver.add(Not(opt_A), Not(opt_C), Not(opt_D), Not(opt_E))
    elif letter == "C":
        solver.add(Not(opt_A), Not(opt_B), Not(opt_D), Not(opt_E))
    elif letter == "D":
        solver.add(Not(opt_A), Not(opt_B), Not(opt_C), Not(opt_E))
    elif letter == "E":
        solver.add(Not(opt_A), Not(opt_B), Not(opt_C), Not(opt_D))
    
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