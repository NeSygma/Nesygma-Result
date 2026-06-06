from z3 import *

# Problem data
num_sets = 14
num_elements = 20

# Set definitions: each set contains certain elements
set_elements = {
    0: {1, 2, 3, 4, 5},
    1: {1, 6, 11, 16},
    2: {2, 7, 12, 17},
    3: {3, 8, 13, 18},
    4: {4, 9, 14, 19},
    5: {5, 10, 15, 20},
    6: {6, 7, 8, 9, 10},
    7: {1, 3, 5, 7, 9},
    8: {2, 4, 6, 8, 10},
    9: {1, 2, 3, 4, 5, 6, 7},
    10: {11, 12, 13, 14, 15},
    11: {8, 9, 10},
    12: {1, 5, 10, 15},
    13: {16, 17, 18, 19, 20},
}

# Costs
cost = [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4]

# Categories: A=0, B=1, C=2, Specialized=3
category = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3]

# Standard categories: A=0, B=1, C=2
# Specialized sets: 9, 10, 11, 12, 13

opt = Optimize()

# Decision variables: whether each set is selected
selected = [Bool(f's_{i}') for i in range(num_sets)]

# For each element, track how many sets cover it
# coverage_count[e] = number of selected sets that contain element e
coverage_count = [Int(f'cov_{e}') for e in range(1, num_elements + 1)]

for e in range(1, num_elements + 1):
    # Count how many selected sets cover element e
    covering_sets = [If(selected[s], 1, 0) for s in range(num_sets) if e in set_elements[s]]
    opt.add(coverage_count[e - 1] == Sum(covering_sets))
    # Full coverage: each element must be covered by at least 1 set
    opt.add(coverage_count[e - 1] >= 1)

# Prerequisites:
# Selecting Set 9 requires selecting Set 0
opt.add(Implies(selected[9], selected[0]))
# Selecting Set 11 requires selecting Set 6
opt.add(Implies(selected[11], selected[6]))

# Mutual exclusion: Set 12 and Set 13 cannot both be selected
opt.add(Not(And(selected[12], selected[13])))

# Category Balancing: If any specialized set is selected, must have at least one from A, B, C
any_specialized = Or([selected[s] for s in [9, 10, 11, 12, 13]])
has_cat_a = Or([selected[s] for s in [0, 1, 2]])
has_cat_b = Or([selected[s] for s in [3, 4, 5]])
has_cat_c = Or([selected[s] for s in [6, 7, 8]])

opt.add(Implies(any_specialized, And(has_cat_a, has_cat_b, has_cat_c)))

# Base cost: sum of costs of selected sets
base_cost = Sum([If(selected[s], cost[s], 0) for s in range(num_sets)])

# Redundancy penalty: for each element covered by more than 3 sets, add penalty of 2
# penalty_per_element[e] = 2 if coverage_count[e] > 3, else 0
penalty_per_element = [If(coverage_count[e] > 3, 2, 0) for e in range(num_elements)]
redundancy_penalty = Sum(penalty_per_element)

# Total cost
total_cost = base_cost + redundancy_penalty

# Minimize total cost
opt.minimize(total_cost)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    
    # Extract selected sets
    selected_sets = [i for i in range(num_sets) if is_true(m[selected[i]])]
    total_sets = len(selected_sets)
    
    # Extract coverage
    covered_elements = list(range(1, num_elements + 1))  # All should be covered
    
    # Compute base cost
    base_cost_val = sum(cost[s] for s in selected_sets)
    
    # Compute redundancy penalty
    redundancy_penalty_val = 0
    for e in range(1, num_elements + 1):
        cov = m.evaluate(coverage_count[e - 1])
        if cov.as_long() > 3:
            redundancy_penalty_val += 2
    
    total_cost_val = base_cost_val + redundancy_penalty_val
    
    print("STATUS: sat")
    print(f"selected_sets: {selected_sets}")
    print(f"total_sets: {total_sets}")
    print(f"covered_elements: {covered_elements}")
    print(f"base_cost: {base_cost_val}")
    print(f"redundancy_penalty: {redundancy_penalty_val}")
    print(f"total_cost: {total_cost_val}")
    
    # Print coverage details for verification
    print("\nCoverage details:")
    for e in range(1, num_elements + 1):
        cov = m.evaluate(coverage_count[e - 1]).as_long()
        covering = [s for s in selected_sets if e in set_elements[s]]
        print(f"  Element {e}: covered {cov} time(s) by sets {covering}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")
    print("Solver returned unknown.")