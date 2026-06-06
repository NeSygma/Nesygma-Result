from z3 import *

# Problem data
vertices = list(range(1, 16))
protected = {1, 15}
costs = {
    1: 10, 2: 4, 3: 5, 4: 6,
    5: 7, 6: 9, 7: 8,
    8: 2, 9: 4, 10: 3,
    11: 5, 12: 7, 13: 6,
    14: 6, 15: 12
}

# Groups
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

# Conditional edges (present only if source remains)
conditional_edges = [
    (3, 7), (3, 11),  # if 3 remains
    (6, 10), (6, 13),  # if 6 remains
    (9, 13), (9, 14),  # if 9 remains
    (12, 4), (12, 7)   # if 12 remains
]

# Create solver
solver = Solver()

# Decision variables: removed[v] = True if vertex v is removed
removed = {v: Bool(f'removed_{v}') for v in vertices}

# 1. Protection constraint: vertices 1 and 15 cannot be removed
for v in protected:
    solver.add(Not(removed[v]))

# 2. Group constraint: at most one vertex per group can be removed
for group_name, group_vertices in groups.items():
    # At most one removed in this group
    solver.add(Sum([If(removed[v], 1, 0) for v in group_vertices]) <= 1)

# 3. Acyclicity constraint: No directed cycles in remaining graph
# We'll use a topological ordering approach: assign each vertex a "rank"
# If there's an edge u->v and both remain, then rank[u] < rank[v]
ranks = {v: Int(f'rank_{v}') for v in vertices}

# For each possible edge (core or conditional), if both endpoints remain, enforce rank ordering
for u, v in core_edges:
    # Edge exists if u is not removed
    solver.add(Implies(Not(removed[u]), 
                       Implies(Not(removed[v]), ranks[u] < ranks[v])))

# For conditional edges: edge exists only if source remains
for u, v in conditional_edges:
    solver.add(Implies(Not(removed[u]), 
                       Implies(Not(removed[v]), ranks[u] < ranks[v])))

# 4. Objective: minimize total removal cost
total_cost = Sum([If(removed[v], costs[v], 0) for v in vertices])

# We'll use an optimization approach: try to find minimum cost
# Since Z3's optimization is limited, we'll iterate over possible costs
# Start with lower bound and increase until we find a solution

# Lower bound: at least one vertex from each cycle must be removed
# But we have group constraints, so we need to be careful

# Let's try to find a solution with cost <= 18 (expected minimum)
# We'll use a soft constraint approach with optimization

# Create an Optimize object for better handling
opt = Optimize()

# Add all constraints to the optimizer
for v in protected:
    opt.add(Not(removed[v]))

for group_name, group_vertices in groups.items():
    opt.add(Sum([If(removed[v], 1, 0) for v in group_vertices]) <= 1)

for u, v in core_edges:
    opt.add(Implies(Not(removed[u]), 
                    Implies(Not(removed[v]), ranks[u] < ranks[v])))

for u, v in conditional_edges:
    opt.add(Implies(Not(removed[u]), 
                    Implies(Not(removed[v]), ranks[u] < ranks[v])))

# Minimize total cost
h = opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract solution
    feedback_set = []
    costs_list = []
    remaining_vertices = []
    
    for v in vertices:
        if model[removed[v]]:
            feedback_set.append(v)
            costs_list.append(costs[v])
        else:
            remaining_vertices.append(v)
    
    total_cost_value = sum(costs_list)
    
    print(f"feedback_set: {sorted(feedback_set)}")
    print(f"costs: {costs_list}")
    print(f"total_cost: {total_cost_value}")
    print(f"remaining_vertices: {sorted(remaining_vertices)}")
    
    # Verify acyclicity
    print("\nVerifying acyclicity...")
    # Check if there are any cycles in the remaining graph
    # We can do this by checking if the rank ordering is consistent
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")