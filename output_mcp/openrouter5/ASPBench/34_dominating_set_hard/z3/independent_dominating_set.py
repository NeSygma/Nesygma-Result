from z3 import *

# Graph: 18 vertices (1-18)
N = 18

# Edges (undirected)
edges = [
    (1,2), (1,4), (1,5), (2,4), (2,5), (3,4), (3,9), (4,5), (4,18),
    (6,7), (6,9), (6,10), (7,9), (8,9), (8,14), (9,10), (11,12), (11,14),
    (12,14), (13,14), (13,17), (15,16), (15,17), (16,17), (17,18)
]

# Build adjacency list (1-indexed)
adj = [[] for _ in range(N+1)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

# Vertex types
critical = {1, 5, 10, 15}
standard = {2, 6, 7, 11, 12, 16}
resilient = {3, 8, 13, 18}

# Vertex costs
cost = [0] * (N+1)
for v in [4, 9]:
    cost[v] = 2
for v in [14, 17]:
    cost[v] = 3
for v in [1, 2, 3, 5, 6, 7, 8]:
    cost[v] = 5
for v in [10, 11, 12, 13, 15, 16, 18]:
    cost[v] = 8

# Decision variables: x[v] = 1 if vertex v is in the dominating set, else 0
x = [Int(f'x_{v}') for v in range(N+1)]

opt = Optimize()

# Domain: binary
for v in range(1, N+1):
    opt.add(Or(x[v] == 0, x[v] == 1))

# Constraint 1: Independent set - no two adjacent vertices both selected
for u, v in edges:
    opt.add(Not(And(x[u] == 1, x[v] == 1)))

# Constraints 2-5: Domination requirements
for v in range(1, N+1):
    # Count how many neighbors are in the dominating set
    neighbor_count = Sum([x[u] for u in adj[v]])
    
    if v in critical:
        # Critical: must be adjacent to at least 1 dominating vertex if not in set
        opt.add(Or(x[v] == 1, neighbor_count >= 1))
    elif v in standard:
        # Standard: must be adjacent to at least 1 dominating vertex if not in set
        opt.add(Or(x[v] == 1, neighbor_count >= 1))
    elif v in resilient:
        # Resilient: must be adjacent to at least 2 dominating vertices if not in set
        opt.add(Or(x[v] == 1, neighbor_count >= 2))
    else:
        # Other vertices (4, 9, 14, 17) - no special type, but still need to be dominated
        # They must be in the set or adjacent to at least 1 dominating vertex
        opt.add(Or(x[v] == 1, neighbor_count >= 1))

# Objective: minimize total cost
total_cost = Sum([cost[v] * x[v] for v in range(1, N+1)])
opt.minimize(total_cost)

result = opt.check()

if result == sat:
    m = opt.model()
    dom_set = [v for v in range(1, N+1) if m.eval(x[v]) == 1]
    tc = sum(cost[v] for v in dom_set)
    print("STATUS: sat")
    print(f"dominating_set = {sorted(dom_set)}")
    print(f"total_cost = {tc}")
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")