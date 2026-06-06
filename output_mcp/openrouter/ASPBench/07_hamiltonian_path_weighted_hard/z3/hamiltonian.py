from z3 import *
import json, sys

N = 100
# Build edge set with weights
edges = {}
# 1. Chain edges weight 1
for i in range(N-1):
    edges[(i, i+1)] = 1
# 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
for Nidx in range(24):
    B = 2 + 4*Nidx
    if B+3 < N:
        edges[(B, B+2)] = 3
        edges[(B+2, B+1)] = 3
        edges[(B+1, B+3)] = 3
# 3. Skips of length 2 at multiples of 4 (weight 4)
for Nidx in range(25):
    S = 4*Nidx
    if S+2 < N:
        edges[(S, S+2)] = 4
# 4. Jumps of length 3 for vertices ≡1 (mod 4) (weight 5)
for Nidx in range(24):
    T = 1 + 4*Nidx
    if T+3 < N:
        edges[(T, T+3)] = 5
# 5. Long bridges of length 4 at multiples of 5 (weight 6)
for K in range(20):
    U = 5*K
    if U+4 < N:
        edges[(U, U+4)] = 6
# Forbidden edges removal
forbidden = set()
# Base forbids
forbidden.update({(0,2), (1,3)})
# Periodic forbids
for Nidx in range(12):
    F = 2 + 8*Nidx
    if F+2 < N:
        forbidden.add((F, F+2))
for Nidx in range(13):
    G = 8*Nidx
    if G+2 < N:
        forbidden.add((G, G+2))
for Nidx in range(12):
    H = 1 + 8*Nidx
    if H+3 < N:
        forbidden.add((H, H+3))
for M in range(10):
    L = 10*M + 5
    if L+4 < N:
        forbidden.add((L, L+4))
# Remove forbidden from edges
for e in list(edges.keys()):
    if e in forbidden:
        del edges[e]

# Declare position variables
pos = [Int(f'p_{i}') for i in range(N)]
solver = Optimize()
# Domain and distinct
for v in range(N):
    solver.add(pos[v] >= 0, pos[v] < N)
solver.add(Distinct(pos))
# Start and end positions
solver.add(pos[0] == 0)
solver.add(pos[99] == N-1)
# Edge existence constraints: if consecutive positions then edge must exist
# For all pairs not in edges, forbid adjacency
edge_set = set(edges.keys())
for u in range(N):
    for v in range(N):
        if u == v:
            continue
        if (u, v) not in edge_set:
            # forbid pos[u] + 1 == pos[v]
            solver.add(Not(pos[u] + 1 == pos[v]))
# Cost expression
cost_terms = []
for (u, v), w in edges.items():
    cost_terms.append(If(pos[u] + 1 == pos[v], w, 0))
cost_expr = Sum(cost_terms)
solver.minimize(cost_expr)

result = solver.check()
if result != sat:
    print("STATUS: unsat")
    sys.exit(0)
model = solver.model()
min_cost = model.eval(cost_expr).as_long()
# Build path from positions
path = [None]*N
for v in range(N):
    p = model[pos[v]].as_long()
    path[p] = v
# Enumerate all optimal paths
# Create a new solver with cost == min_cost
opt_solver = Solver()
# repeat constraints
for v in range(N):
    opt_solver.add(pos[v] >= 0, pos[v] < N)
opt_solver.add(Distinct(pos))
opt_solver.add(pos[0] == 0, pos[99] == N-1)
for u in range(N):
    for v in range(N):
        if u == v:
            continue
        if (u, v) not in edge_set:
            opt_solver.add(Not(pos[u] + 1 == pos[v]))
# cost equality
opt_solver.add(cost_expr == min_cost)
paths = []
while opt_solver.check() == sat:
    m = opt_solver.model()
    cur_path = [None]*N
    for v in range(N):
        cur_path[m[pos[v]].as_long()] = v
    paths.append(cur_path)
    # block this solution
    block = []
    for v in range(N):
        block.append(pos[v] != m[pos[v]])
    opt_solver.add(Or(block))

output = {
    "paths": paths,
    "count": len(paths),
    "exists": len(paths) > 0,
    "min_cost": min_cost
}
print("STATUS: sat")
print(json.dumps(output))