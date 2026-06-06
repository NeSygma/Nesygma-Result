from z3 import *

# Item sizes
item_sizes = {
    1: 4,
    2: 6,
    3: 2,
    4: 3,
    5: 7,
    6: 1,
    7: 5,
    8: 2,
    9: 4
}

# Number of items
num_items = len(item_sizes)

# Maximum possible bins (theoretical upper bound)
max_bins = num_items

# Declare the number of bins as an integer variable to minimize
num_bins = Int('num_bins')

# Create a solver with optimization
opt = Optimize()

# Assign each item to a bin (bin indices start from 1)
# item_to_bin[i] = b means item i is assigned to bin b
item_to_bin = [Int(f'item_{i}_bin') for i in range(1, num_items + 1)]

# Each item must be assigned to a bin between 1 and num_bins
for i in range(num_items):
    opt.add(item_to_bin[i] >= 1, item_to_bin[i] <= num_bins)

# Ensure each item is assigned to exactly one bin
# (This is implicitly handled by the above constraints)

# For each bin, calculate the total size of items assigned to it
# We need to ensure that the total size does not exceed 10
# To do this, we will use a list of lists to represent bins and their items

# Create a list of bins, where each bin is a list of items assigned to it
# We will use a symbolic representation to enforce the capacity constraint

# For each bin b, the total size of items assigned to it must be <= 10
for b in range(1, max_bins + 1):
    # Create a list of items assigned to bin b
    items_in_bin = [
        item for item in range(1, num_items + 1) 
        if item_to_bin[item - 1] == b
    ]
    
    # Calculate the total size of items in bin b
    total_size = Sum([item_sizes[item] for item in items_in_bin])
    
    # Ensure the total size does not exceed 10
    opt.add(total_size <= 10)

# Minimize the number of bins
opt.minimize(num_bins)

# Ensure all items are assigned to a bin
# (This is already handled by the constraints above)

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Get the number of bins used
    num_bins_used = model[num_bins]
    
    # Build the bins structure
    bins = {}
    for b in range(1, num_bins_used.as_long() + 1):
        bins[b] = {
            'bin_id': b,
            'items': [],
            'total_size': 0
        }
    
    # Assign items to bins based on the model
    for item in range(1, num_items + 1):
        bin_id = model[item_to_bin[item - 1]].as_long()
        bins[bin_id]['items'].append(item)
        bins[bin_id]['total_size'] += item_sizes[item]
    
    print("STATUS: sat")
    print(f"num_bins: {num_bins_used}")
    print("bins:")
    for b in range(1, num_bins_used.as_long() + 1):
        print(f"  bin_id: {bins[b]['bin_id']}")
        print(f"    items: {bins[b]['items']}")
        print(f"    total_size: {bins[b]['total_size']}")
    print("feasible: True")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (no solution found)")
else:
    print("STATUS: unknown")