from z3 import *

# ============================================================
# Problem Setup
# ============================================================
vertices = list(range(1, 16))
protected = {1, 15}
costs = {1:10, 2:4, 3:5, 4:6, 5:7, 6:9, 7:8, 8:2, 9:4, 10:3, 11:5, 12:7, 13:6, 14:6, 15:12}

groups = {
    'A': [2, 3, 4],
    'B': [5, 6, 7],
    'C': [8, 9, 10],
    'D': [11, 12, 13],
    'E': [14]
}

# Core edges (always present)
core_edges = [
    (1,2), (1,5), (1,8),
    (2,3), (3,4), (4,2),       # cycle A
    (5,6), (6,7), (7,5),       # cycle B
    (8,9), (9,10), (10,8),     # cycle C
    (11,12), (12,13), (13,11), # cycle D
    (2,11), (4,14), (7,14), (10,15),
    (14,1)                      # long cycle through protected vertex
]

# Conditional edges: (source, target, source_vertex)
# Present only if source_vertex is NOT removed
conditional_edges = [
    (3, 7, 3), (3, 11, 3),
    (6, 10, 6), (6, 13, 6),
    (9, 13, 9), (9, 14, 9),
    (12, 4, 12), (12, 7, 12)
]

# ============================================================
# Z3 Model
# ============================================================
opt = Optimize()

# Decision variables: remove[v] = True if vertex v is removed
remove = {v: Bool(f'remove_{v}') for v in vertices}

# Protected vertices cannot be removed
for v in protected:
    opt.add(remove[v] == False)

# Group constraints: at most one vertex per group can be removed
for gname, gmembers in groups.items():
    # At most one removed in each group
    for i in range(len(gmembers)):
        for j in range(i+1, len(gmembers)):
            opt.add(Not(And(remove[gmembers[i]], remove[gmembers[j]])))

# ============================================================
# Acyclicity via topological ordering
# ============================================================
# For remaining vertices, assign a topological order number.
# If there's an edge u->v in the remaining graph, then order[u] < order[v].
# If a cycle exists, no such ordering is possible.

# Topological order for each vertex (only meaningful if vertex remains)
order = {v: Int(f'order_{v}') for v in vertices}

# Bounds on order values (tight enough for 15 vertices)
for v in vertices:
    opt.add(order[v] >= 0, order[v] <= 15)

# Core edges: if neither endpoint is removed, order[u] < order[v]
for (u, v) in core_edges:
    opt.add(Implies(And(Not(remove[u]), Not(remove[v])), order[u] < order[v]))

# Conditional edges: present only if source is not removed
for (u, v, src) in conditional_edges:
    # Edge exists iff source vertex (src) is not removed AND neither u nor v is removed
    # Actually, the edge is (u,v) and it exists if src (=u) is not removed
    # Both u and v must remain for the edge to matter
    opt.add(Implies(And(Not(remove[src]), Not(remove[v])), order[u] < order[v]))

# ============================================================
# Objective: minimize total removal cost
# ============================================================
total_cost = Sum([If(remove[v], costs[v], 0) for v in vertices])
opt.minimize(total_cost)

# ============================================================
# Solve
# ============================================================
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    removed = sorted([v for v in vertices if m.evaluate(remove[v], model_completion=True)])
    remaining = sorted([v for v in vertices if not m.evaluate(remove[v], model_completion=True)])
    removed_costs = [costs[v] for v in removed]
    total = sum(removed_costs)
    
    print("STATUS: sat")
    print(f"feedback_set: {removed}")
    print(f"costs: {removed_costs}")
    print(f"total_cost: {total}")
    print(f"remaining_vertices: {remaining}")
    
    # Verify acyclicity by checking the topological order
    print("\n--- Verification ---")
    print(f"Removed vertices: {removed}")
    print(f"Total cost: {total}")
    
    # Print topological order for remaining vertices
    print("\nTopological order of remaining vertices:")
    for v in remaining:
        print(f"  v{v}: order = {m.evaluate(order[v], model_completion=True)}")
    
    # Check all edges are satisfied
    print("\nEdge checks (u->v requires order[u] < order[v]):")
    all_ok = True
    for (u, v) in core_edges:
        if u not in removed and v not in removed:
            ou = m.evaluate(order[u], model_completion=True).as_long()
            ov = m.evaluate(order[v], model_completion=True).as_long()
            ok = ou < ov
            if not ok:
                print(f"  VIOLATED: core edge {u}->{v}: order[{u}]={ou}, order[{v}]={ov}")
                all_ok = False
    for (u, v, src) in conditional_edges:
        if src not in removed and v not in removed:
            ou = m.evaluate(order[u], model_completion=True).as_long()
            ov = m.evaluate(order[v], model_completion=True).as_long()
            ok = ou < ov
            if not ok:
                print(f"  VIOLATED: conditional edge {u}->{v} (src={src}): order[{u}]={ou}, order[{v}]={ov}")
                all_ok = False
    if all_ok:
        print("  All edge constraints satisfied - graph is acyclic!")
    
    # Check group constraints
    print("\nGroup constraint check:")
    for gname, gmembers in groups.items():
        removed_in_group = [v for v in gmembers if v in removed]
        print(f"  Group {gname}: removed {removed_in_group} (max 1 allowed)")
        
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")