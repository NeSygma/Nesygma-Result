from z3 import *

# Define vertices and edges
vertices = [1, 2, 3, 4, 5, 6]
edges = [
    (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 4), (3, 6),
    (4, 2), (4, 5),
    (5, 3), (5, 6),
    (6, 1), (6, 4)
]

# Create solver
opt = Optimize()

# Boolean variables: removed[v] = True if vertex v is removed
removed = {v: Bool(f'removed_{v}') for v in vertices}

# Integer variables: rank[v] for topological ordering
rank = {v: Int(f'rank_{v}') for v in vertices}

# Constraint: ranks must be non-negative (or can be any integer, but non-negative is fine)
for v in vertices:
    opt.add(rank[v] >= 0)

# For each edge (u, v), if both u and v are NOT removed, then rank[u] < rank[v]
for u, v in edges:
    # If u is not removed AND v is not removed, then rank[u] < rank[v]
    opt.add(Implies(And(Not(removed[u]), Not(removed[v])), rank[u] < rank[v]))

# Objective: minimize the number of removed vertices
# Count removed vertices: sum of If(removed[v], 1, 0) for all v
removed_count = Sum([If(removed[v], 1, 0) for v in vertices])
opt.minimize(removed_count)

# Check and print results
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Get removed vertices
    removed_vertices = [v for v in vertices if is_true(model[removed[v]])]
    print(f"Removed vertices: {removed_vertices}")
    print(f"Number of removed vertices: {len(removed_vertices)}")
    
    # Verify the solution is optimal
    print(f"Optimal size: {len(removed_vertices)}")
    
    # Show remaining graph
    remaining_vertices = [v for v in vertices if v not in removed_vertices]
    remaining_edges = [(u, v) for u, v in edges if u not in removed_vertices and v not in removed_vertices]
    print(f"Remaining vertices: {remaining_vertices}")
    print(f"Remaining edges: {remaining_edges}")
    
    # Verify acyclicity by checking ranks
    print("Vertex ranks (for topological ordering):")
    for v in remaining_vertices:
        print(f"  Vertex {v}: rank = {model[rank[v]]}")
    
    # Check if any edge violates rank ordering
    violations = []
    for u, v in remaining_edges:
        u_rank = model[rank[u]].as_long()
        v_rank = model[rank[v]].as_long()
        if u_rank >= v_rank:
            violations.append((u, v, u_rank, v_rank))
    
    if violations:
        print("WARNING: Found rank violations (graph may not be acyclic):")
        for u, v, ur, vr in violations:
            print(f"  Edge {u}→{v}: rank[{u}]={ur}, rank[{v}]={vr}")
    else:
        print("✓ Graph is acyclic (all edges satisfy rank[u] < rank[v])")
    
    # Print answer in required format
    print(f"answer:{len(removed_vertices)}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")