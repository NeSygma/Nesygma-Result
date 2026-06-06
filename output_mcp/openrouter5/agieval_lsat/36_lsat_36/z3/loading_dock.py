from z3 import *

# There are 6 bays numbered 1-6.
# Each bay holds a different cargo type.
# Cargo types: fuel, grain, livestock, machinery, produce, textiles
# We'll assign each cargo type a bay number (1-6).

fuel = Int('fuel')
grain = Int('grain')
livestock = Int('livestock')
machinery = Int('machinery')
produce = Int('produce')
textiles = Int('textiles')

cargo_vars = [fuel, grain, livestock, machinery, produce, textiles]

solver = Solver()

# Each bay number is between 1 and 6
for v in cargo_vars:
    solver.add(v >= 1, v <= 6)

# All different
solver.add(Distinct(cargo_vars))

# Constraints:
# 1. grain > livestock
solver.add(grain > livestock)

# 2. livestock > textiles
solver.add(livestock > textiles)

# 3. produce > fuel
solver.add(produce > fuel)

# 4. textiles is next to produce: |textiles - produce| == 1
solver.add(Or(textiles == produce + 1, textiles == produce - 1))

# Additional given: bay 4 is holding produce
solver.add(produce == 4)

# Now we need to determine: for exactly how many of the six bays is the type of cargo completely determined?
# We'll check each bay 1..6 and see if its cargo is forced.

# Let's first get the model
result = solver.check()
if result == sat:
    m = solver.model()
    # Print the assignment
    for v in cargo_vars:
        print(f"{v} = {m[v]}")
    
    # Now determine for each bay, which cargo is forced.
    # We'll do this by checking if there's any alternative assignment.
    # For each bay, we'll try to find a model where that bay's cargo is different.
    
    determined_count = 0
    for bay_num in range(1, 7):
        # Check if bay bay_num has a forced cargo type
        # We'll try to find an alternative model where the cargo at this bay is different
        solver.push()
        # Get the current cargo at this bay
        current_cargo = None
        for v in cargo_vars:
            if m[v].as_long() == bay_num:
                current_cargo = v
                break
        # Add constraint that this bay's cargo is NOT the current one
        solver.add(current_cargo != bay_num)
        alt_result = solver.check()
        if alt_result == unsat:
            # No alternative: this bay's cargo is forced
            determined_count += 1
        solver.pop()
    
    print(f"Determined bays: {determined_count}")
    
    # Now evaluate the answer choices
    # A: two -> determined_count == 2
    # B: three -> determined_count == 3
    # C: four -> determined_count == 4
    # D: five -> determined_count == 5
    # E: six -> determined_count == 6
    
    found_options = []
    for letter, constr in [("A", determined_count == 2), ("B", determined_count == 3), 
                           ("C", determined_count == 4), ("D", determined_count == 5),
                           ("E", determined_count == 6)]:
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
else:
    print("STATUS: unsat")
    print("No solution found")