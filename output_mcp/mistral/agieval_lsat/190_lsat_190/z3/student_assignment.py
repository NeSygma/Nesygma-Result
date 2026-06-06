from z3 import *

# Base constraints solver
solver = Solver()

# Years: 1921, 1922, 1923, 1924 (indices 0, 1, 2, 3)
years = 4
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
student_indices = {s: i for i, s in enumerate(students)}

# Assignments: year -> student index
assignments = [Int(f"year_{i}") for i in range(years)]

# Each year must be assigned exactly one student
for i in range(years):
    solver.add(assignments[i] >= 0, assignments[i] < len(students))

# Constraint 1: Only Louis or Tiffany can be assigned to 1923 (year index 2)
solver.add(Or(assignments[2] == student_indices['Louis'], assignments[2] == student_indices['Tiffany']))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922 (year indices 0 or 1)
# This is automatically handled by the assignment constraints since we're checking specific options

# Constraint 3: If Tiffany is assigned, Ryan must be assigned
# We'll check this in the option constraints

# Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
# We'll check this in the option constraints

# Now evaluate each multiple-choice option
found_options = []

# Option A: Louis, Onyx, Ryan, Yoshio
opt_a_constr = And(
    assignments[0] == student_indices['Louis'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Ryan'],
    assignments[3] == student_indices['Yoshio']
)

# Option B: Mollie, Yoshio, Tiffany, Onyx
opt_b_constr = And(
    assignments[0] == student_indices['Mollie'],
    assignments[1] == student_indices['Yoshio'],
    assignments[2] == student_indices['Tiffany'],
    assignments[3] == student_indices['Onyx']
)

# Option C: Onyx, Ryan, Louis, Tiffany
opt_c_constr = And(
    assignments[0] == student_indices['Onyx'],
    assignments[1] == student_indices['Ryan'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Tiffany']
)

# Option D: Tiffany, Onyx, Louis, Ryan
opt_d_constr = And(
    assignments[0] == student_indices['Tiffany'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Ryan']
)

# Option E: Yoshio, Onyx, Louis, Mollie
opt_e_constr = And(
    assignments[0] == student_indices['Yoshio'],
    assignments[1] == student_indices['Onyx'],
    assignments[2] == student_indices['Louis'],
    assignments[3] == student_indices['Mollie']
)

# Test each option
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    
    # Additional constraints specific to each option:
    # Constraint 3: If Tiffany is assigned, Ryan must be assigned
    if "Tiffany" in constr.sexpr():
        solver.add(Or([assignments[i] == student_indices['Ryan'] for i in range(years)]))
    
    # Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
    # Check if Ryan is assigned in this option
    solver.add(Implies(
        Or([assignments[i] == student_indices['Ryan'] for i in range(years)]),
        And(
            # For each year where Ryan is assigned, the previous year must be Onyx
            And([
                Implies(
                    assignments[i] == student_indices['Ryan'],
                    And(
                        i > 0,  # Ensure there is a previous year
                        assignments[i-1] == student_indices['Onyx']
                    )
                ) for i in range(years)
            ])
        )
    ))
    
    # Constraint 2: If Mollie is assigned, she must be in 1921 or 1922
    if "Mollie" in constr.sexpr():
        solver.add(Or(
            assignments[0] == student_indices['Mollie'],
            assignments[1] == student_indices['Mollie']
        ))
    
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