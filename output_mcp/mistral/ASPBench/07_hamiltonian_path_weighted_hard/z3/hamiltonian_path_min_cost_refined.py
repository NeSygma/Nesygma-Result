from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Number of vertices
N = 100
start = 0
end = 99

# Create a solver for optimization
opt = Optimize()

# Decision variables: path[i] is the i-th vertex in the path
path = [Int(f"path_{i}") for i in range(N)]

# Constraints: path[0] = start, path[N-1] = end
opt.add(path[0] == start)
opt.add(path[N-1] == end)

# All vertices in the path are distinct (Hamiltonian path)
opt.add(Distinct(path))

# Precompute all allowed edges and their weights
allowed_edges = {}

# 1. Chain edges (weight 1): For all i in 0..98: edge (i, i+1) with weight 1
for i in range(N-1):
    allowed_edges[(i, i+1)] = 1

# 2. Local swap gadgets every 4 vertices starting at 2 (weight 3):
# For N in 0..23, let B = 2 + 4*N:
# - Edge (B, B+2) with weight 3
# - Edge (B+2, B+1) with weight 3
# - Edge (B+1, B+3) with weight 3
for N in range(24):
    B = 2 + 4*N
    if B + 2 < N:
        allowed_edges[(B, B+2)] = 3
    if B + 2 < N and B + 1 < N:
        allowed_edges[(B+2, B+1)] = 3
    if B + 1 < N and B + 3 < N:
        allowed_edges[(B+1, B+3)] = 3

# 3. Skips of length 2 at multiples of 4 (weight 4):
# For N in 0..24, let S = 4*N with S+2 <= 99:
# - Edge (S, S+2) with weight 4
for N in range(25):
    S = 4*N
    if S + 2 < N:
        allowed_edges[(S, S+2)] = 4

# 4. Jumps of length 3 for vertices ≡ 1 (mod 4) (weight 5):
# For N in 0..23, let T = 1 + 4*N:
# - Edge (T, T+3) with weight 5
for N in range(24):
    T = 1 + 4*N
    if T + 3 < N:
        allowed_edges[(T, T+3)] = 5

# 5. Long bridges of length 4 at multiples of 5 (weight 6):
# For K in 0..19, let U = 5*K:
# - Edge (U, U+4) with weight 6
for K in range(20):
    U = 5*K
    if U + 4 < N:
        allowed_edges[(U, U+4)] = 6

# Forbidden edges (must not be used)
forbidden_edges = set()

# Base forbids: (0,2), (1,3)
forbidden_edges.add((0, 2))
forbidden_edges.add((1, 3))

# Periodic forbids:
# For N in 0..11, F = 2 + 8*N: forbid (F, F+2)
for N in range(12):
    F = 2 + 8*N
    if F + 2 < N:
        forbidden_edges.add((F, F+2))

# For N in 0..12, G = 8*N with G+2 <= 99: forbid (G, G+2)
for N in range(13):
    G = 8*N
    if G + 2 < N:
        forbidden_edges.add((G, G+2))

# For N in 0..11, H = 1 + 8*N: forbid (H, H+3)
for N in range(12):
    H = 1 + 8*N
    if H + 3 < N:
        forbidden_edges.add((H, H+3))

# For M in 0..9, L = 10*M + 5 with L+4 <= 99: forbid (L, L+4)
for M in range(10):
    L = 10*M + 5
    if L + 4 < N:
        forbidden_edges.add((L, L+4))

# Remove forbidden edges from allowed_edges
for edge in forbidden_edges:
    if edge in allowed_edges:
        del allowed_edges[edge]

# Total cost variable
total_cost = Int("total_cost")

# For each consecutive pair in the path, ensure the edge is allowed and add its weight to the total cost
cost_expr = []
for i in range(N-1):
    u = path[i]
    v = path[i+1]
    # Ensure the edge (u, v) is in allowed_edges
    opt.add(Or([And(u == edge[0], v == edge[1]) for edge in allowed_edges.keys()]))
    # Add the weight of the edge to the total cost
    weight = Int(f"weight_{i}")
    opt.add(Sum([If(And(u == edge[0], v == edge[1]), allowed_edges[edge], 0) for edge in allowed_edges.keys()]) == weight)
    cost_expr.append(weight)

# Total cost is the sum of all edge weights
opt.add(total_cost == Sum(cost_expr))

# Minimize the total cost
opt.minimize(total_cost)

# To find all optimal solutions, we will collect them
solutions = []

# We will iterate to find all solutions with minimal cost
while opt.check() == sat:
    model = opt.model()
    current_cost = model.eval(total_cost)
    current_path = [model.eval(path[i]) for i in range(N)]
    
    # Store the solution
    solutions.append({
        "path": [int(current_path[i].as_long()) for i in range(N)],
        "cost": int(current_cost.as_long())
    })
    
    # Block this solution to find the next one
    block = []
    for i in range(N):
        block.append(path[i] != current_path[i])
    opt.add(Or(block))

# Prepare output
if len(solutions) > 0:
    min_cost = min(sol["cost"] for sol in solutions)
    optimal_solutions = [sol for sol in solutions if sol["cost"] == min_cost]
    output = {
        "paths": [sol["path"] for sol in optimal_solutions],
        "count": len(optimal_solutions),
        "exists": True,
        "min_cost": min_cost
    }
    print("STATUS: sat")
    print(output)
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")