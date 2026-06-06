from z3 import *

# Define the breeds
KITTEN_BREEDS = ['H', 'M', 'S']  # Himalayan, Manx, Siamese
PUPPY_BREEDS = ['G', 'N', 'R']  # Greyhound, Newfoundland, Rottweiler

# Create solver
solver = Solver()

# Decision variables for kitten and puppy breeds for each day (1-7)
kitten = [Int(f'kitten_{i}') for i in range(1, 8)]
puppy = [Int(f'puppy_{i}') for i in range(1, 8)]

# Helper: breed to index mapping
kitten_breed_to_idx = {breed: idx for idx, breed in enumerate(KITTEN_BREEDS)}
puppy_breed_to_idx = {breed: idx for idx, breed in enumerate(PUPPY_BREEDS)}

# Helper: index to breed mapping
kitten_idx_to_breed = {idx: breed for idx, breed in enumerate(KITTEN_BREEDS)}
puppy_idx_to_breed = {idx: breed for idx, breed in enumerate(PUPPY_BREEDS)}

# Constraints

# 1. Greyhounds are featured on day 1
solver.add(puppy[0] == puppy_breed_to_idx['G'])

# 2. No breed is featured on any two consecutive days
for i in range(6):
    # Kitten breeds
    solver.add(kitten[i] != kitten[i+1])
    # Puppy breeds
    solver.add(puppy[i] != puppy[i+1])

# 3. Any breed featured on day 1 is not featured on day 7
# Day 1 breeds
solver.add(Or(
    And(kitten[0] == kitten[6], False),  # Impossible, so this is just a placeholder
    kitten[0] != kitten[6]
))
solver.add(puppy[0] != puppy[6])

# 4. Himalayans are featured on exactly three days, but not on day 1
# Count Himalayans in kitten breeds
num_himalayans = Sum([If(kitten[i] == kitten_breed_to_idx['H'], 1, 0) for i in range(7)])
solver.add(num_himalayans == 3)
solver.add(kitten[0] != kitten_breed_to_idx['H'])  # Not on day 1

# 5. Rottweilers are not featured on day 7, nor on any day that features Himalayans
solver.add(puppy[6] != puppy_breed_to_idx['R'])  # Not on day 7
for i in range(7):
    solver.add(Implies(kitten[i] == kitten_breed_to_idx['H'], puppy[i] != puppy_breed_to_idx['R']))

# Base constraints for breed values (0, 1, 2)
for i in range(7):
    solver.add(kitten[i] >= 0, kitten[i] < 3)
    solver.add(puppy[i] >= 0, puppy[i] < 3)

# Define the options as constraints on kitten sequence
# Each option is a list of kitten breeds for days 1-7
options = {
    "A": ['H', 'M', 'S', 'H', 'M', 'H', 'S'],
    "B": ['M', 'H', 'S', 'H', 'M', 'H', 'M'],
    "C": ['M', 'H', 'M', 'H', 'S', 'M', 'S'],
    "D": ['S', 'H', 'M', 'H', 'S', 'S', 'H'],
    "E": ['S', 'H', 'S', 'H', 'M', 'S', 'H']
}

# Map breed letters to indices for constraints
option_constraints = {}
for letter, breed_seq in options.items():
    constraints = []
    for day_idx, breed in enumerate(breed_seq):
        breed_idx = kitten_breed_to_idx[breed]
        constraints.append(kitten[day_idx] == breed_idx)
    option_constraints[letter] = And(constraints)

# Evaluate each option
found_options = []
for letter, constr in [("A", option_constraints["A"]), 
                        ("B", option_constraints["B"]), 
                        ("C", option_constraints["C"]), 
                        ("D", option_constraints["D"]), 
                        ("E", option_constraints["E"])]:
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