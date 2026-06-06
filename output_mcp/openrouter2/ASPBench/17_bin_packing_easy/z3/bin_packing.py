from z3 import *

# Problem data
sizes = [4,6,2,3,7,1,5,2,4]  # item sizes, index 0..8
n_items = len(sizes)
max_bins = n_items  # upper bound on bins

# Decision variables
bin_of_item = [Int(f'bin_of_item_{i}') for i in range(n_items)]
used_bin = [Bool(f'used_bin_{j}') for j in range(max_bins)]
bin_total = [Int(f'bin_total_{j}') for j in range(max_bins)]

solver = Optimize()

# Each item assigned to a bin index 0..max_bins-1
for i in range(n_items):
    solver.add(bin_of_item[i] >= 0, bin_of_item[i] < max_bins)

# Bin totals and capacity constraints
for j in range(max_bins):
    # total size in bin j
    solver.add(bin_total[j] == Sum([If(bin_of_item[i] == j, sizes[i], 0) for i in range(n_items)]))
    # capacity constraint
    solver.add(bin_total[j] <= 10)
    # used_bin flag
    solver.add(used_bin[j] == Or([bin_of_item[i] == j for i in range(n_items)]))

# Objective: minimize number of used bins
num_bins = Sum([If(used_bin[j], 1, 0) for j in range(max_bins)])
solver.minimize(num_bins)

# Solve
result = solver.check()

if result == sat:
    model = solver.model()
    # Compute used bins and assignments
    bins_info = []
    for j in range(max_bins):
        if is_true(model[used_bin[j]]):
            items_in_bin = [i+1 for i in range(n_items) if model[bin_of_item[i]] == j]
            total = sum(sizes[i] for i in range(n_items) if model[bin_of_item[i]] == j)
            bins_info.append({'bin_id': j+1, 'items': items_in_bin, 'total_size': total})
    # Sort bins by bin_id for consistency
    bins_info.sort(key=lambda x: x['bin_id'])
    # Number of bins used
    num_bins_used = len(bins_info)
    # Print results
    print("STATUS: sat")
    print(f"num_bins = {num_bins_used}")
    print("bins = [")
    for b in bins_info:
        print(f"  {{bin_id:{b['bin_id']}, items:{b['items']}, total_size:{b['total_size']}}},")
    print("]")
    print("feasible = True")
else:
    print("STATUS: unsat")
    print("feasible = False")