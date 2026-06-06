from z3 import *

# Problem Data
item_sizes = [4, 6, 2, 3, 7, 1, 5, 2, 4]
num_items = len(item_sizes)
max_bins = num_items  # Worst case: one item per bin

# Optimization Solver
opt = Optimize()

# Decision Variables
# x[i][j] = 1 if item i is in bin j, else 0
x = [[Int(f"x_{i}_{j}") for j in range(max_bins)] for i in range(num_items)]
# y[j] = 1 if bin j is used, else 0
y = [Int(f"y_{j}") for j in range(max_bins)]

# Constraints
# 1. Each item must be assigned to exactly one bin
for i in range(num_items):
    opt.add(Sum([x[i][j] for j in range(max_bins)]) == 1)
    for j in range(max_bins):
        opt.add(Or(x[i][j] == 0, x[i][j] == 1))

# 2. No bin can have a total size exceeding 10 units
# 3. Bin usage indicator
for j in range(max_bins):
    opt.add(Or(y[j] == 0, y[j] == 1))
    bin_total_size = Sum([x[i][j] * item_sizes[i] for i in range(num_items)])
    opt.add(bin_total_size <= 10 * y[j])

# Objective: Minimize the number of bins used
opt.minimize(Sum(y))

# Solve
result = opt.check()

if result == sat:
    model = opt.model()
    num_bins_used = model.evaluate(Sum(y)).as_long()
    print("STATUS: sat")
    print(f"num_bins: {num_bins_used}")
    
    bins_data = []
    for j in range(max_bins):
        if model.evaluate(y[j]).as_long() == 1:
            items_in_bin = [i + 1 for i in range(num_items) if model.evaluate(x[i][j]).as_long() == 1]
            total_size = sum([item_sizes[i-1] for i in items_in_bin])
            bins_data.append({
                "bin_id": len(bins_data) + 1,
                "items": items_in_bin,
                "total_size": total_size
            })
    
    for b in bins_data:
        print(f"Bin {b['bin_id']}: Items {b['items']}, Total Size: {b['total_size']}")
    print("feasible: True")
else:
    print("STATUS: unsat")
    print("feasible: False")