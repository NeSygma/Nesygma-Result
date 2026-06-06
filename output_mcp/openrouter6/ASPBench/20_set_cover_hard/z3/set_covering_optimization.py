from z3 import *

# Universe elements 1..20
elements = list(range(1, 21))

# Sets data: each set is a tuple (index, elements, cost, category)
sets_data = [
    (0, [1,2,3,4,5], 1, 'A'),
    (1, [1,6,11,16], 1, 'A'),
    (2, [2,7,12,17], 1, 'A'),
    (3, [3,8,13,18], 1, 'B'),
    (4, [4,9,14,19], 1, 'B'),
    (5, [5,10,15,20], 1, 'B'),
    (6, [6,7,8,9,10], 1, 'C'),
    (7, [1,3,5,7,9], 1, 'C'),
    (8, [2,4,6,8,10], 1, 'C'),
    (9, [1,2,3,4,5,6,7], 4, 'specialized'),
    (10, [11,12,13,14,15], 4, 'specialized'),
    (11, [8,9,10], 4, 'specialized'),
    (12, [1,5,10,15], 4, 'specialized'),
    (13, [16,17,18,19,20], 4, 'specialized')
]

# Create binary selection variables for each set
selected = [Bool(f'set_{i}') for i in range(14)]

# Costs for each set
costs = [s[2] for s in sets_data]

# Categories for each set
categories = [s[3] for s in sets_data]

# Create a mapping from element to list of set indices that cover it
element_to_sets = {e: [] for e in elements}
for idx, elems, _, _ in sets_data:
    for e in elems:
        element_to_sets[e].append(idx)

# Coverage constraints: each element must be covered by at least one selected set
solver = Solver()
for e in elements:
    covering_sets = element_to_sets[e]
    solver.add(Or([selected[idx] for idx in covering_sets]))

# Prerequisite constraints
# Set 9 requires Set 0
solver.add(Implies(selected[9], selected[0]))
# Set 11 requires Set 6
solver.add(Implies(selected[11], selected[6]))

# Mutual exclusion: Set 12 and Set 13 cannot both be selected
solver.add(Not(And(selected[12], selected[13])))

# Category balancing: If any specialized set is selected, must include at least one from A, B, C
# Specialized sets are indices 9,10,11,12,13
specialized_indices = [9,10,11,12,13]
# Standard categories: A:0,1,2; B:3,4,5; C:6,7,8
category_A = [0,1,2]
category_B = [3,4,5]
category_C = [6,7,8]

# Boolean: is any specialized set selected?
any_specialized = Or([selected[i] for i in specialized_indices])
# Boolean: at least one from each category
at_least_one_A = Or([selected[i] for i in category_A])
at_least_one_B = Or([selected[i] for i in category_B])
at_least_one_C = Or([selected[i] for i in category_C])

solver.add(Implies(any_specialized, And(at_least_one_A, at_least_one_B, at_least_one_C)))

# Compute coverage count for each element
coverage_count = {}
for e in elements:
    # Sum of selected sets covering element e
    count_expr = Sum([If(selected[idx], 1, 0) for idx in element_to_sets[e]])
    coverage_count[e] = count_expr

# Compute redundancy penalty: for each element, if coverage count > 3, add 2
penalty_terms = []
for e in elements:
    # If coverage_count[e] > 3, then add 2, else 0
    penalty_terms.append(If(coverage_count[e] > 3, 2, 0))
redundancy_penalty = Sum(penalty_terms)

# Compute base cost: sum of costs of selected sets
base_cost = Sum([If(selected[i], costs[i], 0) for i in range(14)])

# Total cost
total_cost = base_cost + redundancy_penalty

# Minimize total cost
opt = Optimize()
opt.add(solver.assertions())  # Add all constraints from solver
opt.minimize(total_cost)

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    # Extract selected sets
    selected_sets = [i for i in range(14) if is_true(model[selected[i]])]
    print(f"selected_sets: {selected_sets}")
    print(f"total_sets: {len(selected_sets)}")
    # Covered elements: all elements 1..20 (by constraint)
    covered_elements = elements
    print(f"covered_elements: {covered_elements}")
    # Base cost
    base_cost_val = sum(costs[i] for i in selected_sets)
    print(f"base_cost: {base_cost_val}")
    # Redundancy penalty
    penalty_val = 0
    for e in elements:
        count = sum(1 for idx in element_to_sets[e] if is_true(model[selected[idx]]))
        if count > 3:
            penalty_val += 2
    print(f"redundancy_penalty: {penalty_val}")
    total_cost_val = base_cost_val + penalty_val
    print(f"total_cost: {total_cost_val}")
    # Check if total cost matches expected optimal cost (5)
    if total_cost_val == 5:
        print("Optimal cost achieved: 5")
    else:
        print(f"Note: total cost is {total_cost_val}, expected optimal is 5")
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")