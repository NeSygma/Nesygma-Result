from z3 import *

# Problem data
universe = [1, 2, 3, 4, 5, 6, 7, 8]
sets = [
    [1, 2, 3],    # Set 0
    [2, 4, 5],    # Set 1
    [3, 6, 7],    # Set 2
    [1, 4, 8],    # Set 3
    [5, 6, 7, 8], # Set 4
    [1, 2, 6]     # Set 5
]

# Create optimization solver
opt = Optimize()

# Binary variables for set selection
selected = [Bool(f'set_{i}') for i in range(6)]

# Objective: minimize number of selected sets
num_selected = Sum([If(selected[i], 1, 0) for i in range(6)])
opt.minimize(num_selected)

# Constraint: each element must be covered by at least one selected set
for element in universe:
    # Check which sets contain this element
    covering_sets = [i for i, s in enumerate(sets) if element in s]
    if covering_sets:
        # At least one of the covering sets must be selected
        opt.add(Or([selected[i] for i in covering_sets]))
    else:
        # This shouldn't happen with our data, but handle gracefully
        print(f"Warning: Element {element} not in any set!")

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract selected sets
    selected_sets = []
    for i in range(6):
        if is_true(model[selected[i]]):
            selected_sets.append(i)
    
    # Calculate covered elements
    covered_elements = set()
    for i in selected_sets:
        covered_elements.update(sets[i])
    
    # Sort for consistent output
    covered_elements = sorted(list(covered_elements))
    
    print(f"selected_sets: {selected_sets}")
    print(f"total_sets: {len(selected_sets)}")
    print(f"covered_elements: {covered_elements}")
    print(f"Optimal number of sets: {len(selected_sets)}")
    
    # Verify coverage
    if covered_elements == universe:
        print("✓ All elements covered!")
    else:
        print("✗ Not all elements covered!")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")