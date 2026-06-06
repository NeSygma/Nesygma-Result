from z3 import *

# BENCHMARK_MODE is ON for this problem
BENCHMARK_MODE = True

# Declare the businesses as symbolic constants
Optometrist, Pharmacy, Restaurant1, Restaurant2, ShoeStore, ToyStore, Veterinarian = Ints('Optometrist Pharmacy Restaurant1 Restaurant2 ShoeStore ToyStore Veterinarian')

# Declare the spaces as a list of integers representing the business in each space
spaces = [Int(f'space_{i}') for i in range(7)]

# Each space must be assigned a unique business
solver = Solver()
solver.add(Distinct(spaces))

# Assign each business to a space
businesses = [Optometrist, Pharmacy, Restaurant1, Restaurant2, ShoeStore, ToyStore, Veterinarian]

# Base constraints from the problem statement

# 1. The pharmacy must be at one end of the row and one of the restaurants at the other.
solver.add(Or(spaces[0] == Pharmacy, spaces[6] == Pharmacy))  # Pharmacy at one end
solver.add(Or(spaces[0] == Restaurant1, spaces[0] == Restaurant2, spaces[6] == Restaurant1, spaces[6] == Restaurant2))  # A restaurant at the other end

# 2. The two restaurants must be separated by at least two other businesses.
# We will enforce this after assigning values to spaces

# 3. The pharmacy must be next to either the optometrist or the veterinarian.
# We will enforce this after assigning values to spaces

# 4. The toy store cannot be next to the veterinarian.
# We will enforce this after assigning values to spaces

# Helper function to check adjacency
def adjacent(a, b, spaces):
    return Or(
        And(spaces[0] == a, spaces[1] == b),
        And(spaces[1] == a, spaces[0] == b),
        And(spaces[1] == a, spaces[2] == b),
        And(spaces[2] == a, spaces[1] == b),
        And(spaces[2] == a, spaces[3] == b),
        And(spaces[3] == a, spaces[2] == b),
        And(spaces[3] == a, spaces[4] == b),
        And(spaces[4] == a, spaces[3] == b),
        And(spaces[4] == a, spaces[5] == b),
        And(spaces[5] == a, spaces[4] == b),
        And(spaces[5] == a, spaces[6] == b),
        And(spaces[6] == a, spaces[5] == b)
    )

