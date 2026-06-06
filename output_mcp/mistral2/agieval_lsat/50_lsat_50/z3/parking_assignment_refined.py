from z3 import *

# Function to check if the current solver state has a unique solution
def has_unique_solution(solver, model):
    # Block the current model
    blocking = []
    for v in model:
        blocking.append(v() != model[v])
    solver.add(Or(blocking))
    
    # Check if there is another solution
    result = solver.check()
    return result == unsat

# Main solver
solver = Solver()

# Declare employees and parking spaces
employees = ["Robertson", "Souza", "Togowa", "Vaughn", "Xu", "Young"]
spaces = [1, 2, 3, 4, 5, 6]

# Assign a parking space to each employee
assign = {e: Int(f"assign_{e}") for e in employees}

# Each employee gets a unique space
solver.add(Distinct(list(assign.values())))

# Each space is assigned to exactly one employee
for s in spaces:
    solver.add(Or([assign[e] == s for e in employees]))

# Constraints from the problem statement
# Young must be assigned a higher-numbered parking space than Togowa
solver.add(assign["Young"] > assign["Togowa"])

# Xu must be assigned a higher-numbered parking space than Souza
solver.add(assign["Xu"] > assign["Souza"])

# Robertson must be assigned a higher-numbered parking space than Young
solver.add(assign["Robertson"] > assign["Young"])

# Robertson must be assigned parking space #1, #2, #3, or #4
solver.add(Or([assign["Robertson"] == s for s in [1, 2, 3, 4]]))

# Define the options as constraints
opt_a_constr = (assign["Souza"] == 1)
opt_b_constr = (assign["Young"] == 2)
opt_c_constr = (assign["Vaughn"] == 3)
opt_d_constr = (assign["Robertson"] == 4)
opt_e_constr = (assign["Xu"] == 5)

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    
    # Check if the option is satisfiable
    if solver.check() == sat:
        model = solver.model()
        # Check if the solution is unique
        if has_unique_solution(solver, model):
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