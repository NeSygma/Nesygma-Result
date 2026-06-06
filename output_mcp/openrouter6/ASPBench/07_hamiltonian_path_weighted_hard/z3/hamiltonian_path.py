from z3 import *
import json

# Create solver for optimization
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
allowed_edges = set()
weights = {}

# 1. Chain edges (weight 1)
for i in range(0, 99):
    allowed_edges.add((i, i+1))
    weights[(i, i+1)] = 1

# 2. Local swap gadgets (weight 3)
for N_val in range(0, 24):
    B = 2 + 4 * N_val
    allowed_edges.add((B, B+2))
    weights[(B, B+2)] = 3
    allowed_edges.add((B+2, B+1))
    weights[(B+2, B+1)] = 3
    allowed_edges.add((B+1, B+3))
    weights[(B+1, B+3)] = 3

# 3. Skips of length 2 (weight 4)
for N_val in range(0, 25):
    S = 4 * N_val
    if S + 2 <= 99:
        allowed_edges.add((S, S+2))
        weights[(S, S+2)] = 4

# 4. Jumps of length 3 (weight 5)
for N_val in range(0, 24):
    T = 1 + 4 * N_val
    allowed_edges.add((T, T+3))
    weights[(T, T+3)] = 5

# 5. Long bridges of length 4 (weight 6)
for K in range(0, 20):
    U = 5 * K
    allowed_edges.add((U, U+4))
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
allowed_edges = allowed_edges - forbidden

print(f"Total allowed edges: {len(allowed_edges)}")
print(f"Sample allowed edges: {list(allowed_edges)[:5]}")

# Define weight function
weight_func = Function('weight_func', IntSort(), IntSort(), IntSort())
for (u, v), w in weights.items():
    if (u, v) in allowed_edges:  # Only add if not forbidden
        opt.add(weight_func(u, v) == w)

# Edge constraints: for each consecutive pair, must be an allowed edge
for i in range(99):
    edge_constraints = []
    for (u, v) in allowed_edges:
        edge_constraints.append(And(p[i] == u, p[i+1] == v))
    opt.add(Or(edge_constraints))

# Total cost
total_cost = Sum([weight_func(p[i], p[i+1]) for i in range(99)])
opt.minimize(total_cost)

# Check for optimal solution
print("Solving optimization...")
result = opt.check()
if result == sat:
    model = opt.model()
    min_cost_val = model.eval(total_cost, model_completion=True)
    print(f"Minimal cost: {min_cost_val}")
    
    # Now enumerate all solutions with this minimal cost
    # Create a new solver for enumeration
    solver = Solver()
    
    # Add all constraints again
    solver.add(p[0] == 0)
    solver.add(p[99] == 99)
    solver.add(Distinct(p))
    
    for i in range(99):
        edge_constraints = []
        for (u, v) in allowed_edges:
            edge_constraints.append(And(p[i] == u, p[i+1] == v))
        solver.add(Or(edge_constraints))
    
    # Fix cost to minimal
    solver.add(total_cost == min_cost_val)
    
    # Enumerate all solutions
    solutions = []
    while solver.check() == sat:
        m = solver.model()
        # Extract path
        path = [m.eval(p[i], model_completion=True) for i in range(N)]
        # Convert to Python integers
        path_ints = [int(str(v)) for v in path]
        solutions.append(path_ints)
        
        # Block this solution
        block = Or([p[i] != path_ints[i] for i in range(N)])
        solver.add(block)
    
    # Prepare output
    output = {
        "paths": solutions,
        "count": len(solutions),
        "exists": len(solutions) > 0,
        "min_cost": int(str(min_cost_val))
    }
    
    print(json.dumps(output, separators=(',', ':')))
    
elif result == unsat:
    print("STATUS: unsat")
    print("No Hamiltonian path exists with the given constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown")