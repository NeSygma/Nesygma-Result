from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Create an optimizer for minimization
opt = Optimize()

# Vertices: 1 to 15
vertices = list(range(1, 16))

# Protected vertices (cannot be removed)
protected = {1, 15}

# Vertex costs (removal cost)
costs = {
    1: 10, 2: 4, 3: 5, 4: 6,
    5: 7, 6: 9, 7: 8,
    8: 2, 9: 4, 10: 3,
    11: 5, 12: 7, 13: 6,
    14: 6, 15: 12
}

# Vertex groups (at most one vertex from each group can be removed)
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

# Conditional edges (present only if source vertex is NOT removed)
conditional_edges = [
    ([3], [(3, 7), (3, 11)]),
    ([6], [(6, 10), (6, 13)]),
    ([9], [(9, 13), (9, 14)]),
    ([12], [(12, 4), (12, 7)])
]

# Decision variables: is_removed[v] is True if vertex v is removed
is_removed = {v: Bool(f"is_removed_{v}") for v in vertices}

# Topological order variables (only meaningful for non-removed vertices)
order = {v: Int(f"order_{v}") for v in vertices}

# Constraint: Protected vertices cannot be removed
for v in protected:
    opt.add(is_removed[v] == False)

# Constraint: Group constraints (at most one vertex per group can be removed)
for group, group_vertices in groups.items():
    # At most one vertex in group_vertices can be removed
    opt.add(Sum([If(is_removed[v], 1, 0) for v in group_vertices]) <= 1)

# Constraint: Topological order for non-removed vertices
# For each vertex, if it is not removed, its order is between 0 and (n-1)
for v in vertices:
    opt.add(If(is_removed[v], True, And(order[v] >= 0, order[v] < len(vertices))))

# Add constraints for core edges
for u, v in core_edges:
    # Edge (u,v) exists in the remaining graph only if u is not removed
    opt.add(Implies(Not(is_removed[u]), order[u] < order[v]))

# Add constraints for conditional edges
for sources, edges_list in conditional_edges:
    for u, v in edges_list:
        # Edge (u,v) exists in the remaining graph only if u is not removed
        opt.add(Implies(Not(is_removed[u]), order[u] < order[v]))

# Objective: Minimize the total removal cost
removal_costs = [If(is_removed[v], costs[v], 0) for v in vertices]
opt.minimize(Sum(removal_costs))

# Check if a solution exists
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract the feedback vertex set (removed vertices)
    feedback_set = sorted([v for v in vertices if is_true(model[is_removed[v]])])
    # Extract the costs for the feedback set
    feedback_costs = [costs[v] for v in feedback_set]
    # Extract the remaining vertices
    remaining_vertices = sorted([v for v in vertices if not is_true(model[is_removed[v]])])
    # Calculate total cost
    total_cost = sum(feedback_costs)
    
    print("STATUS: sat")
    print(f"feedback_set = {feedback_set}")
    print(f"costs = {feedback_costs}")
    print(f"total_cost = {total_cost}")
    print(f"remaining_vertices = {remaining_vertices}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")