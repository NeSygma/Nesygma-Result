from z3 import *
import json

# Build allowed edges dictionary
allowed_edges = {}
# 1. Chain edges
for i in range(0, 99):
    allowed_edges[(i, i+1)] = 1
# 2. Local swap gadgets every 4 vertices starting at 2
for N in range(0, 24):
    B = 2 + 4*N
    allowed_edges[(B, B+2)] = 3
    allowed_edges[(B+2, B+1)] = 3
    allowed_edges[(B+1, B+3)] = 3
# 3. Skips of length 2 at multiples of 4
for N in range(0, 25):
    S = 4*N
    if S+2 <= 99:
        allowed_edges[(S, S+2)] = 4
# 4. Jumps of length 3 for vertices ≡ 1 (mod 4)
for N in range(0, 24):
    T = 1 + 4*N
    if T+3 <= 99:
        allowed_edges[(T, T+3)] = 5
# 5. Long bridges of length 4 at multiples of 5
for K in range(0, 20):
    U = 5*K
    if U+4 <= 99:
        allowed_edges[(U, U+4)] = 6

# Forbidden edges
forbidden = set()
forbidden.add((0, 2))
forbidden.add((1, 3))
for N in range(0, 12):
    F = 2 + 8*N
    forbidden.add((F, F+2))
for N in range(0, 13):
    G = 8*N
    if G+2 <= 99:
        forbidden.add((G, G+2))
for N in range(0, 12):
    H = 1 + 8*N
    forbidden.add((H, H+3))
for M in range(0, 10):
    L = 10*M + 5
    if L+4 <= 99:
        forbidden.add((L, L+4))

# Remove forbidden edges from allowed_edges
for e in forbidden:
    if e in allowed_edges:
        del allowed_edges[e]

# Build allowed successors list for each vertex
allowed_successors = {i: [] for i in range(100)}
for (i,j), w in allowed_edges.items():
    allowed_successors[i].append(j)

# Variables: position of each vertex in the path
pos = [Int(f'pos_{i}') for i in range(100)]

solver = Optimize()
# Domain constraints
for i in range(100):
    solver.add(pos[i] >= 0, pos[i] <= 99)
# Distinct positions
solver.add(Distinct(pos))
# Start and end positions
solver.add(pos[0] == 0)
solver.add(pos[99] == 99)
# Successor constraints: for each vertex except end, its successor must be one of allowed successors
for i in range(100):
    if i == 99:
        continue
    # At least one allowed successor must satisfy pos[i]+1 == pos[j]
    solver.add(Or([pos[i] + 1 == pos[j] for j in allowed_successors[i]]))

# Cost expression
cost_expr = Sum([If(pos[i] + 1 == pos[j], w, 0) for (i,j), w in allowed_edges.items()])
solver.minimize(cost_expr)

result = solver.check()
if result == sat:
    model = solver.model()
    min_cost = model.evaluate(cost_expr, model_completion=True).as_long()
    # reconstruct path
    path = [None]*100
    for v in range(100):
        path[model[pos[v]].as_long()] = v
    output = {
        "paths": [path],
        "count": 1,
        "exists": True,
        "min_cost": min_cost
    }
    print("STATUS: sat")
    print(json.dumps(output))
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")