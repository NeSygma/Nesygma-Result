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

# Helper: allowed edge (u, v) with weight w
# We will define a function to check if an edge is allowed and return its weight

def is_allowed_edge(u, v):
    # Chain edges: (i, i+1) with weight 1
    chain_edges = And([And(path[i] == u, path[i+1] == v) for i in range(N-1)])
    chain_weight = 1
    
    # Local swap gadgets: for N in 0..23, B = 2 + 4*N
    # Edges: (B, B+2), (B+2, B+1), (B+1, B+3) with weight 3
    local_swap_edges = Or([
        And(u == (2 + 4*N), v == (2 + 4*N + 2)) for N in range(24)
    ] + [
        And(u == (2 + 4*N + 2), v == (2 + 4*N + 1)) for N in range(24)
    ] + [
        And(u == (2 + 4*N + 1), v == (2 + 4*N + 3)) for N in range(24)
    ])
    local_swap_weight = 3
    
    # Skips of length 2: for N in 0..24, S = 4*N with S+2 <= 99
    # Edge: (S, S+2) with weight 4
    skip_edges = Or([
        And(u == (4*N), v == (4*N + 2)) for N in range(25) if 4*N + 2 <= 99
    ])
    skip_weight = 4
    
    # Jumps of length 3: for N in 0..23, T = 1 + 4*N
    # Edge: (T, T+3) with weight 5
    jump_edges = Or([
        And(u == (1 + 4*N), v == (1 + 4*N + 3)) for N in range(24)
    ])
    jump_weight = 5
    
    # Long bridges: for K in 0..19, U = 5*K
    # Edge: (U, U+4) with weight 6
    bridge_edges = Or([
        And(u == (5*K), v == (5*K + 4)) for K in range(20) if 5*K + 4 <= 99
    ])
    bridge_weight = 6
    
    # The edge (u, v) is allowed if it matches any of the above patterns
    allowed = Or(chain_edges, local_swap_edges, skip_edges, jump_edges, bridge_edges)
    
    # Forbidden edges (must not be used)
    # Base forbids: (0,2), (1,3)
    forbidden_base = Or(And(u == 0, v == 2), And(u == 1, v == 3))
    
    # Periodic forbids:
    # For N in 0..11, F = 2 + 8*N: forbid (F, F+2)
    forbidden_periodic1 = Or([And(u == (2 + 8*N), v == (2 + 8*N + 2)) for N in range(12)])
    
    # For N in 0..12, G = 8*N with G+2 <= 99: forbid (G, G+2)
    forbidden_periodic2 = Or([And(u == (8*N), v == (8*N + 2)) for N in range(13) if 8*N + 2 <= 99])
    
    # For N in 0..11, H = 1 + 8*N: forbid (H, H+3)
    forbidden_periodic3 = Or([And(u == (1 + 8*N), v == (1 + 8*N + 3)) for N in range(12)])
    
    # For M in 0..9, L = 10*M + 5 with L+4 <= 99: forbid (L, L+4)
    forbidden_periodic4 = Or([And(u == (10*M + 5), v == (10*M + 5 + 4)) for M in range(10) if 10*M + 5 + 4 <= 99])
    
    forbidden = Or(forbidden_base, forbidden_periodic1, forbidden_periodic2, forbidden_periodic3, forbidden_periodic4)
    
    # The edge is allowed and not forbidden
    return And(allowed, Not(forbidden))

# Total cost variable
total_cost = Int("total_cost")

# For each consecutive pair in the path, ensure the edge is allowed and add its weight to the total cost
cost_expr = []
for i in range(N-1):
    u = path[i]
    v = path[i+1]
    # Check if the edge (u, v) is allowed and not forbidden
    opt.add(is_allowed_edge(u, v))
    # Add the weight of the edge to the total cost
    # We need to determine the weight of the edge (u, v)
    # This is tricky because we need to know which pattern the edge matches
    # Instead, we can precompute the weight for each possible edge in the graph
    # But for now, we will use a big Or to match the weight
    weight = Int(f"weight_{i}")
    # Chain edge weight 1
    opt.add(Implies(And(u + 1 == v, u >= 0, u <= 98), weight == 1))
    # Local swap gadgets: (B, B+2), (B+2, B+1), (B+1, B+3) weight 3
    for N in range(24):
        B = 2 + 4*N
        opt.add(Implies(And(u == B, v == B+2), weight == 3))
        opt.add(Implies(And(u == B+2, v == B+1), weight == 3))
        opt.add(Implies(And(u == B+1, v == B+3), weight == 3))
    # Skips: (S, S+2) weight 4
    for N in range(25):
        S = 4*N
        if S + 2 <= 99:
            opt.add(Implies(And(u == S, v == S+2), weight == 4))
    # Jumps: (T, T+3) weight 5
    for N in range(24):
        T = 1 + 4*N
        opt.add(Implies(And(u == T, v == T+3), weight == 5))
    # Bridges: (U, U+4) weight 6
    for K in range(20):
        U = 5*K
        if U + 4 <= 99:
            opt.add(Implies(And(u == U, v == U+4), weight == 6))
    # Default weight (should not happen if edge is allowed)
    opt.add(Implies(Not(Or(
        And(u + 1 == v, u >= 0, u <= 98),
        *[And(u == (2 + 4*N), v == (2 + 4*N + 2)) for N in range(24)],
        *[And(u == (2 + 4*N + 2), v == (2 + 4*N + 1)) for N in range(24)],
        *[And(u == (2 + 4*N + 1), v == (2 + 4*N + 3)) for N in range(24)],
        *[And(u == (4*N), v == (4*N + 2)) for N in range(25) if 4*N + 2 <= 99],
        *[And(u == (1 + 4*N), v == (1 + 4*N + 3)) for N in range(24)],
        *[And(u == (5*K), v == (5*K + 4)) for K in range(20) if 5*K + 4 <= 99]
    )), weight == 0))
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
    min_cost = min(sol for sol in solutions)
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