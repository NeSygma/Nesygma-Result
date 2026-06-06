from z3 import *

# Base constraints for the shopping center problem
solver = Solver()

# Declare the businesses as symbolic constants
businesses = [
    "optometrist",
    "pharmacy",
    "restaurant1",
    "restaurant2",
    "shoe_store",
    "toy_store",
    "veterinarian"
]

# Create a list of Int variables representing the positions of the businesses
# Each position is an Int between 1 and 7 (inclusive)
positions = [Int(f"pos_{b}") for b in businesses]

# Each position must be unique and between 1 and 7
solver.add(Distinct(positions))
for p in positions:
    solver.add(p >= 1, p <= 7)

# Helper function to get the position of a business
def pos(b):
    return positions[businesses.index(b)]

# Constraints from the problem statement:

# 1. The pharmacy must be at one end of the row and one of the restaurants at the other.
solver.add(Or(pos("pharmacy") == 1, pos("pharmacy") == 7))
solver.add(Or(pos("restaurant1") == 1, pos("restaurant1") == 7))
solver.add(Or(pos("restaurant2") == 1, pos("restaurant2") == 7))

# Ensure the two restaurants are at opposite ends
solver.add(Or(
    And(pos("restaurant1") == 1, pos("restaurant2") == 7),
    And(pos("restaurant1") == 7, pos("restaurant2") == 1)
))

# 2. The two restaurants must be separated by at least two other businesses.
# This means the absolute difference between their positions must be at least 3.
solver.add(abs(pos("restaurant1") - pos("restaurant2")) >= 3)

# 3. The pharmacy must be next to either the optometrist or the veterinarian.
# Next means adjacent positions (difference of 1).
solver.add(Or(
    abs(pos("pharmacy") - pos("optometrist")) == 1,
    abs(pos("pharmacy") - pos("veterinarian")) == 1
))

# 4. The toy store cannot be next to the veterinarian.
solver.add(abs(pos("toy_store") - pos("veterinarian")) != 1)

# Now, evaluate each option to see which one satisfies all constraints.

# Define the options as constraints on the positions of the businesses.
# We will check each option by constraining the positions to match the given order.

# Helper function to create constraints for an option
def option_constraints(option_name, order):
    # order is a list of business names in the order of spaces 1 through 7
    constraints = []
    for i, b in enumerate(order):
        # The position of business b must be i+1 (since spaces are 1-indexed)
        constraints.append(pos(b) == i+1)
    return constraints

# Define the options
options = {
    "A": ["pharmacy", "optometrist", "shoe_store", "restaurant1", "veterinarian", "toy_store", "restaurant2"],
    "B": ["pharmacy", "veterinarian", "optometrist", "shoe_store", "restaurant1", "toy_store", "restaurant2"],
    "C": ["restaurant1", "shoe_store", "veterinarian", "pharmacy", "optometrist", "toy_store", "restaurant2"],
    "D": ["restaurant1", "toy_store", "optometrist", "restaurant2", "veterinarian", "shoe_store", "pharmacy"],
    "E": ["restaurant1", "optometrist", "toy_store", "restaurant2", "shoe_store", "veterinarian", "pharmacy"]
}

# Test each option
found_options = []
for letter, order in options.items():
    solver.push()
    # Add constraints for this option
    for b, pos_val in zip(order, range(1, 8)):
        solver.add(pos(b) == pos_val)
    # Check if the constraints are satisfiable
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output the result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")