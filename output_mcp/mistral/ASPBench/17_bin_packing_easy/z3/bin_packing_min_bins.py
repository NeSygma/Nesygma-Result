from z3 import *

# Item sizes
item_sizes = [4, 6, 2, 3, 7, 1, 5, 2, 4]
num_items = len(item_sizes)

# Bin capacity
bin_capacity = 10

# Maximum possible bins (theoretical upper bound)
max_bins = num_items  # Worst case: one item per bin

# Decision variables
# bin_assignment[i] = bin index (0-indexed) for item i
bin_assignment = [Int(f"bin_{i}") for i in range(num_items)]

# Total size in each bin (using Z3 Array to avoid symbolic indexing issues)
bin_total_size = Array('bin_total_size', IntSort(), IntSort())

# Number of bins used (0-indexed, so actual bins = num_bins_used + 1)
num_bins_used = Int("num_bins_used")

# Solver with optimization
opt = Optimize()

# Constraints

# 1. Each item is assigned to a bin
for i in range(num_items):
    opt.add(bin_assignment[i] >= 0)
    opt.add(bin_assignment[i] < max_bins)

# 2. Bin total sizes are correctly computed
# Initialize bin totals to 0 for all bins
for b in range(max_bins):
    opt.add(Select(bin_total_size, b) == 0)

# Add item sizes to their assigned bins
for i in range(num_items):
    b = bin_assignment[i]
    current_size = Select(bin_total_size, b)
    new_size = current_size + item_sizes[i]
    opt.add(Select(bin_total_size, b) == new_size)

# 3. No bin exceeds capacity
for b in range(max_bins):
    opt.add(Select(bin_total_size, b) <= bin_capacity)

# 4. Bins beyond num_bins_used must be empty
# If a bin index is >= num_bins_used, it must not contain any items
# This is implicitly handled by the assignment constraints and the fact that
# we minimize num_bins_used, but we can add an explicit constraint:
for i in range(num_items):
    opt.add(bin_assignment[i] < num_bins_used)

# 5. num_bins_used is the maximum bin index used + 1
# We can express this as: num_bins_used >= bin_assignment[i] + 1 for all i
for i in range(num_items):
    opt.add(num_bins_used >= bin_assignment[i] + 1)

# Objective: minimize the number of bins used
opt.minimize(num_bins_used)

# Check and print result
BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    print("Optimal number of bins:", model[num_bins_used])
    
    # Extract bin assignments
    bin_to_items = {}
    for i in range(num_items):
        b = model[bin_assignment[i]]
        if b in bin_to_items:
            bin_to_items[b].append(i + 1)  # Item IDs are 1-indexed
        else:
            bin_to_items[b] = [i + 1]
    
    # Print bin assignments
    for b in sorted(bin_to_items.keys()):
        items_in_bin = bin_to_items[b]
        total_size = sum(item_sizes[i-1] for i in items_in_bin)
        print(f"Bin {b+1}: items {items_in_bin}, total_size = {total_size}")
    
    print("feasible: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")