from z3 import *

# Item sizes (1-indexed for clarity)
item_sizes = [0, 4, 6, 2, 3, 7, 1, 5, 2, 4]  # Index 0 unused
num_items = 9

# Bin capacity
bin_capacity = 10

# Maximum possible bins (theoretical upper bound)
max_bins = num_items  # Worst case: one item per bin

# Decision variables
# bin_assignment[i] = bin index (0-indexed) for item i (1-indexed)
bin_assignment = [Int(f"bin_{i}") for i in range(1, num_items + 1)]

# Total size in each bin (Python list of Z3 Int)
bin_total_size = [Int(f"bin_total_{b}") for b in range(max_bins)]

# Number of bins used (0-indexed, so actual bins = num_bins_used + 1)
num_bins_used = Int("num_bins_used")

# Solver with optimization
opt = Optimize()

# Constraints

# 1. Each item is assigned to a bin
for i in range(1, num_items + 1):
    opt.add(bin_assignment[i - 1] >= 0)
    opt.add(bin_assignment[i - 1] < max_bins)

# 2. Bin total sizes are correctly computed
for b in range(max_bins):
    opt.add(bin_total_size[b] == Sum([
        If(bin_assignment[i - 1] == b, item_sizes[i], 0)
        for i in range(1, num_items + 1)
    ]))

# 3. No bin exceeds capacity
for b in range(max_bins):
    opt.add(bin_total_size[b] <= bin_capacity)

# 4. Bins beyond num_bins_used must be empty (i.e., no items assigned to them)
for b in range(max_bins):
    if b >= num_bins_used:
        for i in range(1, num_items + 1):
            opt.add(bin_assignment[i - 1] != b)

# 5. num_bins_used is the maximum bin index used + 1
# We can express this as: num_bins_used >= bin_assignment[i] + 1 for all i
for i in range(1, num_items + 1):
    opt.add(num_bins_used >= bin_assignment[i - 1] + 1)

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
    for i in range(1, num_items + 1):
        b = model[bin_assignment[i - 1]]
        if b in bin_to_items:
            bin_to_items[b].append(i)  # Item IDs are 1-indexed
        else:
            bin_to_items[b] = [i]
    
    # Print bin assignments
    for b in sorted(bin_to_items.keys()):
        items_in_bin = bin_to_items[b]
        total_size = sum(item_sizes[i] for i in items_in_bin)
        print(f"Bin {b+1}: items {items_in_bin}, total_size = {total_size}")
    
    print("feasible: True")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")