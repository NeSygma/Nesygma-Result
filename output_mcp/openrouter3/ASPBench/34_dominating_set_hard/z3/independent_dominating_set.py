from z3 import *

# Problem data
vertices = list(range(1, 19))  # 1-18
edges = [
    (1,2), (1,4), (1,5), (2,4), (2,5), (3,4), (3,9), (4,5), (4,18),
    (6,7), (6,9), (6,10), (7,9), (8,9), (8,14), (9,10), (11,12), (11,14),
    (12,14), (13,14), (13,17), (15,16), (15,17), (16,17), (17,18)
]

# Vertex types
critical = [1, 5, 10, 15]
standard = [2, 6, 7, 11, 12, 16]
resilient = [3, 8, 13, 18]

# Vertex costs
costs = {
    4: 2, 9: 2,
    14: 3, 17: 3,
    1: 5, 2: 5, 3: 5, 5: 5, 6: 5, 7: 5, 8: 5,
    10: 8, 11: 8, 12: 8, 13: 8, 15: 8, 16: 8, 18: 8
}

# Create adjacency list for easier lookup
adj = {v: [] for v in vertices}
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

# Create solver
solver = Solver()

# Binary variables: x[v] = 1 if vertex v is in dominating set
x = {v: Int(f'x_{v}') for v in vertices}
for v in vertices:
    solver.add(Or(x[v] == 0, x[v] == 1))

# Constraint 1: Independent set - no two adjacent vertices both in set
for u, v in edges:
    solver.add(Or(x[u] == 0, x[v] == 0))

# Constraint 5: All vertices must be dominated
# For each vertex v, either v is in the set, or it has enough neighbors in the set
for v in vertices:
    # Count neighbors in dominating set
    neighbor_count = Sum([x[u] for u in adj[v]])
    
    if v in critical:
        # Critical: must have at least 1 neighbor in set (if not in set)
        solver.add(Or(x[v] == 1, neighbor_count >= 1))
    elif v in standard:
        # Standard: must have at least 1 neighbor in set (if not in set)
        solver.add(Or(x[v] == 1, neighbor_count >= 1))
    elif v in resilient:
        # Resilient: must have at least 2 neighbors in set (if not in set)
        solver.add(Or(x[v] == 1, neighbor_count >= 2))

# Objective: minimize total cost
total_cost = Sum([costs[v] * x[v] for v in vertices])

# Use Optimize for minimization
opt = Optimize()
opt.add(solver.assertions())
opt.minimize(total_cost)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    dominating_set = sorted([v for v in vertices if model[x[v]] == 1])
    total_cost_value = sum(costs[v] for v in dominating_set)
    
    print("STATUS: sat")
    print(f"dominating_set: {dominating_set}")
    print(f"total_cost: {total_cost_value}")
    
    # Verify constraints
    print("\nVerification:")
    print(f"Independent set check: ", end="")
    independent = True
    for u, v in edges:
        if u in dominating_set and v in dominating_set:
            independent = False
            break
    print("PASS" if independent else "FAIL")
    
    print(f"All vertices dominated: ", end="")
    all_dominated = True
    for v in vertices:
        if v in dominating_set:
            continue
        neighbors_in_set = sum(1 for u in adj[v] if u in dominating_set)
        if v in critical or v in standard:
            if neighbors_in_set < 1:
                all_dominated = False
                break
        elif v in resilient:
            if neighbors_in_set < 2:
                all_dominated = False
                break
    print("PASS" if all_dominated else "FAIL")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")