# Enforce the constraints after assigning values to spaces
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract the positions of the businesses
    space_vals = [model.eval(space) for space in spaces]
    
    # Extract the positions of the restaurants
    restaurant1_pos = None
    restaurant2_pos = None
    for i in range(7):
        if model.eval(spaces[i]) == Restaurant1:
            restaurant1_pos = i
        if model.eval(spaces[i]) == Restaurant2:
            restaurant2_pos = i
    
    # Ensure the restaurants are separated by at least two businesses
    if restaurant1_pos is not None and restaurant2_pos is not None:
        if abs(restaurant1_pos - restaurant2_pos) < 3:
            solver.add(Or(abs(restaurant1_pos - restaurant2_pos) >= 3))
            result = solver.check()
            if result == unsat:
                print("STATUS: unsat")
                print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
                exit()
    
    # Ensure the pharmacy is next to the optometrist or veterinarian
    pharmacy_pos = None
    for i in range(7):
        if model.eval(spaces[i]) == Pharmacy:
            pharmacy_pos = i
    
    if pharmacy_pos is not None:
        solver.add(Or(
            And(pharmacy_pos > 0, spaces[pharmacy_pos - 1] == Optometrist),
            And(pharmacy_pos < 6, spaces[pharmacy_pos + 1] == Optometrist),
            And(pharmacy_pos > 0, spaces[pharmacy_pos - 1] == Veterinarian),
            And(pharmacy_pos < 6, spaces[pharmacy_pos + 1] == Veterinarian)
        ))
        result = solver.check()
        if result == unsat:
            print("STATUS: unsat")
            print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
            exit()
    
    # Ensure the toy store is not next to the veterinarian
    toy_store_pos = None
    veterinarian_pos = None
    for i in range(7):
        if model.eval(spaces[i]) == ToyStore:
            toy_store_pos = i
        if model.eval(spaces[i]) == Veterinarian:
            veterinarian_pos = i
    
    if toy_store_pos is not None and veterinarian_pos is not None:
        solver.add(Not(Or(
            And(toy_store_pos > 0, spaces[toy_store_pos - 1] == Veterinarian),
            And(toy_store_pos < 6, spaces[toy_store_pos + 1] == Veterinarian)
        )))
        result = solver.check()
        if result == unsat:
            print("STATUS: unsat")
            print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
            exit()
    
    # Now, check the specific condition: If the optometrist is next to the shoe store, the businesses immediately on either side of this pair must be...
    optometrist_pos = None
    shoe_store_pos = None
    for i in range(7):
        if model.eval(spaces[i]) == Optometrist:
            optometrist_pos = i
        if model.eval(spaces[i]) == ShoeStore:
            shoe_store_pos = i
    
    if optometrist_pos is not None and shoe_store_pos is not None:
        if abs(optometrist_pos - shoe_store_pos) == 1:
            # The optometrist is next to the shoe store
            # Determine the pair's position
            if optometrist_pos < shoe_store_pos:
                pair_left = optometrist_pos
                pair_right = shoe_store_pos
            else:
                pair_left = shoe_store_pos
                pair_right = optometrist_pos
            
            # The businesses immediately on either side of this pair are at pair_left - 1 and pair_right + 1
            left_side = pair_left - 1 if pair_left > 0 else None
            right_side = pair_right + 1 if pair_right < 6 else None
            
            # Now, we need to check the answer choices
            found_options = []
            
            # Choice A: the pharmacy and a restaurant
            solver.push()
            if left_side is not None and right_side is not None:
                solver.add(Or(
                    And(spaces[left_side] == Pharmacy, Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2)),
                    And(spaces[right_side] == Pharmacy, Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2))
                ))
            elif left_side is not None:
                solver.add(spaces[left_side] == Pharmacy)
            elif right_side is not None:
                solver.add(spaces[right_side] == Pharmacy)
            
            if solver.check() == sat:
                found_options.append("A")
            solver.pop()
            
            # Choice B: the pharmacy and the toy store
            solver.push()
            if left_side is not None and right_side is not None:
                solver.add(Or(
                    And(spaces[left_side] == Pharmacy, spaces[right_side] == ToyStore),
                    And(spaces[right_side] == Pharmacy, spaces[left_side] == ToyStore)
                ))
            elif left_side is not None:
                solver.add(spaces[left_side] == Pharmacy)
            elif right_side is not None:
                solver.add(spaces[right_side] == Pharmacy)
            
            if solver.check() == sat:
                found_options.append("B")
            solver.pop()
            
            # Choice C: the two restaurants
            solver.push()
            if left_side is not None and right_side is not None:
                solver.add(Or(
                    And(spaces[left_side] == Restaurant1, spaces[right_side] == Restaurant2),
                    And(spaces[left_side] == Restaurant2, spaces[right_side] == Restaurant1)
                ))
            elif left_side is not None:
                solver.add(Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2))
            elif right_side is not None:
                solver.add(Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2))
            
            if solver.check() == sat:
                found_options.append("C")
            solver.pop()
            
            # Choice D: a restaurant and the toy store
            solver.push()
            if left_side is not None and right_side is not None:
                solver.add(Or(
                    And(Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2), spaces[right_side] == ToyStore),
                    And(Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2), spaces[left_side] == ToyStore)
                ))
            elif left_side is not None:
                solver.add(Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2))
            elif right_side is not None:
                solver.add(Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2))
            
            if solver.check() == sat:
                found_options.append("D")
            solver.pop()
            
            # Choice E: a restaurant and the veterinarian
            solver.push()
            if left_side is not None and right_side is not None:
                solver.add(Or(
                    And(Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2), spaces[right_side] == Veterinarian),
                    And(Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2), spaces[left_side] == Veterinarian)
                ))
            elif left_side is not None:
                solver.add(Or(spaces[left_side] == Restaurant1, spaces[left_side] == Restaurant2))
            elif right_side is not None:
                solver.add(Or(spaces[right_side] == Restaurant1, spaces[right_side] == Restaurant2))
            
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
        else:
            print("STATUS: unsat")
            print("Refine: Optometrist is not next to the shoe store in the model")
    else:
        print("STATUS: unsat")
        print("Refine: Could not find optometrist or shoe store positions")
else:
    print("STATUS: unknown")