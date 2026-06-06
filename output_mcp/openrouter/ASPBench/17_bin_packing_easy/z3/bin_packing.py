from z3 import *

# Data
sizes = [4,6,2,3,7,1,5,2,4]  # items 1..9
n_items = len(sizes)
max_bins = n_items  # upper bound

# Variables
assign = [Int(f'assign_{i}') for i in range(n_items)]  # bin index for each item (1..max_bins)
used = [Bool(f'used_{j}') for j in range(max_bins)]  # whether bin j+1 is used

opt = Optimize()

# Constraints: each assign in 1..max_bins
for a in assign:
    opt.add(a >= 1, a <= max_bins)

# Link used flags: used_j iff some item assigned to j+1
for j in range(max_bins):
    # used_j => exists i with assign_i == j+1
    # and converse: if any assign_i == j+1 then used_j
    # Use Or of equalities
    eqs = [assign[i] == j+1 for i in range(n_items)]
    opt.add(used[j] == Or(eqs))

# Capacity constraints for each bin
for j in range(max_bins):
    total = Sum([If(assign[i] == j+1, sizes[i], 0) for i in range(n_items)])
    opt.add(total <= 10)

# Objective: minimize number of used bins
num_bins = Sum([If(used[j], 1, 0) for j in range(max_bins)])
opt.minimize(num_bins)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    # Extract assignments
    assignments = [m.eval(assign[i]).as_long() for i in range(n_items)]
    # Compute used bins and totals
    bin_totals = {}
    for i, b in enumerate(assignments):
        bin_totals.setdefault(b, 0)
        bin_totals[b] += sizes[i]
    used_bins = sorted(bin_totals.keys())
    num_used = len(used_bins)
    print("STATUS: sat")
    print(f"num_bins = {num_used}")
    for i, b in enumerate(assignments):
        print(f"item_{i+1} = {b}")
    for b in used_bins:
        print(f"bin_{b}_total = {bin_totals[b]}")
else:
    print("STATUS: unsat")