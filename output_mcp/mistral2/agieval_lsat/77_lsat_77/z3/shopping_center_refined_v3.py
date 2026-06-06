from z3 import *

solver = Solver()

# Declare symbolic variables for each space (1 to 7)
# Each space will be assigned a business type
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# Business types as integers for easier constraint handling
optometrist = 1
pharmacy = 2
restaurant = 3
shoe_store = 5
toy_store = 6
veterinarian = 7

# Each space must be assigned a unique business type
solver.add(Distinct(spaces))

# The pharmacy must be at one end of the row and one of the restaurants at the other
# Let's assume space 1 and space 7 are the ends
solver.add(Or(spaces[0] == pharmacy, spaces[6] == pharmacy))  # pharmacy is at one end
solver.add(Or(spaces[0] == restaurant, spaces[6] == restaurant))  # one restaurant is at the other end

# The two restaurants must be separated by at least two other businesses
# Find the indices of the two restaurants
restaurant_indices = [i for i in range(7) if spaces[i] == restaurant]
# The difference in their positions must be at least 3 (since they are separated by at least two businesses)
if len(restaurant_indices) == 2:
    solver.add(Abs(restaurant_indices[0] - restaurant_indices[1]) >= 3)

# The pharmacy must be next to either the optometrist or the veterinarian
# Define a helper function to find the index of a business type

def find_index(business_type):
    return [i for i in range(7) if spaces[i] == business_type]

pharmacy_indices = find_index(pharmacy)
optometrist_indices = find_index(optometrist)
veterinarian_indices = find_index(veterinarian)

# The pharmacy must be next to either the optometrist or the veterinarian
if len(pharmacy_indices) == 1 and len(optometrist_indices) == 1:
    solver.add(Abs(pharmacy_indices[0] - optometrist_indices[0]) == 1)
if len(pharmacy_indices) == 1 and len(veterinarian_indices) == 1:
    solver.add(Abs(pharmacy_indices[0] - veterinarian_indices[0]) == 1)

# The toy store cannot be next to the veterinarian
toy_store_indices = find_index(toy_store)
if len(toy_store_indices) == 1 and len(veterinarian_indices) == 1:
    solver.add(Abs(toy_store_indices[0] - veterinarian_indices[0]) != 1)

# The shoe store is in space 2
solver.add(spaces[1] == shoe_store)  # shoe_store is at index 1 (space 2)

# Now, let's evaluate the multiple choice options
found_options = []

# Option A: The optometrist is in space 5
solver.push()
solver.add(spaces[4] == optometrist)  # space 5 (index 4) is optometrist
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The pharmacy is in space 1
solver.push()
solver.add(spaces[0] == pharmacy)  # pharmacy is in space 1
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is in space 3
solver.push()
solver.add(spaces[2] == restaurant)  # space 3 (index 2) is a restaurant
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The toy store is in space 6
solver.push()
solver.add(spaces[5] == toy_store)  # space 6 (index 5) is toy_store
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The veterinarian is in space 4
solver.push()
solver.add(spaces[3] == veterinarian)  # space 4 (index 3) is veterinarian
if solver.check() == sat:
    found_options.append("E")
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