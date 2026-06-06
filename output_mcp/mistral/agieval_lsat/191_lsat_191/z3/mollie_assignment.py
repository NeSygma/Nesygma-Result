from z3 import *

# Define students and years
students = ['Louis', 'Mollie', 'Onyx', 'Ryan', 'Tiffany', 'Yoshio']
years = [1921, 1922, 1923, 1924]

# Create a solver
solver = Solver()

# Create assignment variables: assign[i] = student index for year years[i]
assign = [Int(f'assign_{year}') for year in years]

# Add constraints that each assignment is a valid student index (0-5)
for a in assign:
    solver.add(a >= 0, a < len(students))

# Define student indices for convenience
louis_idx = 0
mollie_idx = 1
onyx_idx = 2
ryan_idx = 3
tiffany_idx = 4
yoshio_idx = 5

# Constraint 1: Only Louis or Tiffany can be assigned to 1923 (index 2)
solver.add(Or(assign[2] == louis_idx, assign[2] == tiffany_idx))

# Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922 (index 0 or 1)
solver.add(Implies(Or([a == mollie_idx for a in assign]), Or(assign[0] == mollie_idx, assign[1] == mollie_idx)))

# Constraint 3: If Tiffany is assigned, then Ryan must be assigned
solver.add(Implies(Or([a == tiffany_idx for a in assign]), Or([a == ryan_idx for a in assign])))

# Constraint 4: If Ryan is assigned, then Onyx must be assigned to the year immediately prior
for i in range(1, len(assign)):  # i = 1, 2, 3
    solver.add(Implies(assign[i] == ryan_idx, assign[i-1] == onyx_idx))

# Constraint 5: All assignments must be distinct (each student to exactly one year)
solver.add(Distinct(assign))

# Define the options as constraints
def get_option_constraint(letter):
    if letter == "A":
        # Louis is assigned to 1924 (index 3)
        return assign[3] == louis_idx
    elif letter == "B":
        # Onyx is assigned to 1921 (index 0)
        return assign[0] == onyx_idx
    elif letter == "C":
        # Onyx is assigned to 1924 (index 3)
        return assign[3] == onyx_idx
    elif letter == "D":
        # Tiffany is assigned to 1923 (index 2)
        return assign[2] == tiffany_idx
    elif letter == "E":
        # Yoshio is assigned to 1921 (index 0)
        return assign[0] == yoshio_idx
    else:
        return False

# For each option, check if it forces Mollie to be in 1922 (index 1)
found_options = []
for letter in ["A", "B", "C", "D", "E"]:
    # Push a new scope for the option constraint
    solver.push()
    
    # Add the option constraint
    opt_constr = get_option_constraint(letter)
    solver.add(opt_constr)
    
    # Now check if Mollie must be in 1922
    # We do this by checking if the model where Mollie is NOT in 1922 is possible
    solver.push()
    solver.add(assign[1] != mollie_idx)  # Mollie not in 1922
    result = solver.check()
    solver.pop()
    
    # If UNSAT, then Mollie MUST be in 1922 under this option
    if result == unsat:
        found_options.append(letter)
    
    # Pop the option constraint
    solver.pop()

# Determine the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")