from z3 import *

# Create solver
solver = Solver()

# Define businesses
businesses = ['pharmacy', 'optometrist', 'restaurant1', 'restaurant2', 'shoe_store', 'toy_store', 'veterinarian']

# Create position variables for each business (1-7)
pos = {b: Int(f'pos_{b}') for b in businesses}

# All positions must be between 1 and 7
for b in businesses:
    solver.add(pos[b] >= 1, pos[b] <= 7)

# All positions must be distinct
solver.add(Distinct([pos[b] for b in businesses]))

# Original constraints:
# 1. The pharmacy must be at one end of the row and one of the restaurants at the other.
solver.add(Or(pos['pharmacy'] == 1, pos['pharmacy'] == 7))
solver.add(Or(pos['restaurant1'] == 1, pos['restaurant1'] == 7, 
              pos['restaurant2'] == 1, pos['restaurant2'] == 7))
# Ensure one restaurant is at the opposite end from pharmacy
solver.add(Or(
    And(pos['pharmacy'] == 1, Or(pos['restaurant1'] == 7, pos['restaurant2'] == 7)),
    And(pos['pharmacy'] == 7, Or(pos['restaurant1'] == 1, pos['restaurant2'] == 1))
))

# 2. The two restaurants must be separated by at least two other businesses.
# This means |pos1 - pos2| >= 3
solver.add(Or(
    pos['restaurant1'] - pos['restaurant2'] >= 3,
    pos['restaurant2'] - pos['restaurant1'] >= 3
))

# 3. The pharmacy must be next to either the optometrist or the veterinarian.
solver.add(Or(
    pos['pharmacy'] - pos['optometrist'] == 1,
    pos['optometrist'] - pos['pharmacy'] == 1,
    pos['pharmacy'] - pos['veterinarian'] == 1,
    pos['veterinarian'] - pos['pharmacy'] == 1
))

# 4. The toy store cannot be next to the veterinarian.
solver.add(And(
    pos['toy_store'] - pos['veterinarian'] != 1,
    pos['veterinarian'] - pos['toy_store'] != 1
))

# Now test each answer choice by replacing constraint 2
# We'll create a function to test each option
def test_option(option_constraint):
    # Create a fresh solver for each test
    test_solver = Solver()
    
    # Add all base constraints except the original constraint 2
    for b in businesses:
        test_solver.add(pos[b] >= 1, pos[b] <= 7)
    test_solver.add(Distinct([pos[b] for b in businesses]))
    
    # Add constraint 1
    test_solver.add(Or(pos['pharmacy'] == 1, pos['pharmacy'] == 7))
    test_solver.add(Or(pos['restaurant1'] == 1, pos['restaurant1'] == 7, 
                       pos['restaurant2'] == 1, pos['restaurant2'] == 7))
    test_solver.add(Or(
        And(pos['pharmacy'] == 1, Or(pos['restaurant1'] == 7, pos['restaurant2'] == 7)),
        And(pos['pharmacy'] == 7, Or(pos['restaurant1'] == 1, pos['restaurant2'] == 1))
    ))
    
    # Add constraint 3
    test_solver.add(Or(
        pos['pharmacy'] - pos['optometrist'] == 1,
        pos['optometrist'] - pos['pharmacy'] == 1,
        pos['pharmacy'] - pos['veterinarian'] == 1,
        pos['veterinarian'] - pos['pharmacy'] == 1
    ))
    
    # Add constraint 4
    test_solver.add(And(
        pos['toy_store'] - pos['veterinarian'] != 1,
        pos['veterinarian'] - pos['toy_store'] != 1
    ))
    
    # Add the option-specific constraint
    test_solver.add(option_constraint)
    
    return test_solver.check() == sat

# Test each option
options = []

# Option A: A restaurant must be in either space 3, space 4, or space 5.
opt_a = Or(pos['restaurant1'] == 3, pos['restaurant1'] == 4, pos['restaurant1'] == 5,
           pos['restaurant2'] == 3, pos['restaurant2'] == 4, pos['restaurant2'] == 5)
if test_option(opt_a):
    options.append('A')

# Option B: A restaurant must be next to either the optometrist or the veterinarian.
opt_b = Or(
    Or(pos['restaurant1'] - pos['optometrist'] == 1, pos['optometrist'] - pos['restaurant1'] == 1),
    Or(pos['restaurant1'] - pos['veterinarian'] == 1, pos['veterinarian'] - pos['restaurant1'] == 1),
    Or(pos['restaurant2'] - pos['optometrist'] == 1, pos['optometrist'] - pos['restaurant2'] == 1),
    Or(pos['restaurant2'] - pos['veterinarian'] == 1, pos['veterinarian'] - pos['restaurant2'] == 1)
)
if test_option(opt_b):
    options.append('B')

# Option C: Either the toy store or the veterinarian must be somewhere between the two restaurants.
# This means: (toy_store between R1 and R2) OR (veterinarian between R1 and R2)
opt_c = Or(
    And(pos['restaurant1'] < pos['toy_store'], pos['toy_store'] < pos['restaurant2']),
    And(pos['restaurant2'] < pos['toy_store'], pos['toy_store'] < pos['restaurant1']),
    And(pos['restaurant1'] < pos['veterinarian'], pos['veterinarian'] < pos['restaurant2']),
    And(pos['restaurant2'] < pos['veterinarian'], pos['veterinarian'] < pos['restaurant1'])
)
if test_option(opt_c):
    options.append('C')

# Option D: No more than two businesses can separate the pharmacy and the restaurant nearest it.
# This means: distance between pharmacy and nearest restaurant <= 3
opt_d = Or(
    # If pharmacy is at 1, nearest restaurant must be at 2, 3, or 4
    And(pos['pharmacy'] == 1, Or(pos['restaurant1'] <= 4, pos['restaurant2'] <= 4)),
    # If pharmacy is at 7, nearest restaurant must be at 4, 5, or 6
    And(pos['pharmacy'] == 7, Or(pos['restaurant1'] >= 4, pos['restaurant2'] >= 4))
)
if test_option(opt_d):
    options.append('D')

# Option E: The optometrist cannot be next to the shoe store.
opt_e = And(
    pos['optometrist'] - pos['shoe_store'] != 1,
    pos['shoe_store'] - pos['optometrist'] != 1
)
if test_option(opt_e):
    options.append('E')

# Now use the exact skeleton for multiple choice evaluation
found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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