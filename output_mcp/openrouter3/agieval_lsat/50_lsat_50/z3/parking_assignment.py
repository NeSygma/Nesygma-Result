from z3 import *

# Declare variables for each employee's parking space
Robertson = Int('Robertson')
Souza = Int('Souza')
Togowa = Int('Togowa')
Vaughn = Int('Vaughn')
Xu = Int('Xu')
Young = Int('Young')

# All employees must have distinct parking spaces 1-6
employees = [Robertson, Souza, Togowa, Vaughn, Xu, Young]
solver = Solver()

# Base constraints
for emp in employees:
    solver.add(emp >= 1, emp <= 6)
solver.add(Distinct(employees))

# Rule constraints
solver.add(Young > Togowa)  # Young > Togowa
solver.add(Xu > Souza)      # Xu > Souza
solver.add(Robertson > Young)  # Robertson > Young
solver.add(Or([Robertson == 1, Robertson == 2, Robertson == 3, Robertson == 4]))  # Robertson in {1,2,3,4}

# Define option constraints
opt_a_constr = Souza == 1
opt_b_constr = Young == 2
opt_c_constr = Vaughn == 3
opt_d_constr = Robertson == 4
opt_e_constr = Xu == 5

# Check each option to see if it makes the assignment unique
found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    
    # Check if this option leads to a unique solution
    # We need to check if there's exactly one solution
    if solver.check() == sat:
        # Get the first solution
        m1 = solver.model()
        
        # Try to find a second solution by blocking the first one
        blocking_clause = Or([emp != m1[emp] for emp in employees])
        solver.add(blocking_clause)
        
        if solver.check() == unsat:
            # Only one solution found
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