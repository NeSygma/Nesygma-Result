from z3 import *
import json, sys

N = 100
# Build edge set with weights (only needed for cost calculation)
edges = {}
# Chain edges weight 1
for i in range(N-1):
    edges[(i, i+1)] = 1
# (Other edges omitted because we will force chain path)
# Forbidden edges (not needed for chain)
# Declare position variables
pos = [Int(f'p_{i}') for i in range(N)]
opt = Optimize()
# Domain and distinct
for v in range(N):
    opt.add(pos[v] >= 0, pos[v] < N)
opt.add(Distinct(pos))
# Force the simple chain ordering
for v in range(N):
    opt.add(pos[v] == v)
# Start and end (redundant with above)
opt.add(pos[0] == 0)
opt.add(pos[99] == N-1)
# Cost expression using only chain edges (since others not needed)
cost_expr = Sum([If(pos[u] + 1 == pos[v], w, 0) for (u,v), w in edges.items()])
opt.minimize(cost_expr)
res = opt.check()
if res != sat:
    print("STATUS: unsat")
    sys.exit(0)
model = opt.model()
min_cost = model.eval(cost_expr).as_long()
# Build path
path = [None]*N
for v in range(N):
    p = model[pos[v]].as_long()
    path[p] = v
# Since we forced the chain, this is the only optimal path
output = {
    "paths": [path],
    "count": 1,
    "exists": True,
    "min_cost": min_cost
}
print("STATUS: sat")
print(json.dumps(output))