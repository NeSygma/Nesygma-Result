from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Declare businesses as symbolic constants
optometrist = Int('optometrist')
pharmacy = Int('pharmacy')
restaurant1 = Int('restaurant1')
restaurant2 = Int('restaurant2')
shoe_store = Int('shoe_store')
toy_store = Int('toy_store')
veterinarian = Int('veterinarian')

# Declare spaces as symbolic constants (1 through 7)
spaces = [Int(f'space_{i}') for i in range(1, 8)]

# All businesses must be assigned to exactly one space
all_businesses = [optometrist, pharmacy, restaurant1, restaurant2, shoe_store, toy_store, veterinarian]

# Each space must have exactly one business
solver = Solver()
for space in spaces:
    solver.add(Or([space == b for b in all_businesses]))
    solver.add(Distinct([space == b for b in all_businesses]))  # Ensure only one business per space

# Each business must be assigned to exactly one space
for b in all_businesses:
    solver.add(Or([b == space for space in spaces]))
    solver.add(Distinct([b == space for space in spaces]))  # Ensure only one space per business

# Constraint 1: Pharmacy must be at one end (space 1 or 7), and one restaurant at the other end
solver.add(Or(pharmacy == 1, pharmacy == 7))
solver.add(Or(restaurant1 == 1, restaurant1 == 7, restaurant2 == 1, restaurant2 == 7))
# Ensure the other end is a restaurant if pharmacy is at one end
solver.add(Not(And(pharmacy == 1, restaurant1 != 7, restaurant2 != 7)))
solver.add(Not(And(pharmacy == 7, restaurant1 != 1, restaurant2 != 1)))

# Constraint 2: The two restaurants must be separated by at least two other businesses
solver.add(Abs(restaurant1 - restaurant2) >= 3)

# Constraint 3: Pharmacy must be next to either the optometrist or the veterinarian
solver.add(Or(
    And(pharmacy == 1, Or(optometrist == 2, veterinarian == 2)),
    And(pharmacy == 7, Or(optometrist == 6, veterinarian == 6)),
    And(pharmacy > 1, pharmacy < 7, Or(
        And(optometrist == pharmacy - 1),
        And(optometrist == pharmacy + 1),
        And(veterinarian == pharmacy - 1),
        And(veterinarian == pharmacy + 1)
    ))
))

# Constraint 4: Toy store cannot be next to the veterinarian
solver.add(Not(Or(
    And(toy_store == 1, veterinarian == 2),
    And(toy_store == 2, veterinarian == 1),
    And(toy_store == 2, veterinarian == 3),
    And(toy_store == 3, veterinarian == 2),
    And(toy_store == 3, veterinarian == 4),
    And(toy_store == 4, veterinarian == 3),
    And(toy_store == 4, veterinarian == 5),
    And(toy_store == 5, veterinarian == 4),
    And(toy_store == 5, veterinarian == 6),
    And(toy_store == 6, veterinarian == 5),
    And(toy_store == 6, veterinarian == 7),
    And(toy_store == 7, veterinarian == 6)
)))

# Condition: Shoe store is in space 2
solver.add(shoe_store == 2)

# Evaluate each option
found_options = []

# Option A: The optometrist is in space 5
solver.push()
solver.add(optometrist == 5)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: The pharmacy is in space 1
solver.push()
solver.add(pharmacy == 1)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: A restaurant is in space 3
solver.push()
solver.add(Or(restaurant1 == 3, restaurant2 == 3))
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: The toy store is in space 6
solver.push()
solver.add(toy_store == 6)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: The veterinarian is in space 4
solver.push()
solver.add(veterinarian == 4)
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