from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare symbolic variables for the seven spaces
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# Businesses as symbolic constants
optometrist = Int('optometrist')
pharmacy = Int('pharmacy')
restaurant = Int('restaurant')
restaurant2 = Int('restaurant2')  # Second restaurant
shoe_store = Int('shoe_store')
toy_store = Int('toy_store')
veterinarian = Int('veterinarian')

# All businesses must be assigned to a unique space
all_businesses = [optometrist, pharmacy, restaurant, restaurant2, shoe_store, toy_store, veterinarian]

# Base constraints
solver = Solver()

# Each business is assigned to a unique space
solver.add(Distinct(all_businesses))
for i, space in enumerate(spaces, start=1):
    solver.add(Or([b == i for b in all_businesses]))

# The pharmacy must be at one end of the row and one of the restaurants at the other.
# Ends are spaces 1 and 7
solver.add(Or(pharmacy == 1, pharmacy == 7))
solver.add(Or(restaurant == 1, restaurant == 7, restaurant2 == 1, restaurant2 == 7))

# Ensure one restaurant is at one end and pharmacy at the other
solver.add(Not(And(pharmacy == 1, restaurant == 1)))
solver.add(Not(And(pharmacy == 1, restaurant2 == 1)))
solver.add(Not(And(pharmacy == 7, restaurant == 7)))
solver.add(Not(And(pharmacy == 7, restaurant2 == 7)))

# The two restaurants must be separated by at least two other businesses.
# This means the absolute difference in their positions must be at least 3.
solver.add(Abs(restaurant - restaurant2) >= 3)

# The pharmacy must be next to either the optometrist or the veterinarian.
# Next means adjacent spaces (difference of 1)
solver.add(Or(Abs(pharmacy - optometrist) == 1, Abs(pharmacy - veterinarian) == 1))

# The toy store cannot be next to the veterinarian.
solver.add(Abs(toy_store - veterinarian) != 1)

# Given: The veterinarian is in space 5
solver.add(veterinarian == 5)

# Evaluate each option under the condition that it must be true
found_options = []

# Option A: The optometrist is in space 2
solver.push()
solver.add(optometrist == 2)
# Ensure no other option is valid under this constraint
solver.add(pharmacy != 7)
solver.add(Or(restaurant != 4, restaurant2 != 4))
solver.add(shoe_store != 6)
solver.add(toy_store != 3)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The pharmacy is in space 7
solver.push()
solver.add(pharmacy == 7)
# Ensure no other option is valid under this constraint
solver.add(optometrist != 2)
solver.add(Or(restaurant != 4, restaurant2 != 4))
solver.add(shoe_store != 6)
solver.add(toy_store != 3)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is in space 4
solver.push()
solver.add(Or(restaurant == 4, restaurant2 == 4))
# Ensure no other option is valid under this constraint
solver.add(optometrist != 2)
solver.add(pharmacy != 7)
solver.add(shoe_store != 6)
solver.add(toy_store != 3)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The shoe store is in space 6
solver.push()
solver.add(shoe_store == 6)
# Ensure no other option is valid under this constraint
solver.add(optometrist != 2)
solver.add(pharmacy != 7)
solver.add(Or(restaurant != 4, restaurant2 != 4))
solver.add(toy_store != 3)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The toy store is in space 3
solver.push()
solver.add(toy_store == 3)
# Ensure no other option is valid under this constraint
solver.add(optometrist != 2)
solver.add(pharmacy != 7)
solver.add(Or(restaurant != 4, restaurant2 != 4))
solver.add(shoe_store != 6)
if solver.check() == sat:
    found_options.append("E")
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