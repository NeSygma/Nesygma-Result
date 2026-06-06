from z3 import *

# BENCHMARK_MODE: ON (model-finding with guaranteed solvable instances)
BENCHMARK_MODE = True

# Declare the solver for optimization
opt = Optimize()

# Vertices: 0 to 15
vertices = range(16)

# Selected[i] is True if vertex i is selected in the cover
selected = [Bool(f"selected_{i}") for i in vertices]

# Vertex costs: high-cost vertices (2,10,14) have cost 3; others have cost 1
costs = {i: 3 if i in [2, 10, 14] else 1 for i in vertices}

# Total cost expression
total_cost = Sum([If(selected[i], costs[i], 0) for i in vertices])

# Add the objective: minimize total cost
opt.minimize(total_cost)

# Standard edges: must be covered by at least one endpoint
standard_edges = [(1,3), (1,4), (2,6), (3,7), (4,8), (5,11), (6,7), (7,12), (8,12), (11,13), (12,13), (13,14)]
for u, v in standard_edges:
    opt.add(Or(selected[u], selected[v]))

# Heavy edges: must be covered by both endpoints OR just the master vertex if one endpoint is a master vertex
heavy_edges = [(0,5), (9,10), (14,15)]
master_vertices = {0, 15}

for u, v in heavy_edges:
    # Case 1: Neither u nor v is a master vertex -> both must be selected
    if u not in master_vertices and v not in master_vertices:
        opt.add(selected[u])
        opt.add(selected[v])
    # Case 2: One endpoint is a master vertex -> selecting the master vertex alone is sufficient
    elif u in master_vertices:
        opt.add(Or(selected[u], And(selected[u], selected[v])))
    elif v in master_vertices:
        opt.add(Or(selected[v], And(selected[u], selected[v])))

# Antagonistic pairs: at most one vertex can be selected
antagonistic_pairs = [(1,2), (8,9)]
for u, v in antagonistic_pairs:
    opt.add(Not(And(selected[u], selected[v])))

# Check and print result
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract selected vertices
    selected_vertices = [i for i in vertices if is_true(model[selected[i]])]
    # Extract total cost
    total_cost_value = model.eval(total_cost)
    print("STATUS: sat")
    print(f"vertex_cover = {sorted(selected_vertices)}")
    print(f"total_cost = {total_cost_value}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")