from z3 import *

# Problem data
universe = list(range(1, 21))
# Sets: list of element lists
sets = [
    [1, 2, 3, 4, 5],          # 0
    [1, 6, 11, 16],           # 1
    [2, 7, 12, 17],           # 2
    [3, 8, 13, 18],           # 3
    [4, 9, 14, 19],           # 4
    [5, 10, 15, 20],          # 5
    [6, 7, 8, 9, 10],         # 6
    [1, 3, 5, 7, 9],          # 7
    [2, 4, 6, 8, 10],         # 8
    [1, 2, 3, 4, 5, 6, 7],    # 9 (specialized)
    [11, 12, 13, 14, 15],     # 10 (specialized)
    [8, 9, 10],               # 11 (specialized)
    [1, 5, 10, 15],           # 12 (specialized)
    [16, 17, 18, 19, 20]      # 13 (specialized)
]
# Costs
costs = [1]*9 + [4]*5
# Categories
# A: 0,1,2; B:3,4,5; C:6,7,8; specialized:9-13

# Solver
opt = Optimize()
# Selection booleans
sel = [Bool(f'sel_{i}') for i in range(len(sets))]
# Coverage counts
cov = [Int(f'cov_{e}') for e in universe]

# Coverage constraints
for idx, e in enumerate(universe):
    # Sum of selected sets that contain e
    covering_sets = [If(sel[i], 1, 0) for i, s in enumerate(sets) if e in s]
    opt.add(cov[idx] == Sum(covering_sets))
    # Full coverage
    opt.add(cov[idx] >= 1)

# Prerequisites
opt.add(Implies(sel[9], sel[0]))  # Set 9 requires Set 0
opt.add(Implies(sel[11], sel[6])) # Set 11 requires Set 6

# Mutual exclusion
opt.add(Not(And(sel[12], sel[13])))

# Category balancing
any_special = Or([sel[i] for i in range(9, 14)])
opt.add(Implies(any_special,
                And(Or(sel[0], sel[1], sel[2]),
                    Or(sel[3], sel[4], sel[5]),
                    Or(sel[6], sel[7], sel[8]))))

# Base cost
base_cost = Sum([If(sel[i], costs[i], 0) for i in range(len(sets))])
# Penalty: 2 per element covered by more than 3 sets
penalty = Sum([If(cov[idx] > 3, 2, 0) for idx in range(len(universe))])
# Total cost
total_cost = base_cost + penalty

# Objective: minimize total cost
opt.minimize(total_cost)

# Check
result = opt.check()
if result == sat:
    m = opt.model()
    selected_sets = [i for i in range(len(sets)) if is_true(m[sel[i]])]
    total_sets = len(selected_sets)
    # Compute values
    base_val = m.evaluate(base_cost, model_completion=True).as_long()
    penalty_val = m.evaluate(penalty, model_completion=True).as_long()
    total_val = m.evaluate(total_cost, model_completion=True).as_long()
    # Coverage elements (all 1-20 are covered by definition)
    covered_elements = list(universe)
    # Print results
    print("STATUS: sat")
    print("selected_sets:", selected_sets)
    print("total_sets:", total_sets)
    print("covered_elements:", covered_elements)
    print("base_cost:", base_val)
    print("redundancy_penalty:", penalty_val)
    print("total_cost:", total_val)
else:
    print("STATUS:", result)
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    else:
        print("STATUS: unknown")