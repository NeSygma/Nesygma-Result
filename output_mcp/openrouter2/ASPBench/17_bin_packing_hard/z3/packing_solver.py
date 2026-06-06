from z3 import *

# Problem data
num_items = 27
max_bins = 10  # upper bound on number of bins

# Item properties
sizes = [9,8,3,9,7,4,10,10,10,10,8,7,5,8,6,6,8,6,6,7,7,6,7,5,5,3,5]
# category: 0 electronics, 1 liquid, 2 standard
categories = [0,0,0,1,1,1,0,2,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
fragile = [True,False,False,True,False,False,True,False,True,False,False,False,False,True,True,False,True,True,False,False,False,False,False,True,True,False,False]
# priority: True high, False low
priority = [True]*12 + [False]*15

# Z3 variables
assign = [Int(f'assign_{i}') for i in range(num_items)]

solver = Solver()

# Assignment bounds
for i in range(num_items):
    solver.add(assign[i] >= 0, assign[i] < max_bins)

# High priority items must be in bins 0-5 (1-6 in 1-indexed)
for i in range(num_items):
    if priority[i]:
        solver.add(assign[i] <= 5)

# Capacity constraints per bin
for b in range(max_bins):
    bin_size = Sum([If(assign[i] == b, sizes[i], 0) for i in range(num_items)])
    solver.add(bin_size <= 20)

# Fragility limit per bin
for b in range(max_bins):
    fragile_count = Sum([If(And(assign[i] == b, fragile[i]), 1, 0) for i in range(num_items)])
    solver.add(fragile_count <= 2)

# Incompatibility: electronics and liquids cannot share a bin
electronics_indices = [i for i, cat in enumerate(categories) if cat == 0]
liquid_indices = [i for i, cat in enumerate(categories) if cat == 1]
for b in range(max_bins):
    for e in electronics_indices:
        for l in liquid_indices:
            solver.add(Or(assign[e] != b, assign[l] != b))

# Check satisfiability
result = solver.check()
if result == sat:
    model = solver.model()
    # Compute used bins
    used_bins = []
    for b in range(max_bins):
        if any(model.eval(assign[i]) == b for i in range(num_items)):
            used_bins.append(b)
    num_bins_used = len(used_bins)
    # Compute total priority utilization
    total_priority_utilization = 0
    bins_output = []
    for b in used_bins:
        bin_items = []
        bin_size = 0
        fragile_count = 0
        has_high = False
        for i in range(num_items):
            if model.eval(assign[i]) == b:
                bin_items.append(i)
                bin_size += sizes[i]
                if fragile[i]:
                    fragile_count += 1
                if priority[i]:
                    has_high = True
        if has_high:
            total_priority_utilization += bin_size
        # Build item objects
        item_objs = []
        for i in bin_items:
            item_objs.append({
                'item_id': i+1,
                'size': sizes[i],
                'category': ['electronics','liquid','standard'][categories[i]],
                'fragility': 'fragile' if fragile[i] else 'sturdy',
                'priority': 'high' if priority[i] else 'low'
            })
        bins_output.append({
            'bin_id': b+1,
            'items': item_objs,
            'total_size': bin_size,
            'fragile_count': fragile_count,
            'is_priority_bin': has_high
        })
    # Output
    print("STATUS: sat")
    print("feasible = True")
    print("optimal = False")
    print(f"num_bins = {num_bins_used}")
    print(f"total_priority_utilization = {total_priority_utilization}")
    print("bins = [")
    for bin_dict in bins_output:
        print("  {")
        print(f"    bin_id: {bin_dict['bin_id']},")
        print("    items: [")
        for item in bin_dict['items']:
            print(f"      {{item_id: {item['item_id']}, size: {item['size']}, category: {item['category']}, fragility: {item['fragility']}, priority: {item['priority']}}},")
        print("    ],")
        print(f"    total_size: {bin_dict['total_size']},")
        print(f"    fragile_count: {bin_dict['fragile_count']},")
        print(f"    is_priority_bin: {bin_dict['is_priority_bin']}")
        print("  },")
    print("]")
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")