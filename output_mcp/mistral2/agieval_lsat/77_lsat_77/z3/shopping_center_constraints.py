from z3 import *

solver = Solver()

# Declare symbolic variables for each space (1 to 7)
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# Assign business types to spaces
businesses = [
    "optometrist",
    "pharmacy",
    "restaurant",
    "restaurant",
    "shoe_store",
    "toy_store",
    "veterinarian"
]

# Each space must be assigned a unique business
solver.add(Distinct(spaces))

# The pharmacy must be at one end of the row and one of the restaurants at the other
# Let's assume space 1 and space 7 are the ends
solver.add(Or(spaces[0] == 2, spaces[6] == 2))  # pharmacy is at one end
solver.add(Or(spaces[0] == 3, spaces[6] == 3))  # one restaurant is at the other end

# The two restaurants must be separated by at least two other businesses
# Find the indices of the two restaurants
restaurant_indices = [i for i in range(7) if businesses[i] == "restaurant"]
# Since we have two restaurants, we need to ensure they are separated by at least two spaces
# This is a bit tricky because we don't know which spaces they occupy yet
# We'll handle this after assigning spaces to businesses

# The pharmacy must be next to either the optometrist or the veterinarian
# We'll handle this after assigning spaces to businesses

# The toy store cannot be next to the veterinarian
# We'll handle this after assigning spaces to businesses

# The shoe store is in space 2
solver.add(spaces[1] == 5)  # shoe_store is at index 1 (space 2)

# Now, let's assign businesses to spaces
# We need to ensure that the constraints are satisfied
# We'll use a mapping from business to its index in the spaces list
business_to_index = {}
for i, business in enumerate(businesses):
    business_to_index[business] = spaces[i]

# Pharmacy must be at one end
solver.add(Or(business_to_index["pharmacy"] == spaces[0], business_to_index["pharmacy"] == spaces[6]))

# One restaurant must be at the other end
solver.add(Or(business_to_index["restaurant"] == spaces[0], business_to_index["restaurant"] == spaces[6]))

# The two restaurants must be separated by at least two other businesses
# We need to find the indices of the two restaurants
restaurant_indices = [i for i in range(7) if businesses[i] == "restaurant"]
# The actual spaces occupied by restaurants
restaurant_spaces = [spaces[i] for i in restaurant_indices]
# The difference in their positions must be at least 3 (since they are separated by at least two businesses)
solver.add(Abs(restaurant_spaces[0] - restaurant_spaces[1]) >= 3)

# The pharmacy must be next to either the optometrist or the veterinarian
pharmacy_space = business_to_index["pharmacy"]
optometrist_space = business_to_index["optometrist"]
veterinarian_space = business_to_index["veterinarian"]
solver.add(Or(
    Abs(pharmacy_space - optometrist_space) == 1,
    Abs(pharmacy_space - veterinarian_space) == 1
))

# The toy store cannot be next to the veterinarian
toy_store_space = business_to_index["toy_store"]
solver.add(Abs(toy_store_space - veterinarian_space) != 1)

# Now, let's evaluate the multiple choice options
found_options = []

# Option A: The optometrist is in space 5
solver.push()
solver.add(business_to_index["optometrist"] == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The pharmacy is in space 1
solver.push()
solver.add(business_to_index["pharmacy"] == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is in space 3
solver.push()
solver.add(Or(business_to_index["restaurant"] == 3, 
              And(business_to_index["restaurant"] == 3, 
                  business_to_index["restaurant"] == 3)))  # This is redundant, but ensures clarity
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The toy store is in space 6
solver.push()
solver.add(business_to_index["toy_store"] == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The veterinarian is in space 4
solver.push()
solver.add(business_to_index["veterinarian"] == 4)
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