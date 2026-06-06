from z3 import *

# ============================================================
# DATA
# ============================================================
items_data = [
    (1, 9, "electronics", "fragile", "high"),
    (2, 8, "electronics", "sturdy", "high"),
    (3, 3, "electronics", "sturdy", "high"),
    (4, 9, "liquid", "fragile", "high"),
    (5, 7, "liquid", "sturdy", "high"),
    (6, 4, "liquid", "sturdy", "high"),
    (7, 10, "electronics", "fragile", "high"),
    (8, 10, "standard", "sturdy", "high"),
    (9, 10, "liquid", "fragile", "high"),
    (10, 10, "standard", "sturdy", "high"),
    (11, 8, "standard", "sturdy", "high"),
    (12, 7, "standard", "sturdy", "high"),
    (13, 5, "standard", "sturdy", "low"),
    (14, 8, "standard", "fragile", "low"),
    (15, 6, "standard", "fragile", "low"),
    (16, 6, "standard", "sturdy", "low"),
    (17, 8, "standard", "fragile", "low"),
    (18, 6, "standard", "fragile", "low"),
    (19, 6, "standard", "sturdy", "low"),
    (20, 7, "standard", "sturdy", "low"),
    (21, 7, "standard", "sturdy", "low"),
    (22, 6, "standard", "sturdy", "low"),
    (23, 7, "standard", "sturdy", "low"),
    (24, 5, "standard", "fragile", "low"),
    (25, 5, "standard", "fragile", "low"),
    (26, 3, "standard", "sturdy", "low"),
    (27, 5, "standard", "sturdy", "low"),
]

N = 27  # items
MAX_BINS = 27  # upper bound: at most one item per bin
BIN_CAPACITY = 20
MAX_FRAGILE_PER_BIN = 2
PRIORITY_BINS = list(range(1, 7))  # bins 1-6

# Precompute item properties
item_sizes = [d[1] for d in items_data]
item_categories = [d[2] for d in items_data]
item_fragile = [d[3] == "fragile" for d in items_data]
item_priority = [d[4] == "high" for d in items_data]

# ============================================================
# DECISION VARIABLES
# ============================================================
# bin_for_item[i] = bin number (1..MAX_BINS) assigned to item i
bin_for_item = [Int(f"bin_{i+1}") for i in range(N)]

solver = Solver()

# Domain: each item assigned to a bin from 1 to MAX_BINS
for i in range(N):
    solver.add(bin_for_item[i] >= 1, bin_for_item[i] <= MAX_BINS)

# ============================================================
# CONSTRAINT 1: Capacity - total size in each bin <= 20
# ============================================================
for b in range(1, MAX_BINS + 1):
    total_size = Sum([If(bin_for_item[i] == b, item_sizes[i], 0) for i in range(N)])
    solver.add(total_size <= BIN_CAPACITY)

# ============================================================
# CONSTRAINT 2: Assignment - each item to exactly one bin (already enforced by domain)
# ============================================================

# ============================================================
# CONSTRAINT 3: Incompatibility - electronics and liquids cannot share a bin
# ============================================================
electronics_items = [i for i in range(N) if item_categories[i] == "electronics"]
liquid_items = [i for i in range(N) if item_categories[i] == "liquid"]

for b in range(1, MAX_BINS + 1):
    has_electronics = Or([bin_for_item[i] == b for i in electronics_items])
    has_liquid = Or([bin_for_item[i] == b for i in liquid_items])
    # Not both in the same bin
    solver.add(Not(And(has_electronics, has_liquid)))

# ============================================================
# CONSTRAINT 4: Fragility Limit - no more than 2 fragile items per bin
# ============================================================
fragile_items = [i for i in range(N) if item_fragile[i]]

for b in range(1, MAX_BINS + 1):
    fragile_count = Sum([If(bin_for_item[i] == b, 1, 0) for i in fragile_items])
    solver.add(fragile_count <= MAX_FRAGILE_PER_BIN)

# ============================================================
# CONSTRAINT 5: Priority Placement - high-priority items only in bins 1-6
# ============================================================
high_priority_items = [i for i in range(N) if item_priority[i]]

for i in high_priority_items:
    # bin_for_item[i] must be in {1,2,3,4,5,6}
    solver.add(Or([bin_for_item[i] == b for b in PRIORITY_BINS]))

# ============================================================
# SOLVE
# ============================================================
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    
    # Extract assignment
    assignment = {}
    for i in range(N):
        assignment[i] = m.eval(bin_for_item[i]).as_long()
    
    # Build bins
    bins_used = set(assignment.values())
    num_bins = len(bins_used)
    
    # Compute per-bin stats
    bin_items = {b: [] for b in bins_used}
    for i in range(N):
        b = assignment[i]
        bin_items[b].append(i)
    
    # Total priority utilization: sum of sizes in bins containing at least one high-priority item
    total_priority_utilization = 0
    for b in sorted(bins_used):
        items_in_bin = bin_items[b]
        total_size = sum(item_sizes[i] for i in items_in_bin)
        fragile_count = sum(1 for i in items_in_bin if item_fragile[i])
        has_priority = any(item_priority[i] for i in items_in_bin)
        if has_priority:
            total_priority_utilization += total_size
    
    print("STATUS: sat")
    print(f"feasible: true")
    print(f"optimal: false")
    print(f"num_bins: {num_bins}")
    print(f"total_priority_utilization: {total_priority_utilization}")
    print(f"bins:")
    for b in sorted(bins_used):
        items_in_bin = bin_items[b]
        total_size = sum(item_sizes[i] for i in items_in_bin)
        fragile_count = sum(1 for i in items_in_bin if item_fragile[i])
        has_priority = any(item_priority[i] for i in items_in_bin)
        print(f"  bin_id: {b}")
        print(f"    items: {[items_data[i][0] for i in items_in_bin]}")
        print(f"    total_size: {total_size}")
        print(f"    fragile_count: {fragile_count}")
        print(f"    is_priority_bin: {has_priority}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")