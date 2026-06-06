from z3 import *
import json

# Create optimizer
opt = Optimize()

# Define vertices 0..99
N = 100
p = [Int(f'p_{i}') for i in range(N)]

# Basic constraints: start and end
opt.add(p[0] == 0)
opt.add(p[99] == 99)

# All vertices must be distinct
opt.add(Distinct(p))

# Build allowed edges and weights
allowed_edges = []
weights = {}

# 1. Chain edges (weight 1)
for i in range(0, 99):
    allowed_edges.append((i, i+1))
    weights[(i, i+1)] = 1

# 2. Local swap gadgets (weight 3)
for N_val in range(0, 24):
    B = 2 + 4 * N_val
    allowed_edges.append((B, B+2))
    weights[(B, B+2)] = 3
    allowed_edges.append((B+2, B+1))
    weights[(B+2, B+1)] = 3
    allowed_edges.append((B+1, B+3))
    weights[(B+1, B+3)] = 3

# 3. Skips of length 2 (weight 4)
for N_val in range(0, 25):
    S = 4 * N_val
    if S + 2 <= 99:
        allowed_edges.append((S, S+2))
        weights[(S, S+2)] = 4

# 4. Jumps of length 3 (weight 5)
for N_val in range(0, 24):
    T = 1 + 4 * N_val
    allowed_edges.append((T, T+3))
    weights[(T, T+3)] = 5

# 5. Long bridges of length 4 (weight 6)
for K in range(0, 20):
    U = 5 * K
    allowed_edges.append((U, U+4))
    weights[(U, U+4)] = 6

# Forbidden edges
forbidden = set()

# Base forbids
forbidden.add((0, 2))
forbidden.add((1, 3))

# Periodic forbids
for N_val in range(0, 12):
    F = 2 + 8 * N_val
    forbidden.add((F, F+2))

for N_val in range(0, 13):
    G = 8 * N_val
    if G + 2 <= 99:
        forbidden.add((G, G+2))

for N_val in range(0, 12):
    H = 1 + 8 * N_val
    forbidden.add((H, H+3))

for M in range(0, 10):
    L = 10 * M + 5
    if L + 4 <= 99:
        forbidden.add((L, L+4))

# Remove forbidden edges from allowed
allowed_edges = [e for e in allowed_edges if e not in forbidden]

print(f"Total allowed edges: {len(allowed_edges)}")

# Edge constraints: for each consecutive pair, must be an allowed edge
for i in range(99):
    edge_options = []
    for (u, v) in allowed_edges:
        edge_options.append(And(p[i] == u, p[i+1] == v))
    opt.add(Or(edge_options))

# Calculate total cost
total_cost = Int('total_cost')
cost_terms = []
for i in range(99):
    edge_cost = Int(f'edge_cost_{i}')
    edge_options = []
    for (u, v) in allowed_edges:
        w = weights[(u, v)]
        edge_options.append(And(p[i] == u, p[i+1] == v, edge_cost == w))
    opt.add(Or(edge_options))
    cost_terms.append(edge_cost)

opt.add(total_cost == Sum(cost_terms))

# Minimize total cost
opt.minimize(total_cost)

print("Finding minimum cost...")
result = opt.check()
if result == sat:
    m = opt.model()
    min_cost = m.eval(total_cost, model_completion=True)
    print(f"Minimum cost: {min_cost}")
    
    # Now find all paths with this minimum cost
    opt2 = Optimize()
    
    # Add all constraints again
    p2 = [Int(f'p2_{i}') for i in range(N)]
    opt2.add(p2[0] == 0)
    opt2.add(p2[99] == 99)
    opt2.add(Distinct(p2))
    
    for i in range(99):
        edge_options = []
        for (u, v) in allowed_edges:
            edge_options.append(And(p2[i] == u, p2[i+1] == v))
        opt2.add(Or(edge_options))
    
    # Calculate cost
    cost_terms2 = []
    for i in range(99):
        edge_cost2 = Int(f'edge_cost2_{i}')
        edge_options = []
        for (u, v) in allowed_edges:
            w = weights[(u, v)]
            edge_options.append(And(p2[i] == u, p2[i+1] == v, edge_cost2 == w))
        opt2.add(Or(edge_options))
        cost_terms2.append(edge_cost2)
    
    total_cost2 = Sum(cost_terms2)
    opt2.add(total_cost2 == min_cost)
    
    # Enumerate all solutions with this cost
    solutions = []
    max_solutions = 1000
    
    while opt2.check() == sat and len(solutions) < max_solutions:
        m2 = opt2.model()
        path = [m2.eval(p2[i], model_completion=True) for i in range(N)]
        path_ints = [int(str(v)) for v in path]
        solutions.append(path_ints)
        
        # Block this solution
        block = Or([p2[i] != path_ints[i] for i in range(N)])
        opt2.add(block)
    
    # Prepare output
    output = {
        "paths": solutions,
        "count": len(solutions),
        "exists": True,
        "min_cost": int(str(min_cost))
    }
    
    print(json.dumps(output, separators=(',', ':')))
    
elif result == unsat:
    print("STATUS: unsat")
    print("No Hamiltonian path exists")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")