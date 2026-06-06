from z3 import *

solver = Solver()

# Days 1 through 7
N = 7
days = range(N)  # 0 to 6 for easier indexing

# Kitten breeds: Himalayan, Manx, Siamese
kitten_breeds = ['Himalayan', 'Manx', 'Siamese']

# Puppy breeds: Greyhound, Newfoundland, Rottweiler
puppy_breeds = ['Greyhound', 'Newfoundland', 'Rottweiler']

# Declare kitten and puppy assignments for each day
# We'll use integers to represent breeds for easier constraint handling
kitten = [Int(f'kitten_day_{d}') for d in days]
puppy = [Int(f'puppy_day_{d}') for d in days]

# Helper: breed index mapping
kitten_idx = {b: i for i, b in enumerate(kitten_breeds)}
puppy_idx = {b: i for i, b in enumerate(puppy_breeds)}

# Base constraints
# 1. Greyhounds are featured on day 1 (index 0)
solver.add(puppy[0] == puppy_idx['Greyhound'])

# 2. No breed is featured on any two consecutive days
for d in range(N - 1):
    solver.add(kitten[d] != kitten[d + 1])
    solver.add(puppy[d] != puppy[d + 1])

# 3. Any breed featured on day 1 is not featured on day 7 (index 6)
# Day 1 kitten and puppy breeds cannot be on day 7
solver.add(kitten[0] != kitten[6])
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days, but not on day 1 (index 0)
solver.add(Sum([If(kitten[d] == kitten_idx['Himalayan'], 1, 0) for d in days]) == 3)
solver.add(kitten[0] != kitten_idx['Himalayan'])

# 5. Rottweilers are not featured on day 7 (index 6), nor on any day that features Himalayans
solver.add(puppy[6] != puppy_idx['Rottweiler'])
for d in days:
    solver.add(Implies(kitten[d] == kitten_idx['Himalayan'], puppy[d] != puppy_idx['Rottweiler']))

# Now evaluate the multiple choice options for kitten breeds
# We will check each option to see if it satisfies all constraints

# Define the options as lists of kitten breeds for days 1-7 (indices 0-6)
option_A = ['Himalayan', 'Manx', 'Siamese', 'Himalayan', 'Manx', 'Himalayan', 'Siamese']
option_B = ['Manx', 'Himalayan', 'Siamese', 'Himalayan', 'Manx', 'Himalayan', 'Manx']
option_C = ['Manx', 'Himalayan', 'Manx', 'Himalayan', 'Siamese', 'Manx', 'Siamese']
option_D = ['Siamese', 'Himalayan', 'Manx', 'Himalayan', 'Siamese', 'Siamese', 'Himalayan']
option_E = ['Siamese', 'Himalayan', 'Siamese', 'Himalayan', 'Manx', 'Siamese', 'Himalayan']

# Helper function to convert option to Z3 constraints

def option_constraints(option_list):
    constraints = []
    for d in days:
        # Map breed name to index
        kitten_breed_idx = kitten_idx[option_list[d]]
        constraints.append(kitten[d] == kitten_breed_idx)
    return constraints

# Evaluate each option
found_options = []

for letter, option_list in [("A", option_A), ("B", option_B), ("C", option_C), ("D", option_D), ("E", option_E)]:
    solver.push()
    # Add the kitten assignment constraints for this option
    for constr in option_constraints(option_list):
        solver.add(constr)
    # Check if the constraints are satisfiable
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