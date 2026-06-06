from z3 import *

# Problem data
sizes = [4, 6, 2, 3, 7, 1, 5, 2, 4]  # item sizes
n = len(sizes)
capacity = 10
max_bins = 9  # upper bound on number of bins

solver = Optimize()

# Decision variables: bin_of_item[i] in 0..max_bins-1
bin_of_item = [Int(f'bin_{i}') for i in range(n)]

# Each item assigned to a bin (domain constraints)
for i in range(n):
    solver.add(bin_of_item[i] >= 0, bin_of_item[i] < max_bins)

# used[b] indicates whether bin b is used
used = [Bool(f'used_{b}') for b in range(max_bins)]

# Define used[b] as Or of assignments to that bin
for b in range(max_bins):
    solver.add(used[b] == Or([bin_of_item[i] == b for i in range(n)]))

# Capacity constraints
for b in range(max_bins):
    assigned_sizes = [If(bin_of_item[i] == b, sizes[i], 0) for i in range(n)]
    solver.add(Sum(assigned_sizes) <= capacity)

# Objective: minimize number of used bins
solver.minimize(Sum([used[b] for b in range(max_bins)]))

# Solve
if solver.check() == sat:
    model = solver.model()
    print("STATUS: sat")
    # Extract which bins are used
    used_bins = [b for b in range(max_bins) if is_true(model[used[b]])]
    print(f"num_bins = {len(used_bins)}")
    # Print item -> bin assignment
    for i in range(n):
        b = model[bin_of_item[i]].as_long()
        print(f"item {i+1} -> bin {b+1}")
    # Print bin details
    for b in used_bins:
        items_in_bin = [i+1 for i in range(n) if model[bin_of_item[i]].as_long() == b]
        total = sum(sizes[i] for i in range(n) if model[bin_of_item[i]].as_long() == b)
        print(f"bin {b+1}: items {items_in_bin}, total_size {total}")
else:
    print("STATUS: unsat")