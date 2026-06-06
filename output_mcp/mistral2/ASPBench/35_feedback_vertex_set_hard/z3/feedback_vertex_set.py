from z3 import *

# BENCHMARK_MODE: ON (since the problem is guaranteed solvable)
BENCHMARK_MODE = True

# --- Problem Data ---
vertices = list(range(1, 16))
protected = {1, 15}
costs = {
    1: 10, 2: 4, 3: 5, 4: 6,
    5: 7, 6: 9, 7: 8,
    8: 2, 9: 4, 10: 3,
    11: 5, 12: 7, 13: 6,
    14: 6, 15: 12
}

# Groups: at most one vertex per group can be removed
groups = {
    'A': [2, 3, 4],
    'B': [5, 6, 7],
    'C': [8, 9, 10],
    'D': [11, 12, 13],
    'E': [14]
}

# Core edges (always present)
core_edges = [
    (1, 2), (1, 5), (1, 8),
    (2, 3), (3, 4), (4, 2),
    (5, 6), (6, 7), (7, 5),
    (8, 9), (9, 10), (10, 8),
    (11, 12), (12, 13), (13, 11),
    (2, 11), (4, 14), (7, 14), (10, 15),
    (14, 1)
]

# Conditional edges (present only if source is not removed)
conditional_edges = [
    ((3, 7), [3]), ((3, 11), [3]),
    ((6, 10), [6]), ((6, 13), [6]),
    ((9, 13), [9]), ((9, 14), [9]),
    ((12, 4), [12]), ((12, 7), [12])
]

# --- Z3 Model ---
opt = Optimize()

# 1. Decision variables
removed = [Bool(f'removed_{v}') for v in vertices]
order = [Int(f'order_{v}') for v in vertices]

# 2. Constraints

# Protection: 1 and 15 cannot be removed
opt.add(Not(removed[0]))  # vertex 1 (index 0)
opt.add(Not(removed[14]))  # vertex 15 (index 14)

# Group constraints: at most one vertex per group can be removed
for group in groups.values():
    # Use a loop to add AtMost constraints for each group
    group_bools = [removed[v-1] for v in group]
    opt.add(AtMost(*group_bools, 1))

# Core edges: for every core edge (u, v), if u is not removed, then order[u] < order[v]
for u, v in core_edges:
    u_idx = u - 1
    v_idx = v - 1
    opt.add(Implies(Not(removed[u_idx]), order[u_idx] < order[v_idx]))

# Conditional edges: for each conditional edge ((u, v), sources), the edge exists only if all sources are not removed
for (u, v), sources in conditional_edges:
    u_idx = u - 1
    v_idx = v - 1
    # The edge (u, v) exists only if all sources are not removed
    sources_not_removed = [Not(removed[s-1]) for s in sources]
    edge_exists = And(sources_not_removed)
    opt.add(Implies(edge_exists, order[u_idx] < order[v_idx]))

# Acyclicity: all vertices must have distinct orders (topological sort)
opt.add(Distinct(order))

# 3. Objective: minimize total removal cost
total_cost = Sum([If(removed[v-1], costs[v], 0) for v in vertices])
opt.minimize(total_cost)

# --- Check and Print ---
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract feedback vertex set
    feedback_set = [v for v in vertices if is_true(model[removed[v-1]])]
    feedback_set.sort()
    # Extract costs
    costs_list = [costs[v] for v in feedback_set]
    # Total cost
    total_cost_val = sum(costs_list)
    # Remaining vertices
    remaining_vertices = [v for v in vertices if v not in feedback_set]
    remaining_vertices.sort()
    # Print results
    print("STATUS: sat")
    print(f"feedback_set = {feedback_set}")
    print(f"costs = {costs_list}")
    print(f"total_cost = {total_cost_val}")
    print(f"remaining_vertices = {remaining_vertices}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")