from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# We'll solve the problem by finding all possible assignments that satisfy the constraints
# Then determine how many bays are uniquely determined

# Create variables for which bay holds each cargo type
# Bay numbers are 1-6
fuel_bay = Int('fuel_bay')
grain_bay = Int('grain_bay')
livestock_bay = Int('livestock_bay')
machinery_bay = Int('machinery_bay')
produce_bay = Int('produce_bay')
textiles_bay = Int('textiles_bay')

# All bays must be between 1 and 6
solver = Solver()
solver.add(fuel_bay >= 1, fuel_bay <= 6)
solver.add(grain_bay >= 1, grain_bay <= 6)
solver.add(livestock_bay >= 1, livestock_bay <= 6)
solver.add(machinery_bay >= 1, machinery_bay <= 6)
solver.add(produce_bay >= 1, produce_bay <= 6)
solver.add(textiles_bay >= 1, textiles_bay <= 6)

# All bays must be distinct (each cargo type is in a different bay)
solver.add(Distinct([fuel_bay, grain_bay, livestock_bay, machinery_bay, produce_bay, textiles_bay]))

# Given constraint: Bay 4 is holding produce
solver.add(produce_bay == 4)

# Constraint 1: The bay holding grain has a higher number than the bay holding livestock
solver.add(grain_bay > livestock_bay)

# Constraint 2: The bay holding livestock has a higher number than the bay holding textiles
solver.add(livestock_bay > textiles_bay)

# Constraint 3: The bay holding produce has a higher number than the bay holding fuel
solver.add(produce_bay > fuel_bay)

# Constraint 4: The bay holding textiles is next to the bay holding produce
solver.add(Or(textiles_bay == produce_bay - 1, textiles_bay == produce_bay + 1))

# Find all solutions
solutions = []
decision_vars = [fuel_bay, grain_bay, livestock_bay, machinery_bay, produce_bay, textiles_bay]

while solver.check() == sat:
    model = solver.model()
    # Record the current solution
    sol = {v: model[v] for v in decision_vars}
    solutions.append(sol)
    
    # Block this solution to find the next one
    solver.add(Or([v != model[v] for v in decision_vars]))

# Now analyze the solutions to see which bays are uniquely determined
if len(solutions) > 0:
    # Initialize counts for each bay being the same across all solutions
    bay_counts = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}
    
    for sol in solutions:
        for bay_num in range(1, 7):
            # For each bay number, track what cargo type is assigned
            # We need to find which cargo type is at this bay in the solution
            # Since we have variables for which bay holds each cargo, we need to invert this
            pass
    
    # Better approach: For each solution, create a mapping from bay number to cargo type
    # Then check consistency across solutions
    bay_to_cargo_across_solutions = {}
    
    for sol in solutions:
        # Invert the solution: for each bay number, what cargo is there?
        bay_to_cargo = {}
        for cargo_var, bay_num in sol.items():
            # cargo_var is like fuel_bay, grain_bay, etc.
            # bay_num is the actual bay number (IntVal)
            cargo_type = str(cargo_var).split('_')[0]  # Extract cargo type name
            actual_bay = bay_num.as_long()
            bay_to_cargo[actual_bay] = cargo_type
        
        for bay_num in range(1, 7):
            cargo_type = bay_to_cargo.get(bay_num)
            if cargo_type is not None:
                if bay_num not in bay_to_cargo_across_solutions:
                    bay_to_cargo_across_solutions[bay_num] = []
                bay_to_cargo_across_solutions[bay_num].append(cargo_type)
    
    # Count how many bays have the same cargo type in all solutions
    determined_bays_count = 0
    for bay_num in range(1, 7):
        if bay_num in bay_to_cargo_across_solutions:
            cargo_types = bay_to_cargo_across_solutions[bay_num]
            if len(set(cargo_types)) == 1:
                determined_bays_count += 1
    
    print(f"STATUS: sat")
    print(f"Total solutions found: {len(solutions)}")
    print(f"Number of bays with determined cargo: {determined_bays_count}")
    
    # Now test each answer choice to see which one matches
    found_options = []
    for letter, expected_count in [("A", 2), ("B", 3), ("C", 4), ("D", 5), ("E", 6)]:
        solver.push()
        solver.add(produce_bay == 4)  # Base constraint
        # Add constraint that the number of determined bays equals expected_count
        # We can't directly constrain this, so we just check if our count matches
        # Instead, we'll just verify the count we computed
        if determined_bays_count == expected_count:
            found_options.append(letter)
        solver.pop()
    
    if len(found_options) == 1:
        print(f"answer:{found_options[0]}")
    elif len(found_options) > 1:
        print("STATUS: unsat")
        print(f"Refine: Multiple options found {found_options}")
    else:
        print("STATUS: unsat")
        print("Refine: No options found")
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (no solutions found in benchmark mode; refine required)")