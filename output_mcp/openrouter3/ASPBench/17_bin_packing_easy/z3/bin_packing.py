from z3 import *

# Problem data
item_sizes = [4, 6, 2, 3, 7, 1, 5, 2, 4]
num_items = len(item_sizes)
bin_capacity = 10

# We'll try with up to 9 bins (worst case: each item in its own bin)
# But we expect optimal to be 4 bins
max_bins = 9

# Create solver
opt = Optimize()

# Decision variables: bin_assignment[i] = bin number (1-indexed) for item i
bin_assignment = [Int(f'bin_{i}') for i in range(num_items)]

# Add constraints for each item
for i in range(num_items):
    # Each item must be assigned to a bin between 1 and max_bins
    opt.add(bin_assignment[i] >= 1)
    opt.add(bin_assignment[i] <= max_bins)

# For each bin, we need to ensure total size doesn't exceed capacity
# We'll create a helper function to sum sizes for items in a specific bin
for b in range(1, max_bins + 1):
    # Sum of sizes of items assigned to bin b
    bin_sum = Sum([If(bin_assignment[i] == b, item_sizes[i], 0) for i in range(num_items)])
    # Bin capacity constraint
    opt.add(bin_sum <= bin_capacity)

# Minimize the number of bins used
# The number of bins used is the maximum bin number assigned to any item
num_bins_used = Int('num_bins_used')
opt.add(num_bins_used == Max(bin_assignment))
opt.minimize(num_bins_used)

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    num_bins = model[num_bins_used].as_long()
    print(f"Number of bins used: {num_bins}")
    
    # Group items by bin
    bins = {}
    for i in range(num_items):
        bin_num = model[bin_assignment[i]].as_long()
        if bin_num not in bins:
            bins[bin_num] = []
        bins[bin_num].append(i + 1)  # Item IDs are 1-indexed
    
    # Print bin assignments
    print("\nBin assignments:")
    for bin_num in sorted(bins.keys()):
        items_in_bin = bins[bin_num]
        total_size = sum(item_sizes[i-1] for i in items_in_bin)
        print(f"Bin {bin_num}: Items {items_in_bin}, Total size: {total_size}")
    
    # Print in required format
    print(f"\nnum_bins: {num_bins}")
    print("feasible: True")
    
    # Verify solution
    print("\nVerification:")
    for bin_num in sorted(bins.keys()):
        items_in_bin = bins[bin_num]
        total_size = sum(item_sizes[i-1] for i in items_in_bin)
        print(f"Bin {bin_num}: {total_size} units (capacity: {bin_capacity})")
        if total_size > bin_capacity:
            print("ERROR: Bin exceeds capacity!")
            break
    else:
        print("All bins within capacity ✓")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found with the given constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")