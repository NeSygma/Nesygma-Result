from z3 import *

# Problem data
items = [
    # (id, size, category, fragility, priority)
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

# Constants
BIN_CAPACITY = 20
FRAGILE_LIMIT = 2
PRIORITY_BINS_START = 1  # bins 1-6 (1-indexed)
PRIORITY_BINS_END = 6

# Determine number of bins needed - estimate
total_size = sum(item[1] for item in items)
print(f"Total size: {total_size}")
min_bins_needed = (total_size + BIN_CAPACITY - 1) // BIN_CAPACITY
print(f"Minimum bins needed: {min_bins_needed}")

# We'll use 15 bins to be safe (0-indexed: 0-14)
NUM_BINS = 15

# Create solver
solver = Solver()

# Variables
# assignment[i] = bin index (0-14) for item i (0-indexed)
assignment = [Int(f"assign_{i}") for i in range(len(items))]

# bin_used[j] = True if bin j is used
bin_used = [Bool(f"bin_used_{j}") for j in range(NUM_BINS)]

# Fragile count per bin (we'll use integer variable)
bin_fragile_count = [Int(f"bin_fragile_{j}") for j in range(NUM_BINS)]

# Total size per bin
bin_total_size = [Int(f"bin_size_{j}") for j in range(NUM_BINS)]

# Priority bin indicator (bins 1-6 are priority bins, 1-indexed)
# In 0-indexed: bins 0-5 are priority bins
is_priority_bin = [Bool(f"is_priority_{j}") for j in range(NUM_BINS)]
for j in range(NUM_BINS):
    if j < 6:  # bins 0-5 correspond to bins 1-6
        solver.add(is_priority_bin[j] == True)
    else:
        solver.add(is_priority_bin[j] == False)

# 1. Assignment constraint: each item assigned to exactly one bin
for i in range(len(items)):
    solver.add(assignment[i] >= 0)
    solver.add(assignment[i] < NUM_BINS)

# 2. Capacity constraint: total size per bin <= 20
for j in range(NUM_BINS):
    # Calculate total size for bin j
    sizes_for_bin = []
    for i in range(len(items)):
        item_size = items[i][1]
        # Use If to add size only if item assigned to this bin
        sizes_for_bin.append(If(assignment[i] == j, item_size, 0))
    solver.add(bin_total_size[j] == Sum(sizes_for_bin))
    solver.add(Implies(bin_used[j], bin_total_size[j] <= BIN_CAPACITY))

# 3. Incompatibility: electronics and liquids cannot be in same bin
for j in range(NUM_BINS):
    # For each bin, we need to ensure that if there is any electronics, there is no liquid, and vice versa.
    # We'll create two Boolean variables indicating presence of electronics and liquids in the bin.
    has_elec = Bool(f"has_elec_{j}")
    has_liq = Bool(f"has_liq_{j}")
    
    # Determine if bin has electronics or liquids
    elec_conditions = []
    liq_conditions = []
    for i in range(len(items)):
        category = items[i][2]
        if category == "electronics":
            elec_conditions.append(assignment[i] == j)
        elif category == "liquid":
            liq_conditions.append(assignment[i] == j)
    
    # has_elec is true if at least one electronics item is assigned to this bin
    if elec_conditions:
        solver.add(has_elec == Or(elec_conditions))
    else:
        solver.add(has_elec == False)
    
    # has_liq is true if at least one liquid item is assigned to this bin
    if liq_conditions:
        solver.add(has_liq == Or(liq_conditions))
    else:
        solver.add(has_liq == False)
    
    # Constraint: cannot have both electronics and liquids
    solver.add(Not(And(has_elec, has_liq)))

# 4. Fragility limit: no more than 2 fragile items per bin
for j in range(NUM_BINS):
    fragile_count = []
    for i in range(len(items)):
        fragility = items[i][3]
        if fragility == "fragile":
            fragile_count.append(If(assignment[i] == j, 1, 0))
    solver.add(bin_fragile_count[j] == Sum(fragile_count))
    solver.add(Implies(bin_used[j], bin_fragile_count[j] <= FRAGILE_LIMIT))

# 5. Priority placement: high-priority items only in bins 1-6 (0-indexed: 0-5)
for i in range(len(items)):
    priority = items[i][4]
    if priority == "high":
        solver.add(assignment[i] < 6)  # bins 0-5

# 6. Bin usage: a bin is used if at least one item assigned to it
for j in range(NUM_BINS):
    assigned_to_bin = [assignment[i] == j for i in range(len(items))]
    solver.add(bin_used[j] == Or(assigned_to_bin))

# 7. All items must be assigned (already covered by assignment constraints)

# 8. Optional: minimize number of bins (soft constraint)
# We'll add a soft constraint to minimize the number of bins used
# But first find any feasible solution

print("Solving...")
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract solution
    assignment_values = [model[assignment[i]].as_long() for i in range(len(items))]
    bin_used_values = [model[bin_used[j]] for j in range(NUM_BINS)]
    
    # Count used bins
    num_bins_used = sum(1 for used in bin_used_values if used)
    
    # Calculate total priority utilization
    total_priority_utilization = 0
    for i in range(len(items)):
        if items[i][4] == "high":
            bin_idx = assignment_values[i]
            if bin_idx < 6:  # priority bin
                total_priority_utilization += items[i][1]
    
    # Build bins array
    bins = []
    for j in range(NUM_BINS):
        if bin_used_values[j]:
            bin_items = []
            for i in range(len(items)):
                if assignment_values[i] == j:
                    item_data = {
                        "id": items[i][0],
                        "size": items[i][1],
                        "category": items[i][2],
                        "fragility": items[i][3],
                        "priority": items[i][4]
                    }
                    bin_items.append(item_data)
            
            # Calculate bin stats
            total_size_bin = sum(item["size"] for item in bin_items)
            fragile_count_bin = sum(1 for item in bin_items if item["fragility"] == "fragile")
            is_priority = any(item["priority"] == "high" for item in bin_items)
            
            bins.append({
                "bin_id": j + 1,  # 1-indexed
                "items": bin_items,
                "total_size": total_size_bin,
                "fragile_count": fragile_count_bin,
                "is_priority_bin": is_priority
            })
    
    # Print results in required format
    print(f"feasible: True")
    print(f"optimal: False")
    print(f"num_bins: {num_bins_used}")
    print(f"total_priority_utilization: {total_priority_utilization}")
    print("bins:")
    for bin_data in bins:
        print(f"  - bin_id: {bin_data['bin_id']}")
        print(f"    items: {bin_data['items']}")
        print(f"    total_size: {bin_data['total_size']}")
        print(f"    fragile_count: {bin_data['fragile_count']}")
        print(f"    is_priority_bin: {bin_data['is_priority_bin']}")
    
    # Additional verification: check constraints
    print("\nVerification:")
    # Check capacity
    for bin_data in bins:
        if bin_data["total_size"] > BIN_CAPACITY:
            print(f"ERROR: Bin {bin_data['bin_id']} exceeds capacity")
        if bin_data["fragile_count"] > FRAGILE_LIMIT:
            print(f"ERROR: Bin {bin_data['bin_id']} has too many fragile items")
        # Check incompatibility
        categories = set(item["category"] for item in bin_data["items"])
        if "electronics" in categories and "liquid" in categories:
            print(f"ERROR: Bin {bin_data['bin_id']} has both electronics and liquids")
        # Check priority placement
        for item in bin_data["items"]:
            if item["priority"] == "high" and bin_data["bin_id"] > 6:
                print(f"ERROR: High-priority item {item['id']} in non-priority bin {bin_data['bin_id']}")
    print("Verification complete.")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")