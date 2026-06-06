from z3 import *

# Data
num_items = 27
sizes = [9,8,3,9,7,4,10,10,10,10,8,7,5,8,6,6,8,6,6,7,7,6,7,5,5,3,5]
# categories: 0=electronics,1=liquid,2=standard
cat_str = ['electronics','electronics','electronics','liquid','liquid','liquid','electronics','standard','liquid','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard','standard']
cat = [0 if c=='electronics' else 1 if c=='liquid' else 2 for c in cat_str]
# fragility: 0=fragile,1=sturdy
frag_str = ['fragile','sturdy','sturdy','fragile','sturdy','sturdy','fragile','sturdy','fragile','sturdy','sturdy','sturdy','sturdy','fragile','fragile','sturdy','fragile','fragile','sturdy','sturdy','sturdy','sturdy','sturdy','fragile','fragile','sturdy','sturdy']
frag = [0 if f=='fragile' else 1 for f in frag_str]
# priority: 0=high,1=low
prio_str = ['high','high','high','high','high','high','high','high','high','high','high','high','low','low','low','low','low','low','low','low','low','low','low','low','low','low','low']
prio = [0 if p=='high' else 1 for p in prio_str]

max_bins = 27  # enough bins

# Variables: bin assignment for each item (0-indexed)
bin_of = [Int(f'bin_{i}') for i in range(num_items)]
solver = Solver()
# domain constraints
for i in range(num_items):
    solver.add(bin_of[i] >= 0, bin_of[i] < max_bins)
    # priority constraint for high priority items
    if prio[i] == 0:  # high
        solver.add(bin_of[i] <= 5)  # bins 0..5 correspond to 1..6

# Capacity constraints per bin
for b in range(max_bins):
    total_size = Sum([If(bin_of[i] == b, sizes[i], 0) for i in range(num_items)])
    solver.add(total_size <= 20)
    # fragility limit
    fragile_cnt = Sum([If(And(bin_of[i] == b, frag[i] == 0), 1, 0) for i in range(num_items)])
    solver.add(fragile_cnt <= 2)
    # incompatibility electronics vs liquids
    ele_cnt = Sum([If(And(bin_of[i] == b, cat[i] == 0), 1, 0) for i in range(num_items)])
    liq_cnt = Sum([If(And(bin_of[i] == b, cat[i] == 1), 1, 0) for i in range(num_items)])
    # cannot have both >0
    solver.add(Or(ele_cnt == 0, liq_cnt == 0))

# Each item assigned exactly one bin already enforced by single variable

result = solver.check()
if result == sat:
    m = solver.model()
    print("STATUS: sat")
    # collect assignments
    assignments = [m.eval(bin_of[i]).as_long() + 1 for i in range(num_items)]  # 1-indexed bins
    for i, b in enumerate(assignments, start=1):
        print(f"Item {i} -> Bin {b}")
    # compute number of used bins
    used = set(assignments)
    print(f"num_bins = {len(used)}")
else:
    print("STATUS: unsat")