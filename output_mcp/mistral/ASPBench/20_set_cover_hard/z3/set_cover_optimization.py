from z3 import *

# ============================================================================
# Problem: Set Cover with Constraints and Redundancy Penalty
# Universe: Elements 1..20
# Sets: 14 sets with elements, costs, and categories
# Constraints: Full coverage, prerequisites, mutual exclusion, category balancing, redundancy penalty
# Objective: Minimize total cost = base_cost + redundancy_penalty
# ============================================================================

# Initialize optimizer
opt = Optimize()

# ============================================================================
# 1. Declare symbolic variables
# ============================================================================

# Boolean variables for set selection
selected = [Bool(f"selected_{i}") for i in range(14)]

# ============================================================================
# 2. Define set data: elements, cost, category
# ============================================================================

# Elements for each set (1-indexed for clarity)
set_elements = [
    [1, 2, 3, 4, 5],           # Set 0
    [1, 6, 11, 16],            # Set 1
    [2, 7, 12, 17],            # Set 2
    [3, 8, 13, 18],            # Set 3
    [4, 9, 14, 19],            # Set 4
    [5, 10, 15, 20],           # Set 5
    [6, 7, 8, 9, 10],          # Set 6
    [1, 3, 5, 7, 9],           # Set 7
    [2, 4, 6, 8, 10],          # Set 8
    [1, 2, 3, 4, 5, 6, 7],     # Set 9
    [11, 12, 13, 14, 15],      # Set 10
    [8, 9, 10],                # Set 11
    [1, 5, 10, 15],            # Set 12
    [16, 17, 18, 19, 20],      # Set 13
]

# Costs for each set
set_costs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4]

# Categories: A, B, C, or specialized (we'll use strings for clarity)
set_categories = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'specialized', 'specialized', 'specialized', 'specialized', 'specialized']

# Standard categories (A, B, C) correspond to sets 0-8
# Specialized sets are 9-13 (cost > 1)

# ============================================================================
# 3. Add constraints
# ============================================================================

# Constraint 1: Full coverage of all elements 1..20
# We'll track coverage per element using a boolean array
covered = [Bool(f"covered_{e}") for e in range(1, 21)]

# For each element, it is covered if at least one set containing it is selected
for e in range(1, 21):
    # Find all sets that contain element e
    sets_containing_e = [i for i in range(14) if e in set_elements[i]]
    # Element e is covered if any of those sets is selected
    opt.add(covered[e-1] == Or([selected[i] for i in sets_containing_e]))

# Ensure all elements are covered
opt.add(And(covered))

# Constraint 2: Prerequisites
# Selecting Set 9 requires selecting Set 0
opt.add(Implies(selected[9], selected[0]))
# Selecting Set 11 requires selecting Set 6
opt.add(Implies(selected[11], selected[6]))

# Constraint 3: Mutual exclusion: Set 12 and Set 13 cannot both be selected
opt.add(Not(And(selected[12], selected[13])))

# Constraint 4: Category balancing
# If any specialized set (cost > 1) is selected, must include at least one set from each standard category A, B, C
# Standard categories: A (sets 0,1,2), B (sets 3,4,5), C (sets 6,7,8)
# Specialized sets: 9-13

# Helper: define standard category sets
standard_A = [0, 1, 2]
standard_B = [3, 4, 5]
standard_C = [6, 7, 8]

# If any specialized set is selected, enforce category balancing
specialized_selected = Or(selected[9], selected[10], selected[11], selected[12], selected[13])

# Enforce that if specialized_selected, then at least one from A, B, C is selected
opt.add(Implies(specialized_selected, Or([selected[i] for i in standard_A])))
opt.add(Implies(specialized_selected, Or([selected[i] for i in standard_B])))
opt.add(Implies(specialized_selected, Or([selected[i] for i in standard_C])))

# ============================================================================
# 4. Define objective: minimize total cost = base_cost + redundancy_penalty
# ============================================================================

# Base cost: sum of costs of selected sets
base_cost = Sum([If(selected[i], set_costs[i], 0) for i in range(14)])

# Redundancy penalty: for each element covered by more than 3 sets, add penalty of 2
# We need to count, for each element, how many selected sets cover it
# Then, for elements with count > 3, add 2 to penalty

# We'll compute coverage count per element
coverage_count = [Int(f"coverage_count_{e}") for e in range(1, 21)]

for e in range(1, 21):
    sets_containing_e = [i for i in range(14) if e in set_elements[i]]
    # Count how many of those sets are selected
    count_expr = Sum([If(selected[i], 1, 0) for i in sets_containing_e])
    opt.add(coverage_count[e-1] == count_expr)

# Redundancy penalty: 2 for each element with coverage_count > 3
redundancy_penalty = 2 * Sum([If(coverage_count[e-1] > 3, 1, 0) for e in range(1, 21)])

# Total cost
total_cost = base_cost + redundancy_penalty

# Minimize total cost
opt.minimize(total_cost)

# ============================================================================
# 5. Check and print results
# ============================================================================

BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal solution found!")
    
    # Extract selected sets
    selected_sets = [i for i in range(14) if is_true(model[selected[i]])]
    print(f"selected_sets = {selected_sets}")
    
    # Total sets selected
    total_sets = len(selected_sets)
    print(f"total_sets = {total_sets}")
    
    # Covered elements (should be all 1-20)
    covered_elements = [e for e in range(1, 21) if is_true(model[covered[e-1]])]
    print(f"covered_elements = {covered_elements}")
    
    # Base cost
    base_cost_val = sum(set_costs[i] for i in selected_sets)
    print(f"base_cost = {base_cost_val}")
    
    # Redundancy penalty
    redundancy_penalty_val = sum(2 for e in range(1, 21) if model[coverage_count[e-1]].as_long() > 3)
    print(f"redundancy_penalty = {redundancy_penalty_val}")
    
    # Total cost
    total_cost_val = base_cost_val + redundancy_penalty_val
    print(f"total_cost = {total_cost_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")