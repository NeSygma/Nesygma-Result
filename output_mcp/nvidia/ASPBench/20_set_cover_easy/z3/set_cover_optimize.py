from z3 import *

# Universe elements
universe = [1, 2, 3, 4, 5, 6, 7, 8]

# Sets definitions
sets = [
    [1, 2, 3],      # Set 0
    [2, 4, 5],      # Set 1
    [3, 6, 7],      # Set 2
    [1, 4, 8],      # Set 3
    [5, 6, 7, 8],   # Set 4
    [1, 2, 6]       # Set 5
]

# Boolean variable for each set
selected = [Bool(f's{i}') for i in range(len(sets))]

# Optimize for minimization
opt = Optimize()

# Coverage constraint: each element must be covered by at least one selected set
for e in universe:
    covering = [selected[i] for i, s in enumerate(sets) if e in s]
    opt.add(Or(covering))

# Objective: minimize number of selected sets
opt.minimize(Sum([If(selected[i], 1, 0) for i in range(len(sets))]))

# Solve
result = opt.check()
if result == sat:
    model = opt.model()
    # Extract selected set indices
    selected_sets = [i for i in range(len(sets)) if model[selected[i]]]
    total_sets = len(selected_sets)
    # Compute covered elements (should be all universe)
    covered_elements = []
    for e in universe:
        for i, s in enumerate(sets):
            if i in selected_sets and e in s:
                covered_elements.append(e)
                break
    # Output required information
    print("STATUS: sat")
    print(f"selected_sets = {selected_sets}")
    print(f"total_sets = {total_sets}")
    print(f"covered_elements = {covered_elements}")
else:
    print("STATUS: unsat")