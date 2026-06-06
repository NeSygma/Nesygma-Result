from z3 import *

# Define problem data
universe = [1,2,3,4,5,6,7,8]
sets = [ {1,2,3}, {2,4,5}, {3,6,7}, {1,4,8}, {5,6,7,8}, {1,2,6} ]

n_sets = len(sets)

# Decision variables: whether each set is selected
sel = [Bool(f'sel_{i}') for i in range(n_sets)]

opt = Optimize()

# Constraint: each element must be covered by at least one selected set
for e in universe:
    opt.add(Or([sel[i] for i in range(n_sets) if e in sets[i]]))

# Objective: minimize number of selected sets
opt.minimize(Sum([If(sel[i],1,0) for i in range(n_sets)]))

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    selected = [i for i in range(n_sets) if is_true(m[sel[i]])]
    total_sets = len(selected)
    # Compute covered elements from selected sets
    covered = set()
    for i in selected:
        covered.update(sets[i])
    covered_list = sorted(list(covered))
    print("STATUS: sat")
    print("selected_sets =", selected)
    print("total_sets =", total_sets)
    print("covered_elements =", covered_list)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("UNKNOWN")